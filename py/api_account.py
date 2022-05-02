#!/usr/bin/python
# -*- coding: utf-8 -*-

# api.py: REST API for basic account related stuff: signup/login/logout
#
# 

from flask import request, session, g, jsonify

import db
import webutil
import account
from webutil import app, login_required, get_myself

from apis.user_apis import UserService
from public.vld_param import vld_params_encrypt, Validator
from public.http_tool import check_login_encrypt, not_check_login
from units.cryptoFunc import decode_base64

import logging
log = logging.getLogger("api")
###################################################CMS User####################################################
user_api = UserService()

@app.route('/user/login_register', methods=["POST", "GET"])
@not_check_login
def register_login(data):
    """
        登录注册接口
    :param data:
    :return:
    """
    params = vld_params_encrypt(
        data,
        {
            'versioncode:int':{'default': 1},
            'android_id: str': {'default': None},
            'login_type: int': {'default': 1},
            'login_token: str': {'default': None},
            'os': {'default': "0"},
            'iOS_key:str': {'default': None},
            'open_id:str': {'default': None},

        }
    )
    params['ip'] = request.headers.get('X-Forwarded-For', '')
    log.info("{}".format(params['ip']))
    return user_api.register_or_login_new(**params)

@app.route('/user/logout', methods=["POST", "GET"])
@not_check_login
def user_logout(data):
    """
        退出登录
    """
    params = vld_params_encrypt(
        data,
        {
            'uid: str': {'default': None, 'rule': Validator.required},
        })
    return user_api.user_logout(**params)

@app.route('/user/rtm/token', methods=['POST', "GET"])
@check_login_encrypt
def gen_rtm_token(data):
    """
        生成agora rtm token
    """
    params = vld_params_encrypt(
        data,
        {
            'uid:str': {'default': ''},
        })
    return user_api.gen_rtm_token(**params)

@app.route('/user/wechat/signature', methods=['POST', "GET"])
@not_check_login
def get_wechat_signature(data):
    """
        生成agora rtm token
    """
    params = vld_params_encrypt(
        data,
        {
            'appid:str': {'default': ''},
        })
    return user_api.get_wechat_signature(**params)

@app.route('/user/wechat/login', methods=['POST', "GET"])
@not_check_login
def wechat_login(data):
    """
        生成agora rtm token
    """
    params = vld_params_encrypt(
        data,
        {
            'code:str': {'default': ''},
            'versioncode:int': {'default': 1},
            'android_id: str': {'default': None},
            'iOS_key:str': {'default': None},
            'os:int':{'default':1},
        })
    params['ip'] = request.headers.get('X-Forwarded-For', '')
    return user_api.wechat_login(**params)

@app.route('/user/loginpwd', methods=['POST', "GET"])
@not_check_login
def user_loginpwd(data):
    """
        生成agora rtm token
    """
    params = vld_params_encrypt(
        data,
        {
            'username:str': {'default': ''},
            'password:str': {'default': ''},
            'versioncode:int': {'default': 1},
            'android_id: str': {'default': None},
            'iOS_key:str': {'default': None},
            'os:int':{'default':1},
        })
    params['ip'] = request.headers.get('X-Forwarded-For', '')
    return user_api.user_loginpwd(**params)

@app.route('/user/getuid', methods=['POST', "GET"])
@not_check_login
def user_getuid(data):
    """
        生成agora rtm token
    """
    params = vld_params_encrypt(
        data,
        {
            'versioncode:int': {'default': 1},
            'android_id: str': {'default': None},
            'iOS_key:str': {'default': None},
            'os:int':{'default':1},
        })
    params['ip'] = request.headers.get('X-Forwarded-For', '')
    return user_api.user_getuid(**params)


#更新用户信息信息
@app.route('/user/update_userinfo', methods=['POST', "GET"])
@check_login_encrypt
def update_userinfo(data):
    """
        生成agora rtm token
    """
    params = vld_params_encrypt(
        data,
        {
            'uid:str':{'default': None},
            'training_effect:int': {'default': 1},
            'training_method: int': {'default': 1},
            'training_interval:int': {'default': 1},
            'height:int':{'default':155},
            'weight:int': {'default': 50},
            'birthday:str': {'default': None},
            'gender:int': {'default': 1},
        })
    params['ip'] = request.headers.get('X-Forwarded-For', '')
    return user_api.update_userinfo(**params)

###############################################################################################################

@app.route('/api/login', methods = ['POST'])
def login():
    """Logs the user in with email+password.
       On success returns the user object,
       on error returns 400 and json with err-field."""

    input = request.json or {}
    email = input.get('email')
    password = input.get('password')

    if not email or not password:
        return webutil.warn_reply("Missing input")

    u = db.get_user_by_email(email)
    if not u or not account.check_password(u.password, password):
        # error
        return webutil.warn_reply("Invalid login credentials")
    else:
        # success
        account.build_session(u, is_permanent=input.get('remember', True))

        log.info("LOGIN OK agent={}".format(webutil.get_agent()))
        return jsonify(u), 200


@app.route('/api/signup', methods = ['POST'])
def signup():
    """Signs a new user to the service. On success returns the user object,
       on error returns 400 and json with err-field."""

    input = request.json or {}
    email  = input.get('email')
    password = input.get('password')
    fname  = input.get('fname')
    lname  = input.get('lname')
    company  = input.get('company')

    if not email or not password or not fname or not lname:
        return webutil.warn_reply("Invalid signup input")

    u = db.get_user_by_email(email)
    if u:
        msg = "Signup email taken: {}".format(email)
        return webutil.warn_reply(msg)

    err = account.check_password_validity(password)
    if err:
        return jsonify({"err":err}), 400

    # create new user
    u = db.User()
    u.email = email
    u.company = company
    u.first_name = fname
    u.last_name = lname
    u.password = account.hash_password(password)
    u.tags = []
    u.role = 'editor' # set default to what makes sense to your app
    u.save(force_insert=True)

    account.new_signup_steps(u)
    account.build_session(u, is_permanent=input.get('remember', True))

    log.info("SIGNUP OK agent={}".format(webutil.get_agent()))

    return jsonify(u), 201


@app.route('/api/logout', methods = ['POST'])
@login_required
def logout():
    """Logs out the user, clears the session."""
    session.clear()
    return jsonify({}), 200


@app.route('/api/me')
@login_required
def me():
    """Return info about me. Attach more data for real use."""

    me = get_myself()
    reply = {"me": me}

    return jsonify(reply), 200


@app.route('/api/users')
@login_required(role='superuser')
def users():
    """Search list of users. Only for superusers"""

    input = request.args or {}
    page = input.get('page')
    size = input.get('size')
    search = input.get('search')

    reply = db.query_users(page, size, search)

    return jsonify(reply), 200

