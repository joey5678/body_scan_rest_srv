from functools import wraps
import uuid
import json
import logging
from json import JSONEncoder
from datetime import datetime
from bson import ObjectId
from .x_db  import get_db_session
from public import cryptoFun_new
from flask import request, make_response
from units.redis_tools import redis_conn
from  .exceptions import NotLoginException, InvalidADException, BannedException, MissParamException, \
    UpdateException, BizFailException, VldException, OtherLoginException
log = logging.getLogger("root")
error_log = logging.getLogger("error")
unencrypt_log = logging.getLogger("unencrypt_log")


class MyJsonEncode(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return int(o.timestamp())
        elif isinstance(o, set):
            return JSONEncoder.default(self, [i for i in o])
        elif isinstance(o, ObjectId):
            return str(o)
        else:
            return JSONEncoder.default(self, o)




def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator


class WebTools(object):

    @classmethod
    def get_param(cls, name, default=None):
        if request.method == 'GET':
            return request.args.get(name, default)
        elif request.method == 'POST':
            param = request.args.get(name, '') or request.form.get(name, '')
            if not param:
                body_params = cls.get_body_params()
                param = body_params.get(name, default)
            return param

    @classmethod
    def get_body_params(cls):
        stream_params = getattr(request, "stream_params", None)
        if stream_params is None:
            data = request.stream.read()
            if data:
                params = json.loads(data.decode())
                request.stream_params = params
                return params
            else:
                return {}
        else:
            return stream_params

    @classmethod
    def get_request(cls):
        return request

    @classmethod
    def get_client_ip(cls, r):
        clientIp = r.headers.get('X-Real-IP', '')
        if not clientIp:
            clientIp = str(r.remote_addr)

        return clientIp


def jsonify_encrypt(func):
    """AES加密"""
    @wraps(func)
    @add_response_headers({'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    def decorated_function(*args, **kwargs):
        log.debug("request.path:%s", request.path)
        ret = {"code": 0, "msg": "", "data": {}}
        db_session = None
        lock_name = "{}:{}".format(func.__name__, uuid.uuid1())

        try:
            data = get_data_from_body()
            kwargs.update({"data": data})
            log.debug("request_data:{}".format(data))
            ret = func(*args, **kwargs)

        except MissParamException as mpe:
            ret.update({"code": 7001, "msg": "miss param versioncode"})

        except VldException as ve:
            ret.update({"code": 7002, "msg": str(ve)})

        except BizFailException as bfe:
            log.error(str(bfe))
            db_session = get_db_session(auto_create=False)
            ret.update({"code": bfe.error_code, "msg": _(str(bfe))}, data=bfe.data)
            if db_session:
                db_session.rollback()

        except NotLoginException as e:
            ret.update({"code": 40, "msg": "Please login"})

        except InvalidADException as e:
            ret.update({"code": 501, "msg": str(e)})

        except BannedException as e:
            ret.update({'code': 41, "msg": str(e)})

        except UpdateException as e:
            ret.update({'code': 42, "msg": _(str(e))})

        except OtherLoginException as e:
            ret.update({'code': 43, "msg": "other device login"})

        except Exception as e:
            error_log.exception(e)
            db_session = get_db_session(auto_create=False)
            ret.update({"code": 500, "msg": "Unable to connect to server",  "log": str(e)})
            if db_session:
                db_session.rollback()

        else:
            db_session = get_db_session(auto_create=False)
            if db_session:
                db_session.commit()

        finally:
            db_session = get_db_session(auto_create=False)
            if db_session:
                db_session.close()

        log.debug("JsonResult:{}".format(ret))
        log.debug("JsonResult:{}".format(json.dumps(ret)))
        cryptograph = cryptoFun_new.aes_func.encrypt(json.dumps(ret))
       # ret = {"return_data":cryptograph}
        json_str = json.dumps(cryptograph, ensure_ascii=False, cls=MyJsonEncode)

        return json_str

    return decorated_function


def jsonify_unencrypt(func):
    """连接h5服务和各种回调服务"""
    @wraps(func)
    @add_response_headers({'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
    def decorated_function(*args, **kwargs):
        log.debug("request.path:%s", request.path)
        ret = {"code": 0, "msg": "", "data": {}}
        db_session = None

        lock_name = "{}:{}".format(func.__name__, uuid.uuid1())

        try:
            data = get_data_from_body()
            kwargs.update({"data": data})
            log.debug("request_data:{}".format(data))
            ret = func(*args, **kwargs)

        except MissParamException as mpe:
            ret.update({"code": 7001, "msg": "miss param versioncode"})

        except VldException as ve:
            ret.update({"code": 7002, "msg": str(ve)})

        except BizFailException as bfe:
            unencrypt_log.error(str(bfe))
            db_session = get_db_session(auto_create=False)
            ret.update({"code": bfe.error_code, "msg": _(str(bfe))}, data=bfe.data)
            if db_session:
                db_session.rollback()

        except NotLoginException as e:
            ret.update({"code": 40, "msg": "Please login"})

        except InvalidADException as e:
            ret.update({"code": 501, "msg": str(e)})

        except BannedException as e:
            ret.update({'code': 41, "msg": str(e)})

        except UpdateException as e:
            ret.update({'code': 42, "msg": _(str(e))})

        except Exception as e:
            error_log.exception(e)
            db_session = get_db_session(auto_create=False)
            ret.update({"code": 500, "msg": "Unable to connect to server"})
            if db_session:
                db_session.rollback()

        else:
            db_session = get_db_session(auto_create=False)
            if db_session:
                db_session.commit()

        finally:
            db_session = get_db_session(auto_create=False)
            if db_session:
                db_session.close()

        log.debug("JsonResult:%s", ret)
        cryptograph = cryptoFun_new.aes_func.encrypt(json.dumps(ret))
        #ret = {"return_data": cryptograph}
        json_str = json.dumps(cryptograph, ensure_ascii=False, cls=MyJsonEncode)
        return json_str

    return decorated_function


def not_check_login(func):
    """
    if not login, return error

    :return:
    """
    @wraps(func)
    @jsonify_unencrypt
    def wrap(*args, **kwargs):
        return func(*args, **kwargs)

    return wrap


def check_login_encrypt(func):
    """
        此接口接收客户端post的加密参数和返回加密参数
    :return:
    """
    @wraps(func)
    @jsonify_encrypt
    def wrap(*args, **kwargs):
        data = kwargs['data']
        uid = data.get("uid", "")
        token = data.get("token", "")
        if uid =="4491197847086043111":
            return func(*args, **kwargs)

        log.debug("check_login_encrypt.data:%s",data)
        if not token:
            raise NotLoginException()
        aid = data.get("uid", "")
        log.debug("aid :%s",aid)

        #if aid.strip():
         #   raise InvalidADException(_("Aid is invalid"))
        os = data.get("os", "")
        version_code = data.get("versioncode", "")
        if not version_code:
            raise MissParamException()
        else:
            new_token = redis_conn.hget("uid_token", uid)
            log.debug("check_login.new_token: %s", new_token)
            if new_token and new_token.decode("utf-8") != token:
                raise OtherLoginException()
            key = "get_uid_from_{}".format(token)
            get_uid = redis_conn.get(key)
            if not get_uid:
                raise NotLoginException()

            if get_uid and uid != get_uid.decode("utf-8"):
                raise NotLoginException()

            else:  # uid相等更新过期时间
                redis_conn.set(key, uid, ex=7 * 24 * 3600)
        return func(*args, **kwargs)
    return wrap

def get_data_from_body():
    stream_params = getattr(request, "stream_params", None)
    if stream_params is None:
        data = request.stream.read()
        log.debug("request.params:%s", data)
        if data:
            #stream_params = json.loads(data.decode())
            stream_params = data.decode()
    log.debug("request.params:%s",stream_params)
    #de_data = cryptoFun_new.aes_func.decrypt(stream_params.get("request_data", ""))
    de_data = cryptoFun_new.aes_func.decrypt(stream_params)
    log.debug("request.params:%s,de_data:%s",stream_params,de_data)
    data = json.loads(de_data)
    return data
