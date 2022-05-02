import json
import math
import pickle
import random
import uuid
import time
import requests

from public.api import ApiResult, DistributedLock, delete_api_cache_key

# from public.async_tools import len_queue, pop_queue, push_queue
from units import tools
from settings import errorCode, config#, kafka_topics
from models.sql_models import User
from units.redis_tools import redis_conn
from settings.evn_conf import es
from public import x_db
from models.sql_models import Session
from sqlalchemy import and_
import hashlib
from random import randrange

log = tools.getLogger("root")
device_ban_log = tools.getLogger("device_ban")
token_check_log = tools.getLogger("token_check_log")
uid_token_log = tools.getLogger("uid_token_log")
report_log = tools.getLogger("report_log")

class UserService(object):
    def register_or_login_new(self, os, login_type, ip, versioncode, iOS_key,android_id, open_id,login_token=''):
        result = ApiResult.get_inst()
        if not login_type:
            return result.error(errorCode.CODE_PARAMETER_ERR, msg="params error1")
        type = int(login_type)
        rid = 0
        uid = ""
        head = ""
        name = ""
        iscoach = 0
        sex=1
        country="CN"
        data = {}
        if type==1:#如果是微信登录，取微信后台验证这个的有效性
            #获取第一步的 code 后，请求以下链接获取 access_token：
           # hosts = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
           #     config.wechatAppId, config.wechatAppSecret, login_token)
          #  response = requests.get(url=hosts, timeout=10)
          #  log.info("wechat access url:{},response:{}".format(hosts, response.text))
         #   data = json.loads(response.text)
         #   log.info("data length:{}".format(len(data)))
           # if len(data)<=3:
          #      return result.error()
            access_token  = login_token
            openid = open_id
            #这里用openid及logintype去 user表里面查找信息
            #session = x_db.get_db_session()
            session = Session()
            token = ""
            ret =  session.query(User).filter(and_(User.logintype == login_type,User.thirduid==openid)).first()
            if not ret:##如果不存在，则记录没有，去调用微信的下一个接口
                hosts = 'https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}'.format(access_token, openid)
                response = requests.get(url=hosts, timeout=10)
                log.info("wechat get user info url:{},response:{}".format(hosts, response.text.encode('ISO-8859-1').decode("utf8")))
                userinfo = json.loads(response.text.encode('ISO-8859-1').decode("utf8"))
                if len(userinfo)<=3:
                    return result.error(code=errorCode.LOGIN_FAIL,msg="微信认证登录失败")
                head =userinfo["headimgurl"]
                name = userinfo["nickname"]
                sex = userinfo["sex"]
                country = userinfo["country"]
                log.info("test 124")
                uid = tools.get_uid();
                log.info("test 125")

                #赋值插入
                token = self._set_token_(uid, ip, iOS_key, android_id)
                log.info("test 126")
                user = User(uid=uid,name=name,head=head,gender=sex,logintype=login_type,thirduid=openid,country=country,android_id=android_id,os=os,iOS_key=iOS_key,training_effect=0,training_method=0,training_interval=0,height=0,weight=0)
                log.info("test 127")
                session.add(user)
                session.commit()
                rid =user.rid
            else:#存在了，获取head,name,rid,直接返回
                rid = ret.rid  #rid = ret.t_user_info.rid
                uid =  ret.uid
                head = ret.head
                name = ret.name
                iscoach = ret.iscoach
                token = self._set_token_(uid, ip, iOS_key, android_id)
        session.close()
        data["rid"] = rid
        data['token'] = token
        data['uid'] =   uid
        data['head'] = head
        data['name'] = name
        data['iscoach'] = iscoach
        return result.success(data=data)

    def _set_token_(self, uid, ip, ios_key, androidid):
        """
        生成token
        :param uid:
        :return:
        """
        real_token = str(uuid.uuid1()).replace("-", "")
        key = "get_uid_from_{}".format(real_token)
        redis_conn.set(key, uid, ex=7 * 24 * 3600)
        redis_conn.hset("uid_token", uid, real_token)
        return real_token


    def get_user_list(self, uid, start_page,page_size):
        result = ApiResult.get_inst()
        start = (start_page - 1) * page_size
        log.debug("start :%d",start)
        end_index = start_page*page_size
        log.debug("end_index :%d",end_index)
        return_list = list()
        user_obj = redis_conn.zrange('coach_status', start,end_index, desc=True, withscores=True)
        log.info("user_obj :{}".format(user_obj))
        total = redis_conn.zcard("coach_status")
        log.info("total :{}".format(total))
        session = Session()
        current_page = start_page
        coach_number =0

        end_index = start_page*page_size
        log.info("current_page :{},current_page:{},end_index:{}".format(start_page,page_size,end_index))
        if total <= end_index:
            end_index = total
        if user_obj:
            coach_number = len(user_obj)
            for one in user_obj:
                ret_data = dict()
                ret_data["status"] =0
                uid = one[0]
                status = int(one[1])
                if status==1:
                    ret_data["status"] =2
                elif status ==2:
                    ret_data["status"] =1
                else:
                    ret_data["status"] = status
                ret = session.query(User).filter(and_(User.iscoach == 1, User.uid == uid)).first()
                if ret:
                    ret_data["uid"] = ret.uid
                    ret_data["head"] = ret.head
                    ret_data["name"] = ret.name
                    ret_data["iscoach"] = ret.iscoach
                    ret_data["desc"]= ret.desc
                    return_list.append(ret_data.copy())
        session.close()
        return result.success(data={"coach": return_list, "total": total,"current_page":current_page,"coach_number":coach_number})


    def user_logout(self, uid):
        result = ApiResult.get_inst()
        session = Session()
        user_obj = session.query(User).filter(User.uid == uid).first()
        if user_obj.iscoach == 1:
            redis_conn.zadd("coach_status",  0,uid)
        session.close()
        return result.success()


    def gen_rtm_token(self, uid):
        result = ApiResult.get_inst()
        rtm_token = ""
        try:
            rtm_token = tools._gen_rtm_token(uid)
        except Exception as e:
            log.exception("gen rtm token error :{}".format(e))

        return result.success(data={"rtm_token": rtm_token})

    def get_wechat_signature(self,appid):
        result = ApiResult.get_inst()
        access_token=""
        #这里去redis里面查找有没有access_token，如果没有就要先获取access_token
        noncestr = str(uuid.uuid1()).replace("-", "")[0:6]
        scope="snsapi_base,snsapi_userinfo"
        timesmaple = int(time.time())
        access_info=""
        timestamp = timesmaple
        hosts = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(
            config.wechatAppId, config.wechatAppSecret)
        sdk_ticket=""
        ##先来获取 ticket
        redis_token = redis_conn.get("access_token")
        if not redis_token:
            response = requests.get(url=hosts, timeout=10)
            access_info = json.loads(response.text)
            access_token = access_info["access_token"]
            expires_in = access_info["expires_in"]
            expires_time = timesmaple + int(expires_in)
            token_value = access_token + "/" + str(expires_time)
            redis_conn.set("access_token", token_value)
        else:
            log.info("redis_token :{}".format(redis_token))
            item_value = str(redis_token,'utf-8')
            log.info("item_value :{},timesmaple:{}".format(item_value,timesmaple))
            item = item_value.split("/")
            access_token = item[0]
            if timesmaple >int(item[1]):
                response = requests.get(url=hosts, timeout=10)
                access_info = json.loads(response.text)
                access_token = access_info["access_token"]
                expires_in = access_info["expires_in"]
                expires_time = timesmaple + int(expires_in)
                token_value = access_token + "/" + str(expires_time)
                redis_conn.set("access_token", token_value)
        ticket=""
        ticket_redis = redis_conn.get("ticket")
        if not ticket_redis:
            hosts_ticket="https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=2".format(access_token)
            response = requests.get(url=hosts_ticket, timeout=10)
            ticket_info = json.loads(response.text)
            ticket = ticket_info["ticket"]
            expires_in = ticket_info["expires_in"]
            ticket_value=ticket+"/"+ str(timesmaple+int(expires_in))
            redis_conn.set("ticket",ticket_value)
        else:
            log.info("ticket_redis :{}".format(ticket_redis))
            item_value = str(ticket_redis,'utf-8')
            log.info("item_value :{}".format(item_value))
            item = item_value.split("/")
            log.info("item_value1:{},2:{}".format(item[0],item[1]))
            ticket = item[0]
            if timesmaple > int(item[1]):
                hosts_ticket = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=2".format(
                    access_token)
                response = requests.get(url=hosts_ticket, timeout=10)
                ticket_info = json.loads(response.text)
                ticket = ticket_info["ticket"]
                expires_in = ticket_info["expires_in"]
                ticket_value = ticket + "/" + str(timesmaple + int(expires_in))
                redis_conn.set("ticket", ticket_value)
        string1="appid={0}&noncestr={1}&sdk_ticket={2}&timestamp={3}".format(config.wechatAppId,noncestr,ticket,timesmaple)
        log.info("str_singturae:{}".format(string1))
        sha = hashlib.sha1(string1.encode('utf-8'))
        encrypts = sha.hexdigest()
        api_data={
                "appid":config.wechatAppId,
                "noncestr":noncestr,
                "scope":scope,
                "timestamp":timestamp,
                "signature":encrypts
        }
        return result.success(data=api_data)

    def wechat_login(self,code,ip,iOS_key,android_id,versioncode,os):
        result = ApiResult.get_inst()
        rid = 0
        uid = ""
        head = ""
        name = ""
        iscoach = 0
        sex=1
        country="CN"
        data = {}

        hosts = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
             config.wechatAppId, config.wechatAppSecret, code)
        response = requests.get(url=hosts, timeout=10)
        log.info("wechat access url:{},response:{}".format(hosts, response.text))
        data = json.loads(response.text)
        log.info("data length:{}".format(len(data)))
        if len(data)<=3:
            return result.error()
        access_token = data["access_token"]
        openid = data["openid"]
        session=Session()
        sex = 1
        birthday=""
        height=0
        weight = 0
        ret = session.query(User).filter(and_(User.logintype == 1, User.thirduid == openid)).first()
        if not ret:
            hosts = 'https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}'.format(access_token, openid)
            response = requests.get(url=hosts, timeout=10)
            log.info("wechat get user info url:{},response:{}".format(hosts, response.text.encode('ISO-8859-1').decode(
                "utf8")))
            userinfo = json.loads(response.text.encode('ISO-8859-1').decode("utf8"))

            if len(userinfo) <= 3:
                return result.error(code=errorCode.LOGIN_FAIL, msg="微信认证登录失败")
            head = userinfo["headimgurl"]
            log.info("wechat get user info head:{}".format(head))
            name = userinfo["nickname"]
            log.info("wechat get user info name:{}".format(name))
            sex = userinfo["sex"]
            log.info("wechat get user info sex:{}".format(sex))
            country = userinfo["country"]
            log.info("wechat get user info country:{}".format(country))
            uid = tools.get_uid();
            login_type = 1
            log.info("test 124")
            # 赋值插入
            token = self._set_token_(uid, ip, iOS_key, android_id)
            log.info("test 125")
            user = User(uid=uid, name=name, head=head, gender=sex, logintype=login_type, thirduid=openid,
                        country=country, android_id=android_id, os=os, iOS_key=iOS_key,training_effect=0,training_method=0,training_interval=0,height=0,weight=0)
            log.info("test 126")
            session.add(user)
            log.info("test 128")
            session.commit()
            log.info("test 127")

            rid = user.rid
        else:
            rid = ret.rid  # rid = ret.t_user_info.rid
            uid = ret.uid
            head = ret.head
            name = ret.name
            iscoach = ret.iscoach
            sex = ret.gender
            birthday = ret.birthday
            height = ret.height
            weight = ret.weight
            token = self._set_token_(uid, ip, iOS_key, android_id)
        session.close()
        api_data={}
        api_data["rid"] = rid
        api_data['token'] = token
        api_data['uid'] =   uid
        api_data['head'] = head
        api_data['name'] = name
        api_data['iscoach'] = iscoach
        api_data['sex'] = sex
        api_data['birthday'] = birthday
        api_data['height'] = height
        api_data['weight'] = weight
        return result.success(data=api_data)

    def user_loginpwd(self,username,password,ip,iOS_key,android_id,versioncode,os):
        result = ApiResult.get_inst()
        rid = 0
        uid = ""
        head = "https://api.gearinter.com/static/images/teacher/15.png"
        name = ""
        iscoach = 0
        sex = 1
        country = "CN"
        data = {}

        ##这里来检查用户名和密码
        if username!=config.username:
            return result.error(code=errorCode.LOGIN_FAIL,msg="login fail")
        if password !=config.password:
            return result.error(code=errorCode.LOGIN_FAIL,msg="login fail")
        uid = config.uid
        token = self._set_token_(uid, ip, iOS_key, android_id)
        rid = config.rid
        name = "Cami"
        api_data = {}
        api_data["rid"] = rid
        api_data['token'] = token
        api_data['uid'] = uid
        api_data['head'] = head
        api_data['name'] = name
        return result.success(data=api_data)

    def user_getuid(self,ip,iOS_key,android_id,versioncode,os):
        result = ApiResult.get_inst()
        rid = 0
        uid = ""
        head = ""
        name = ""
        iscoach = 0
        data = {}
        aid={}
       # if config.andorid_to_uid[android_id]:
       #     uid = config.andorid_to_uid[android_id]
       # else:
       #     uid = config.y_uid
        random_index = randrange(0, len(config.uid_list))
        uid =str(config.uid_list[random_index])
        token = self._set_token_(uid, ip, iOS_key, android_id)
        session = Session()
        user_obj = session.query(User).filter(User.uid == uid).first()
        rid = user_obj.rid
        name = "firenow"
        api_data = {}
        api_data["rid"] = rid
        api_data['token'] = token
        api_data['uid'] = uid
        api_data['head'] = head
        api_data['name'] = name
        if not config.user_to_achor[uid]:
            api_data['aid'] =config.uid
        else:
            api_data['aid'] = config.user_to_achor[uid]
        session.close()
        return result.success(data=api_data)

    def update_userinfo(self,ip,training_effect,training_method,training_interval,height,weight,birthday,gender,uid):
        result = ApiResult.get_inst()
        session = Session()
        user_obj = session.query(User).filter(User.uid == uid).first()
        if user_obj:
            user_obj.gender = gender
            user_obj.birthday = birthday
            user_obj.training_effect = training_effect
            user_obj.training_method = training_method
            user_obj.training_interval = training_interval
            user_obj.height = height
            user_obj.weight = weight
        session.commit()
        session.close()
        return result.success()

    # def get_banners(self,ip,uid):
    #     result = ApiResult.get_inst()
    #     return_list = list()
    #     session = Session()
    #     banners_obj = session.query(Banner).filter(or_(Banner.status == 1)).all()
    #     banners_number = len(banners_obj)
    #     if banners_obj:
    #         for one in banners_obj:
    #             ret_data = dict()
    #             ret_data["type"] = str(one.type)
    #             ret_data["actual_id"] = one.actual_id
    #             ret_data["banner_img"] = one.banner_img.strip()
    #             return_list.append(ret_data.copy())
    #     session.close()
    #     return result.success(data={"banners": return_list, "total": banners_number})

    # def get_dict(self,uid,type,ip,language):
    #     result = ApiResult.get_inst()
    #     return_list = list()
    #     session = Session()
    #     dict_obj = session.query(Dict).filter(and_(Dict.type == type,Dict.language==language)).all()
    #     dict_number = len(dict_obj)
    #     if dict_obj:
    #         for one in dict_obj:
    #             ret_data = dict()
    #             ret_data["value"] = str(one.value)
    #             ret_data["id"] = one.id
    #             return_list.append(ret_data.copy())
    #     session.close()
    #     return result.success(data={"dict": return_list, "total": dict_number})

    # def get_live_course(self,uid,ip,date):
    #     result = ApiResult.get_inst()
    #     return_list = list()
    #     session = Session()
    #     dict_obj = session.query(Live_Info).filter(Live_Info.live_date == date).all()
    #     total_num=0
    #     local_time = int(time.time())
    #     if dict_obj:
    #         for one in dict_obj:
    #             ret_data = dict()
    #             start_time = int(one.start_time)
    #             end_time = int(one.end_time)
    #             status = 0
    #             if local_time> end_time:
    #                 continue
    #             if  local_time>start_time and local_time<end_time:
    #                 status = 1
    #             ret_data["live_status"] = status
    #             ret_data["live_id"] = one.live_id
    #             ret_data["live_name"] = one.live_name
    #             ret_data["coach_id"] = one.uid
    #             ret_data["live_banner"] = one.live_banner
    #             ret_data["live_date"] = one.live_date
    #             time_local = time.localtime(start_time)
    #             ret_data["live_start"] = time.strftim("%H:%M",time_local)
    #             labe = one.live_label
    #             lab_arry = labe.split(",")
    #             lab_list = list()
    #             for itm in lab_arry:
    #                 lab_obj = session.query(Dict).filter(Dict.id== itm).first()
    #                 lab_value = lab_obj.value
    #                 lab_list.append(lab_value)
    #             ret_data["live_labe"] = lab_list
    #             coach =  session.query(User).filter(User.uid== one.uid).first()
    #             ret_data["coache_head"] =coach.head
    #             ret_data["coache_name"] = coach.name
    #             total_num = total_num+1
    #             return_list.append(ret_data.copy())
    #     session.close()
    #     return result.success(data={"live_course": return_list, "total": total_num})


    # def get_live_course_detail(self,ip,uid,live_id):
    #     result = ApiResult.get_inst()
    #     return_list = list()
    #     session = Session()
    #     live_info = session.query(Live_Info).filter(Live_Info.live_id == int(live_id)).first()
    #     data = {}
    #     if live_info:
    #         data["live_id"] = live_info.live_id
    #         data["live_name"] = live_info.live_name
    #         data["coach_id"] = live_info.uid
    #         coach = session.query(User).filter(User.uid == live_info.uid).first()
    #         data["coache_head"] = coach.head
    #         data["coache_name"] = coach.name
    #         data["live_banner"] = live_info.live_banner
    #         live_monthy =  live_info.live_date[0:4]
    #         live_date =  live_info.live_date[4:2]
    #         live_time=live_monthy+"月"+live_date
    #         data["live_date"] = live_time
    #         time_local = time.localtime(int(live_info.start_time))
    #         ret_data["live_start"] = time.strftim("%H:%M", time.localtime(int(live_info.start_time)))
    #         data["live_end"] =  time.strftim("%H:%M", time.localtime(int(live_info.end_time)))
    #         data["live_desc"] = live_info.live_desc
    #         data["for_people"] = live_info.for_people
    #         data["taboo_people"] = live_info.taboo_people
    #         data["training_preparation"] = live_info.training_preparation
    #         data["body_response"] = live_info.body_response
    #         data["live_duration"] = int(live_info.live_duration)
    #         data["burn_calories"] = int(live_info.burn_calories)
    #         labe = live_info.live_label
    #         lab_arry = labe.split(",")
    #         lab_list = list()
    #         for itm in lab_arry:
    #             lab_obj = session.query(Dict).filter(Dict.id == itm).first()
    #             lab_value = lab_obj.value
    #             lab_list.append(lab_value)
    #         data["live_labe"] = live_labe
    #     follow = session.query(Follow).filter((and_(Follow.uid == uid, Follow.aid == live_info.uid))).first()
    #     if follow:
    #         data["is_follow"] = 1
    #     else:
    #         data["is_follow"] = 1
    #     session.close()
    #     return result.success(data=data)

    # def do_user_follow(self,ip,uid,aid,optype):
    #     result = ApiResult.get_inst()
    #     session = Session()
    #     ctime = int(time.time())
    #     if optype==1: ##关注
    #         follow = Follow(uid=uid, aid=aid, ctime = ctime)
    #         session.add(follow)
    #     if optype==2:##取消关注
    #         session.query(Follow).filter((and_(Follow.uid == uid, Follow.aid == aid))).delete()
    #     session.commit()
    #     session.close()
    #     return  result.success()

    # def get_my_follow(self,ip,uid):
    #     result = ApiResult.get_inst()
    #     session = Session()
    #     ctime = int(time.time())
    #     follow_obj = session.query(Follow).filter((Follow.uid == uid)).all()
    #     total =0
    #     return_list = list()
    #     if follow_obj:
    #         total = len(follow_obj)
    #         for one in follow_obj:
    #             ret_data = dict()
    #             coach =  session.query(User).filter(User.uid== one.aid).first()
    #             if  coach:
    #                 ret_data["name"] = coach.name
    #                 ret_data["head"] = coach.head
    #                 ret_data["aid"] = one.aid
    #                 lab_list = list()
    #                 ret_data["labe"] = lab_list
    #                 return_list.append(ret_data.copy())
    #     session.commit()
    #     session.close()
    #     return result.success(data={"follows": return_list, "total": total})

    # def get_coachs(self,ip,uid,categorys,language):
    #     result = ApiResult.get_inst()
    #     session = Session()
    #     category_list = list()
    #     return_list = list()
    #     if categorys=="0":
    #         dict_obj  =  session.query(Dict).filter(Dict.type==4).all()
    #         for one in dict_obj:
    #             category_list.append(one.id)
    #     else:
    #         category_arry= categorys.split(",")
    #         for item in category_arry:
    #             category_list.append(item)
    #             ##Coach.id.in_(my_list_of_ids)
    #   #  coach_obj =  session.query(Coach).all()
    #     coach_obj = session.query(Coach).filter(or_(Coach.coach_type == 1, Coach.coach_type == 0)).all()
    #     total = 0
    #     if coach_obj:
    #         for item_coach in coach_obj:
    #             for category in category_list:
    #                 if item_coach.language !=language:
    #                     continue
    #                 if item_coach.training_category.find(str(category)) !=-1:##找到记录
    #                     ret_data = dict()
    #                     coach = session.query(User).filter(User.uid == item_coach.uid).first()
    #                     ret_data["name"] = coach.name
    #                     ret_data["banner"] = item_coach.banner_img
    #                     ret_data["coach_id"] =item_coach.uid
    #                     ret_data["coach_type"] = item_coach.coach_type
    #                     labe = item_coach.custom_label
    #                     lab_arry = labe.split(",")
    #                     lab_list = list()
    #                     for itm in lab_arry:
    #                         lab_list.append(itm)
    #                     ret_data["labe"] = lab_list
    #                     ret_data["total_trainees"] =item_coach.total_trainees
    #                     return_list.append(ret_data.copy())
    #                     total = total+1
    #                     break
    #     session.close()
    #     return result.success(data={"coachs": return_list, "total": total})

    # def get_coach_info(self,ip,uid,coach_id):
    #     result = ApiResult.get_inst()
    #     session = Session()
    #     data = {}
    #     coach_obj = session.query(Coach).filter(Coach.uid == coach_id).first()
    #     if coach_obj:
    #         user_info = session.query(User).filter(User.uid == coach_id).first()
    #         if user_info:
    #             data["name"] = user_info.name
    #             data["head"] = coach_obj.coach_head_img
    #         data["banner"] = coach_obj.banner_img
    #         data["desc"] = coach_obj.fdesc
    #         data["total_trainees"] = coach_obj.total_trainees
    #         data["is_follow"] = 0
    #        # date["head_img"] = coach_obj.coach_head_img
    #     session.close()
    #     return result.success(data=data)

    # def get_coach_courses(self,ip,uid,coach_uid,language):
    #     result = ApiResult.get_inst()
    #     return_list = list()
    #     session = Session()
    #     Course_obj = session.query(Course).filter(and_(Course.uid == coach_uid,Course.language==language)).all()
    #     total_num = 0
    #     local_time = int(time.time())
    #     if Course_obj:
    #         for one in Course_obj:
    #             ret_data = dict()
    #             ret_data["course_id"] = one.course_id
    #             ret_data["course_name"] = one.course_name
    #             ret_data["total_trainees"] = one.total_trainees
    #             ret_data["img_url"] = one.course_img
    #             labe = one.label
    #             lab_arry = labe.split(",")
    #             lab_list = list()
    #             for itm in lab_arry:
    #                 lab_list.append(itm)
    #             ret_data["labe"] = lab_list
    #             total_num = total_num + 1
    #             return_list.append(ret_data.copy())
    #     session.close()
    #     return result.success(data={"courses": return_list, "total": total_num})

    # def get_medal_list(self,ip,uid):
    #     result = ApiResult.get_inst()
    #     return_list = list()
    #     session = Session()
    #     Medal_obj = session.query(Medal_list).filter(Medal_list.uid == uid).all()
    #     total_num = 0
    #     local_time = int(time.time())
    #     if Medal_obj:
    #         for one in Medal_obj:
    #             ret_data = dict()
    #             medal_info = session.query(Medal_info).filter(Medal_info.medal_id == one.medal_id).first()
    #             if medal_info:
    #                 dict_info = session.query(Dict).filter(Dict.id == medal_info.medal_type).first()
    #                 ret_data["medal_type"] = dict_info.value
    #                 ret_data["name"] = medal_info.medal_name
    #                 ret_data["medal_url"] = medal_info.medal_url
    #                 ret_data["medal_desc"] = medal_info.medal_name
    #                 total_num = total_num + 1
    #                 return_list.append(ret_data.copy())
    #     session.close()
    #     return result.success(data={"medals": return_list, "total": total_num})

    # def get_certificate_list(self,ip,uid):
    #     result = ApiResult.get_inst()
    #     return_list = list()
    #     session = Session()
    #     cer_obj = session.query(Certificate_list).filter(Certificate_list.uid == uid).all()
    #     total_num = 0
    #     local_time = int(time.time())
    #     if cer_obj:
    #         for one in cer_obj:
    #             ret_data = dict()
    #             cer_info = session.query(Certificate_info).filter(Certificate_info == one.certificate_id).first()
    #             #if cer_info:
    #             #    total_num = total_num + 1
    #             #    return_list.append(ret_data.copy())
    #     session.close()
    #     return result.success(data={"certificates": return_list, "total": total_num})


    # def training_report(self,ip,uid,date,class_type,class_id,training_time,burn_calories):
    #     result = ApiResult.get_inst()
    #     return result.success()

    # def get_course_list(self,ip,uid,categorys,language):
    #     result = ApiResult.get_inst()
    #     return_list=list()
    #     session = Session()
    #     category_list = list()
    #     log.info("get_course_list categorys:{},len:{}".format(categorys,len(categorys)))
    #     if categorys == "0":
    #         dict_obj = session.query(Dict).filter(Dict.type == 4).all()
    #         for one in dict_obj:
    #             category_list.append(one.id)
    #     else:
    #         category_arry = categorys.split(",")
    #         for item in category_arry:
    #             category_list.append(item)
    #             ##Coach.id.in_(my_list_of_ids)
    #     course_obj = session.query(Course).filter(Course.language==language).all()
    #     total_num = 0
    #     if course_obj:
    #         for item_course in course_obj:
    #             for category in category_list:
    #                 if item_course.training_category.find(str(category)) != -1:  ##找到记录
    #                     ret_data = dict()
    #                     ret_data["course_id"] = item_course.course_id
    #                     ret_data["course_name"] = item_course.course_name
    #                     ret_data["total_trainees"] = item_course.total_trainees
    #                     ret_data["img_url"] = item_course.course_img
    #                     ret_data["course_type"] = item_course.course_type
    #                     labe = item_course.label
    #                     lab_arry = labe.split(",")
    #                     lab_list = list()
    #                     for itm in lab_arry:
    #                         lab_list.append(itm)
    #                     ret_data["labe"] = lab_list
    #                     return_list.append(ret_data.copy())
    #                     total_num = total_num + 1
    #                     break
    #     session.close()
    #     return result.success(data={"courses": return_list, "total": total_num})

    # def get_course_info(self,ip,uid,course_id,language):
    #     result = ApiResult.get_inst()
    #     session = Session()
    #     Course_obj = session.query(Course).filter(and_(Course.course_id == course_id,Course.language==language)).first()
    #     local_time = int(time.time())
    #     total_num = 0
    #     if Course_obj:
    #         ret_data = dict()
    #         user_info  = session.query(User).filter(User.uid == Course_obj.uid).first()
    #         ret_data["coach_name"] = user_info.name
    #         ret_data["coach_head"] = user_info.head
    #         ret_data["coach_uid"] = Course_obj.uid

    #         ret_data["total_trainees"] = Course_obj.total_trainees
    #         ret_data["course_banner"] = Course_obj.course_img
    #         ret_data["course_desc"] = Course_obj.fdesc
    #         ret_data["course_name"] = Course_obj.course_name
    #         ret_data["course_id"] = course_id
    #         ret_data["course_type"] = Course_obj.course_type

    #         follow = session.query(Follow).filter((and_(Follow.uid == uid, Follow.aid == Course_obj.uid))).first()
    #         if follow:
    #             ret_data["is_follow"] = 1
    #         else:
    #             ret_data["is_follow"] = 1

    #         ret_data["burn_calories"] = Course_obj.burn_calories
    #         ret_data["course_duration"] = Course_obj.course_duration
    #         ret_data["total_class"] = Course_obj.total_course
    #         labe = Course_obj.label
    #         lab_arry = labe.split(",")
    #         lab_list = list()
    #         for itm in lab_arry:
    #             lab_list.append(itm)
    #         ret_data["labe"] = lab_list
    #         class_obj = session.query(Course_class).filter(and_(Course_class.course_id == course_id,Course_class.language==language)).all()
    #         return_list =  list()
    #         if class_obj:
    #             for one in class_obj:
    #                 class_data = dict()
    #                 class_data["class_id"] = one.class_id
    #                 class_data["class_name"] = one.class_name
    #                 class_data["class_img"] = one.class_img
    #                 class_data["class_duration"] = one.class_duration
    #                 class_data["burn_calories"] = one.burn_calories
    #                 class_data["content_url"] = one.content_url
    #                 class_data["is_finish"] = 0
    #                 class_data["class_type"] = 3
    #                 labe = one.custom_label
    #                 lab_arry = labe.split(",")
    #                 lab_list = list()
    #                 for itm in lab_arry:
    #                     lab_list.append(itm)
    #                 class_data["labe"] = lab_list
    #                 total_num = total_num + 1
    #                 return_list.append(class_data.copy())
    #         ret_data["class_list"] = return_list
    #     session.close()
    #     return result.success(data=ret_data)

    # def add_training_plan(self,ip,uid,course_id,class_id,class_type,plain_date):
    #     result = ApiResult.get_inst()
    #     session = Session()
    #     Training = Training_plan(uid=uid, class_id=class_id, class_type=class_type, training_date=plain_date)
    #     session.add(Training)
    #     session.commit()
    #     return result.success()

    # def check_update(self,ip,versioncode,android_id,iOS_key,os):
    #     result = ApiResult.get_inst()
    #     log.info("check_update versioncode:{},android_id:{},iOS_key:{}".format(versioncode,android_id,iOS_key))
    #     api_data = {}
    #     api_data["versioncode"] = 3
    #     api_data['is_forced'] = 0
    #     if versioncode<2:
    #         api_data['is_forced'] = 1 #0,普通升级，1强制升级
    #     api_data['url'] = "http://8.134.63.224/FN2C_20211207_1030_1.0.2.apk"
    #     return result.success(data=api_data)

    # def get_personal_coachs(self,ip,uid,language):
    #     result = ApiResult.get_inst()
    #     session = Session()
    #     return_list = list()
    #     coach_obj = session.query(Coach).filter(or_(Coach.coach_type == 1, Coach.coach_type == 2)).all()
    #     total = 0
    #     if coach_obj:
    #         for item_coach in coach_obj:
    #             ret_data = dict()
    #             if item_coach.language != language:
    #                 continue
    #             coach = session.query(User).filter(User.uid == item_coach.uid).first()
    #             ret_data["name"] = coach.name
    #             ret_data["banner"] = item_coach.banner_img
    #             ret_data["coach_id"] = item_coach.uid
    #             ret_data["coach_type"] = item_coach.coach_type
    #             labe = item_coach.custom_label
    #             lab_arry = labe.split(",")
    #             lab_list = list()
    #             for itm in lab_arry:
    #                 lab_list.append(itm)
    #             ret_data["labe"] = lab_list
    #             ret_data["total_trainees"] = item_coach.total_trainees
    #             return_list.append(ret_data.copy())
    #             total = total + 1
    #     session.close()
    #     return result.success(data={"coachs": return_list, "total": total})


    # def apply_phone(self, uid, aid):
        # result = ApiResult.get_inst()
        # log.info("uid :{},aid:{},y_uid:{}".format(uid,aid,config.y_uid))
        # if str(uid)==str(config.y_uid):
        #     log.info("uid :{},aid:{},y_uid:{}".format(uid, aid, config.y_uid))
        #     aid = config.uid
        #     uid = str(config.y_uid)
        # if not redis_conn.sismember("coach_list",aid):
        #     log.info("aid data:{}".format(aid))
        #     return result.error(msg="user not exist")
        # #查目标用户的状态
        # log.info("aid data:{}".format(aid))

        # status = int(redis_conn.zscore("coach_status",aid))
        # if status == 1:
        #     code = errorCode.CODE_USER_BUSY
        #     return result.error(msg="用户忙线")

        # #如果状态没有问题，则入库
        # phone_data = Phone_histroy(uid=uid,aid=aid,ctime = int(time.time()),status = 0)
        # session = Session()
        # session.add(phone_data)
        # session.commit()
        # phone_id = phone_data.id
        # uid_user={}
        # aid_user={}
        # uid_user = session.query(User).filter(User.uid == uid).first()
        # log.info("uid_user data:{}".format(uid_user))
        # log.info("uid_user rid:{},uid:{},r_uid:{}".format(uid_user.rid,uid_user.uid,uid))

        # aid_user =  session.query(User).filter(User.uid == str(aid)).first()
        # data = {
        #     "uid": [aid],
        #     "topic": kafka_topics.APPLY_CALL,
        #     "send_data": {
        #         "uid": uid,
        #         "aid": aid,
        #         "head": uid_user.head,
        #         "name": uid_user.name,
        #         "phone_id": str(phone_id),
        #         "agora_id": aid_user.rid,
        #         "agora_token": tools.gen_agora_token(str(phone_id), aid_user.rid)
        #     }
        # }
        # log.info("apply_phone  kafka producer begin")
        # tools.gen_kafka_producer(topic=kafka_topics.ONCALL, data=data)
        # log.info("apply_phone  kafka producer end")

        # api_data = {
        #     "head": aid_user.head,
        #     "name": aid_user.name,
        #     "phone_id": str(phone_id),
        #     "aid": aid,
        #     "agora_id": uid_user.rid,
        #     "agora_token": tools.gen_agora_token(str(phone_id),uid_user.rid)
        # }
        # session.close()
        # return result.success(data=api_data)

    # def close_phone(self,uid,aid,phone_id):
    #     result = ApiResult.get_inst()
    #     session =Session()
    #     phone_history = session.query(Phone_histroy).filter(Phone_histroy.id== int(phone_id)).first()
    #     if redis_conn.sismember("coach_list", uid):
    #         redis_conn.zadd("coach_status", 2,uid)
    #     if redis_conn.sismember("coach_list", aid):
    #         redis_conn.zadd("coach_status", 2,aid)
    #     if not phone_history:
    #         session.close()
    #         return result.error(code=errorCode.CODE_PARAMETER_ERR,msg="参数错误")

    #     api_data = {}
    #     msg = ""

    #     if phone_history.status == 0: ##未接通
    #         phone_history.end_time = int(time.time())
    #         phone_history.hang_up = uid
    #         msg = "通话取消"
    #         api_data = {
    #             "phone_id": str(phone_id),
    #             "date":phone_history.end_time,
    #             "minutes": 0

    #         }
    #         data = {
    #             "uid": [phone_history.uid, phone_history.aid],
    #             "topic": kafka_topics.CLOSE_PHONE,
    #             "send_data": {
    #                 "uid": phone_history.uid,
    #                 "aid": phone_history.aid,
    #                 "phone_id": phone_id,
    #                 "minutes": 0
    #             }
    #         }
    #         log.info("close data:{}".format(data))

    #         tools.gen_kafka_producer(topic=kafka_topics.ONCALL, data=data)
    #     #首先查找通话历史表，看记录是否在
    #     else:
    #         msg = "通话结束"
    #         phone_history.end_time = int(time.time())
    #         phone_history.hang_up = uid
    #         phone_history.status=3
    #         minutes = int(time.time()) - phone_history.start_time
    #         api_data = {
    #             "phone_id": str(phone_id),
    #             "date": phone_history.end_time,
    #             "minutes": minutes
    #         }
    #         data = {
    #             "uid": [phone_history.uid, phone_history.aid],
    #             "topic": kafka_topics.CLOSE_PHONE,
    #             "send_data": {
    #                 "uid": phone_history.uid,
    #                 "aid": phone_history.aid,
    #                 "phone_id": phone_id,
    #                 "minutes": minutes
    #             }
    #         }
    #         log.info("close data:{}".format(data))

    #         tools.gen_kafka_producer(topic=kafka_topics.ONCALL, data=data)

    #     session.commit()
    #     session.close()
    #     return result.success(msg = msg,data = api_data)

    # def operate_phone(self,uid,phone_id,opt):
    #     result = ApiResult.get_inst()
    #     session = Session()
    #     phone_history = session.query(Phone_histroy).filter(Phone_histroy.id==int(phone_id)).first()
    #     log.info("operate_phone phone_id :{},opt:{},phone_history{}".format(phone_id,opt,phone_history))
    #     if not phone_history:
    #         session.close()
    #         return result.error(code=errorCode.CODE_PARAMETER_ERR, msg="参数错误")
    #     user_obj = session.query(User).filter(User.uid ==str(phone_history.uid) ).first()
    #     data={}
    #     if opt==1:
    #         data = {
    #             "uid": [phone_history.uid, phone_history.aid],
    #             "topic": kafka_topics.CONNECT_CALL,
    #             "send_data": {
    #                 "uid": uid,
    #                 "head": user_obj.head,
    #                 "phone_id": str(phone_id),
    #                 "name":user_obj.name
    #             }
    #         }
    #         phone_history.status = 1
    #         phone_history.start_time = int(time.time())
    #         #if  redis_conn.sismember("coach_list", uid) and uid !="4474277787314688001":
    #         #    redis_conn.zadd("coach_status", 1,uid)

    #     elif opt==2:
    #         phone_history.status = 2
    #         # phone_obj.aid = uid
    #         phone_history.end_time = int(time.time())
    #         phone_history.hang_up = uid
    #         data = {
    #             "uid": [phone_history.uid, phone_history.aid],
    #             "topic": kafka_topics.REJECT_CALL,
    #             "send_data": {
    #                 "uid": uid,
    #                 "head": user_obj.head,
    #                 "phone_id": str(phone_id),
    #                 "name":user_obj.name
    #             }
    #         }
    #     tools.gen_kafka_producer(topic=kafka_topics.ONCALL, data=data)
    #     session.commit()
    #     session.close()
    #     return  result.success()

    # def create_course(self,uid,course_name,course_desc):
    #     result = ApiResult.get_inst()
    #     session = Session()
    #     user_obj = session.query(User).filter(User.uid ==uid ).first()
    #     course_data =Course(uid=uid,roomname=course_name,roomdes=course_desc,roomhead=user_obj.head,ctime=int(time.time()))
    #     session.add(course_data)
    #     session.commit()
    #     course_id = str(course_data.id)
    #     data = {
    #         "course_id":course_id,
    #         "owner_uid":uid,
    #         "name":course_name,
    #         "head":user_obj.head,
    #         "desc":course_desc
    #     }
    #     session.close()
    #     return result.success(data = data)

    # def course_enter(self,uid,course_id):
    #     result = ApiResult.get_inst()
    #     #房间内用户数加1
    #     redis_key = "room_" + str(course_id)
    #     redis_conn.incr(redis_key)
    #     session = Session()
    #     course_obj = session.query(Course).filter(Course.id ==int(course_id)).first()
    #     user_obj = session.query(User).filter(User.uid == uid).first()
    #     owner_obj = session.query(User).filter(User.uid == course_obj.uid).first()

    #     if user_obj.iscoach == 1:
    #         redis_conn.zadd("coach_status", 1,uid)
    #     if not course_obj:
    #         msg="参数错误"
    #         session.close()
    #         result.error(code = errorCode.CODE_PARAMETER_ERR,msg=msg)
    #     if uid == course_obj.uid:
    #         course_obj.status = 1
    #         session.commit()
    #     total = int(redis_conn.get(redis_key))
    #     agora_token = tools.gen_agora_token(str(course_id),str(user_obj.rid))
    #     api_data = {
    #         "agora_token": agora_token,
	#         "agora_id": user_obj.rid,
	#         "owner_uid": course_obj.uid,
    #         "owner_agora_id":owner_obj.rid,
	#         "total": total,
	#         "course_id": str(course_id),
    #         "head":course_obj.roomhead,
    #         "name":course_obj.roomname,
    #         "desc":course_obj.roomdes
    #     }
    #     session.close()
    #     return result.success(data=api_data)

    # def enter_course(self,uid,course_id):
    #     result = ApiResult.get_inst()
    #     redis_key = "room_" + str(course_id)
    #     total = int(redis_conn.get(redis_key))
    #     session = Session()
    #     user_obj = session.query(User).filter(User.uid == uid).first()
    #     data = {
    #         "topic": kafka_topics.ENTER_ROOM,
    #         "send_data": {
    #             "uid": str(uid),
    #             "head": user_obj.head,
    #             "course_id": str(course_id),
    #             "name": user_obj.name,
    #             "total": total
    #         }
    #     }
    #     tools.gen_kafka_producer(topic=kafka_topics.ONCALL, data=data)
    #     session.close()
    #     return result.success()

    # def course_leave(self, uid, course_id):
    #     result = ApiResult.get_inst()
    #     redis_key = "room_" + str(course_id)
    #     redis_conn.decr(redis_key)
    #     log.info("course_leave total:{}".format(redis_conn.get(redis_key)))
    #     session =Session()
    #     course_obj = session.query(Course).filter(Course.id ==int(course_id)).first()
    #     user_obj = session.query(User).filter(User.uid == uid).first()
    #     total =  int(redis_conn.get(redis_key))
    #     if total<0:
    #         total = 0
    #         redis_conn.set(redis_key,0)
    #     if user_obj.iscoach == 1:
    #         redis_conn.zadd("coach_status", 2,uid)
    #     if uid == course_obj.uid:
    #         course_obj.status=2
    #         session.commit()
    #     data = {
    #         "topic": kafka_topics.LEAVE_ROOM,
    #         "send_data": {
    #             "uid": str(uid),
    #             "head": user_obj.head,
    #             "course_id": str(course_id),
    #             "name": user_obj.name,
    #             "total": total
    #         }
    #     }
    #     tools.gen_kafka_producer(topic=kafka_topics.ONCALL, data=data)
    #     session.close()
    #     return result.success()

    # def course_sendmsg(self,uid,course_id,message):
        # result = ApiResult.get_inst()
        # session = Session()
        # user_obj = session.query(User).filter(User.uid == uid).first()
        # data = {
        #     "topic": kafka_topics.SEND_MSG,
        #     "send_data": {
        #         "uid": str(uid),
        #         "head": user_obj.head,
        #         "course_id": str(course_id),
        #         "name": user_obj.name,
        #         "message": message
        #     }
        # }
        # tools.gen_kafka_producer(topic=kafka_topics.ONCALL, data=data)
        # return result.success()


# def get_country_code(self, os, ip):
#     result = ApiResult.get_inst()
#     if not ip:
#         return result.success(data={"country": "AE"})
#     country_code = parse_ip_code(ip)
#     if not country_code:
#         return result.success(data={"country": "AE"})
#     else:
#         tail_country = config.IP_MAP_COUNTRY.get(country_code, "AE")
#         total_country = country_code + "_" + tail_country
#         return result.success(data={"country": total_country})

