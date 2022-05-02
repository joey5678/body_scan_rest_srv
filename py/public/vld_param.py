# coding=utf-8
import collections
import datetime
import json
import logging
import re

from flask import request
from public import cryptoFun_new

from  .exceptions import VldException, MissParamException
from  .http_tool import WebTools

log = logging.getLogger("root")
params_log = logging.getLogger('params')


class Validator(object):

    @classmethod
    def required(cls, param_item):
        value = param_item.get("value", None)
        message = param_item.get("message", "") or "{label} required"
        if (value is None or value == ""):
            raise VldException(message.format(**param_item))

    @classmethod
    def in_list(cls, range_list):
        range_list = list(range_list)

        def _v(param_item):
            value = param_item.get("value", None)
            message = param_item.get("message", "") or "{label} out of range"
            if (value not in range_list):
                raise VldException(message.format(**param_item))

        return _v

    @classmethod
    def range(cls, min, max):

        def _v(param_item):
            value = param_item.get("value", None)
            message = param_item.get("message", "") or "{label} out of range {min}~{max}"

            _param_item = {"min": min, "max": max}
            _param_item.update(param_item)
            if (not (min <= value <= max)):
                raise VldException(message.format(**_param_item))

        return _v

    @classmethod
    def regex(cls, pattern):
        def _v(param_item):
            value = param_item.get("value", "") or ""
            message = param_item.get("message", "") or "{label} Input error, please reenter"

            if (not re.findall(pattern, str(value))):
                raise VldException(message.format(**param_item))

        return _v


def vld_params_encrypt(data, params):
    """
        接收客户端传过来的加密信息-----【post】的方法
        :param params:
        :return:
    """
    xparams = {}
    ordered_dict = collections.OrderedDict(params)
    for key, val in ordered_dict.items():

        find1 = re.findall("(\w+)(?:\:(str|int|float|datetime))?", key)

        param_name = ""
        param_type = "auto"
        param_default = None
        param_val = None

        if (find1):
            param_name = find1[0][0]
            param_type = find1[0][1] if find1[0][1] else "auto"

        param_default = val.get("default", None)
        param_label = val.get("label", "") or param_name

        if not param_name:
            continue

        param_val = data.get(param_name, param_default)

        if (param_val and param_type == "auto" and isinstance(param_val, str)):
            if (param_val.isdigit()):
                try:
                    param_val = int(param_val)
                except Exception as e:
                    try:
                        param_val = float(param_val)
                    except Exception as e:
                        pass

        if (param_type in ["str", "int", "float", "datetime"] and param_val is None):
            raise MissParamException("missing param [{label}]".format(label=param_label))

        try:
            if (param_type == "str"):
                pass

            elif (param_type == "int"):
                param_val = int(param_val)

            elif (param_type == "float"):
                param_val = float(param_val)

            elif (param_type == "datetime" and param_val and isinstance(param_val, str)):
                _dt = None
                try:
                    _dt = datetime.datetime.strptime(param_val, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    pass

                try:
                    _dt = datetime.datetime.strptime(param_val, "%Y-%m-%d %H:%M")
                except Exception as e:
                    pass

                try:
                    _dt = datetime.datetime.strptime(param_val, "%Y-%m-%d")
                except Exception as e:
                    pass

                if _dt is None:
                    raise Exception()
                else:
                    param_val = _dt

        except Exception as e:
            raise VldException("Parameter[{label}] conversion failure".format(label=param_label))

        rule_method = val.get("rule", None)

        if rule_method:
            rule_method(dict(label=param_label, value=param_val, message=val.get("message", "")))

        xparams[val.get("rename", "") or param_name] = param_val

    params_log.debug("xparams:%s", xparams)

    return xparams


def vld_params_unencrypt(params):

    xparams = {}
    ordered_dict = collections.OrderedDict(params)
    for key, val in ordered_dict.items():

        find1 = re.findall("(\w+)(?:\:(str|int|float|datetime))?", key)

        param_name = ""
        param_type = "auto"
        param_default = None
        param_val = None

        if(find1):
            param_name = find1[0][0]
            param_type = find1[0][1] if find1[0][1] else "auto"

        param_default = val.get("default", None)
        param_label = val.get("label", "") or param_name

        if not param_name: continue

        param_val = WebTools.get_param(param_name, param_default)

        if(param_val and param_type == "auto" and isinstance(param_val, str)):
            if(param_val.isdigit()):
                try:
                    param_val = int(param_val)
                except Exception as e:

                    try:
                        param_val = float(param_val)
                    except Exception as e:
                        pass

        if(param_type in ["str", "int", "float", "datetime"] and param_val is None):
            raise MissParamException("missing param [{label}]".format(label=param_label))

        try:
            if (param_type == "str"):
                pass

            elif (param_type == "int"):
                param_val = int(param_val)

            elif (param_type == "float"):
                param_val = float(param_val)

            elif (param_type == "datetime" and param_val and isinstance(param_val, str)):
                _dt = None
                try:
                    _dt = datetime.datetime.strptime(param_val, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    pass

                try:
                    _dt = datetime.datetime.strptime(param_val, "%Y-%m-%d %H:%M")
                except Exception as e:
                    pass

                try:
                    _dt = datetime.datetime.strptime(param_val, "%Y-%m-%d")
                except Exception as e:
                    pass

                if _dt is None:
                    raise Exception()
                else:
                    param_val = _dt

        except Exception as e:
            raise VldException("Parameter[{label}] conversion failure".format(label=param_label))

        rule_method = val.get("rule", None)

        if rule_method:
            rule_method(dict(label=param_label, value=param_val, message=val.get("message", "")))

        xparams[val.get("rename", "") or param_name] = param_val

    params_log.debug("xparams:%s", xparams)

    return xparams

