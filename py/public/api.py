# coding=utf-8
import hashlib
import json
import pickle
import re
import functools
import time
from public import x_db
from units.redis_tools import redis_conn

# 暂不能删除，api 代码中引用了它
from .exceptions import BizFailException


class ApiResult(dict):

    def error(self, code=4004, msg="", data={}):
        self["code"] = code
        self["msg"] = msg
        self["data"] = data
        return self

    def success(self, code=0, data={}, msg="success"):
        self["code"] = code
        self["msg"] = msg
        self["data"] = data
        return self

    @classmethod
    def get_inst(cls):
        return ApiResult(code=0, msg="", data={})


class BaseApi(object):

    @property
    def db_session(self):
        return x_db.get_db_session(auto_create=True)

    @classmethod
    def get_db_session(cls, auto_create=True):
        return x_db.get_db_session(auto_create=auto_create)


def get_db_session(auto_create=True):
    return x_db.get_db_session(auto_create=auto_create)


def convert_to_builtin_type(obj):
    """
    其它类型的对象转换为json str
    """
    from bson import ObjectId
    # from mongoengine import Document
    import datetime

    if isinstance(obj, ObjectId):
        return "%s" % obj

    elif isinstance(obj, datetime.datetime):
        return "%.3f" % obj.timestamp()

    # elif isinstance(obj, Document):
    #     return "%s" % obj.id

    raise Exception("%s is not JSON serializable" % obj)


def rds_api_cache(ex=300, mgr_key=""):
    """
    Api方法结果缓存， Api方法参数要求是简单的类型， 装饰器排列在最底层
    :param ex: T-int, 设置过期时间
    :param mgr_key: T-string, 管理键eval表达式
    :example:

    @xxx
    @rds_api_cache(ex=60)
    def api_method(self):
    """

    def wrapper(func):

        @functools.wraps(func)
        def _d(*args, **kwargs):

            def _get_params_key():
                _args = args[1:]
                _kwargs = {}
                _kwargs.update(kwargs)

                for index, _arg in enumerate(_args):
                    _kwargs["_arg_%d" % index] = _arg

                pkey_name = json.dumps(_kwargs, sort_keys=True, default=convert_to_builtin_type)
                pn_bytes = pkey_name.encode("utf-8")
                pn_key = "{}{}".format(hashlib.md5(pn_bytes).hexdigest(), hashlib.sha256(pn_bytes).hexdigest())
                return pn_key

            def _mk_func_name_key():

                find = re.findall("function\s(\w+\.\w+)", "%s" % func)
                func_name = find[0]

                func_name_key = "api_cache_" + func_name
                if mgr_key:
                    _mgr_key = eval(mgr_key, {"args": args, "kwargs": kwargs})
                else:
                    _mgr_key = _get_params_key()
                _func_key = func_name_key + '_' + str(_mgr_key)

                return _func_key

            func_key = _mk_func_name_key()
            dumps_data = redis_conn.get(func_key)

            if dumps_data is None:
                rs = func(*args, **kwargs)
                dumps_data = pickle.dumps(rs)
                redis_conn.set(func_key, dumps_data, ex=ex)

                return rs

            rs = pickle.loads(dumps_data)
            return rs

        return _d

    return wrapper


def delete_api_cache_key(method_name, mgr_key=""):
    """
    删除缓存
    """
    target_key_name = "api_cache_%s_%s" % (method_name, mgr_key)
    redis_conn.delete(target_key_name)


class DistributedLock(object):
    """
    分布式锁,基于Redis的setNx特性实现
    name 请根据锁定的资源名称制定，不要随意使用相同的名称，避免相同的资源锁名
    """

    def __init__(self, name, timeout=2, ex=10, slp=0.4):
        self.name = "DistributedLock:" + name
        self.trys = timeout
        self.ex = ex
        self.slp = slp
        self.ts = time.time()

    def __enter__(self):
        locked = self._try_lock()
        if not locked: raise Exception("Distributed Lock Timeout.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._release()

    def _try_lock(self):
        """尝试得到锁，超时返回False"""
        rds = redis_conn
        while True:
            locked = rds.set(self.name, 1, ex=self.ex, nx=True)
            if locked: return True
            if time.time() - self.ts >= self.trys: return False
            time.sleep(self.slp or 1)

        return False

    def _release(self):
        rds = redis_conn
        rds.delete(self.name)
        return True

    @classmethod
    def nx_lock(cls, name, ex=10):
        """
        给资源上锁
        :param name:
        :param ex:
        :return: bool
        """
        rds = redis_conn
        locked = rds.set("NX_LOCK:{}".format(name), 1, ex=ex, nx=True)
        if locked: return True

        return False

    @classmethod
    def del_nx_lock(cls, name):
        """
        删除资源锁
        :param name:
        """
        rds = redis_conn
        rds.delete("NX_LOCK:".format(name))
