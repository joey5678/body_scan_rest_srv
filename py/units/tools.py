import time
import datetime
import uuid

# from jo_user.models.mongo_models import Follow, Fans, Friend, BadgeSource
from models.mongo_models import Gift, Follow, User
from settings import log_conf
from units.redis_tools import redis_conn

from settings import config
from settings.evn_conf import KAFKA_ADDRESS
from units.RtmTokenBuilder import RtmTokenBuilder, Role_Rtm_User
from units.RtcTokenBuilder import RtcTokenBuilder, Role_Publisher

import json
from functools import wraps
from flask import make_response, request
# import snowflake.client
# from kafka import KafkaProducer

def getLogger(name="root"):
    import logging.config
    logging.config.dictConfig(log_conf.LOGGING)
    return logging.getLogger(name=name)


def get_ranking_user_send_top(times):
    return "ranking_top_send_user_{}".format(times)


def get_ranking_user_rec_top(times):
    return "ranking_top_rec_user_{}".format(times)


def get_room_id_by_uid(uid):
    return 'r:{}'.format(uid)


def check_name(name):
    """
    校验用户名称
    :return:
    """
    import re
    rr = re.compile(r'\w*vip\w*')
    if rr.findall(name):
        return False
    return True


def detect_safe_search_uri(uri, client):
    """Detects unsafe features in the file located in Google Cloud Storage or
    on the Web."""
    from google.cloud import vision
    response = client.annotate_image({
        'image': {'source': {'image_uri': uri}},
        'features': [{'type': vision.enums.Feature.Type.SAFE_SEARCH_DETECTION}],
    })

    safe = response.safe_search_annotation
    return (safe.adult, safe.medical, safe.spoof, safe.violence)


def get_gift_info(gid):
    ret = dict()
    gift_obj = Gift.objects(git=gid).first()
    if gift_obj:
        ret['gnama'] = gift_obj['gname']
        ret['gicon'] = gift_obj['gicon']
        ret['price'] = gift_obj['price']
    return ret


def check_age_from_birthday(birthday):
    format_date = birthday + "00:00:00"
    timeArray = time.strptime(format_date, "%Y-%m-%d%H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    now = int(time.time())
    if (now - timeStamp) >= config.eighteenth_years_old:
        return 1
    else:
        return 0

# def gen_kafka_producer(topic, data):
#     producer = KafkaProducer(bootstrap_servers=KAFKA_ADDRESS)
#     send_data = json.dumps(data).encode("utf-8")
#     producer.send(topic=topic, value=send_data)
#     producer.close()
#     return True

def check_is_followed(uid, aid):
    return 1 if Follow.objects(uid=uid, aid=aid).first() else 0


# def check_is_block(uid, aid):
#     return 1 if BlockUser.objects(uid=uid, aid=aid).first() else 0


def get_cdn_address(url):
    url = url.strip('/')
    if url.startswith('jojor-source'):
        url = url[13:]
    return config.home_page_prefix + url


def get_audited_photo_from_audit_photo_list(audit_photo_list):
    """
        从审核图片列表里获取已经通过审核的图片
    """
    index = 0
    audited_list = list()
    if not audit_photo_list or len(audit_photo_list) == 0:
        return audited_list
    for photo_info in audit_photo_list:
        if photo_info["status"] != 2:
            continue
        audited_list.append(photo_info["photo"])
        index += 1
        if len(audited_list) >= 9:
            break
    return audited_list


def get_free_msg_key(uid):
    return "free_msg_key_{}".format(uid)


def get_coins(uid):
    user_obj = User.objects(id=uid).first()
    return user_obj.coins


def check_user_status(uid):
    status = 0
    user_obj = User.objects(id=uid).first()
    if user_obj:
        if user_obj.hidden_online == 0:
            status = user_obj.status
        else:
            status = 0
    return status


def gen_agora_token(room_id, agora_id):
    # 10s 过期
    agora_token = RtcTokenBuilder.buildTokenWithUid(config.agora_appid, config.appCertificate, room_id, agora_id, Role_Publisher,
                                                   0)
    return agora_token

def _gen_rtm_token(uid):
    expirationTimeInSeconds = 24 * 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expirationTimeInSeconds
    token = RtmTokenBuilder.buildToken(config.Appid, config.appCertificate, uid, Role_Rtm_User, privilegeExpiredTs)
    return token

def get_uid():
    # return snowflake.client.get_guid()
    return str(uuid.uuid4())
def gen_signature(param):
    str_parm = ''
    # 将字典中的key排序
    for p in sorted(param):
        # 每次排完序的加到串中
        # str类型需要转化为url编码格式
        if isinstance(param[p], str):
            str_parm = str_parm + str(p) + "=" + str(param[p]) + "&"
        continue
        str_parm = str_parm + str(p) + "=" + str(param[p]) + "&"
    return str_parm
