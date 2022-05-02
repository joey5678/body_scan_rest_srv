#!python
# coding=utf-8
from mongoengine import connect, Document, StringField, IntField, ListField, DictField
import os
mongodb_host = os.environ.get("mongo_host",
                              "")
connect(host=mongodb_host, retrywrites='false')


class User(Document):
    """ 用户表"""
    name = StringField(default='')              # 用户名字
    head = StringField(default='')              # 用户头像
    banner = ListField(default=[])              # 轮播图
    gender = IntField(default=1)                # 性别。1代表男性，2代表女性
    uid = StringField(default="")               # token验证出来的id
    age = IntField(default=25)                  # 用户年龄
    country = StringField(default='')           # 用户国家
    rid = StringField(default="1000000")        # 用户原始rid
    agora_id = IntField(default=1000000)        # 用户redis 出的id (用于给声网初始化，唯一性)
    valid = IntField(default=1)                 # 用户是否被封号。0代表被封号
    login_type = IntField(default=0)            # 1-Google登录， 2-FaceBook登录， 3-Snapchat登录，4-手机登录， 5-苹果登录,  6-游客苹果登录,  7-游客谷歌登录
    birthday = StringField(default='')          # 用户生日
    lang = IntField(default=1)                  # 1代表英语地区， 2代表阿语地区, 3代表阿语地区
    imsi = StringField(default='')              # 安卓手机标识
    imei = StringField(default='')              # 安卓手机标识
    android_id = StringField(default='')        # 安卓手机标识
    ioskey = StringField(default='')            # 苹果手机标识
    os = StringField(default='')                # “0”代表安卓用户， “1”代表苹果用户
    desc = StringField(default='')              # 个性签名
    ip = StringField(default="")                # ip地址
    register_date = IntField(default=0)         # 注册时间, 时间搓表示
    coin_price = IntField(default=30)           # 聊天金币价格
    video = DictField(default={})             # 主播展示视频,字典格式,preview预览图,video视频地址,c_time修改时间
    gender_lang = IntField(default=0)           # 主播身份的语言区      1 代表英语， 2 代表阿语
    gender_area = IntField(default=0)           # 主播身份的地区        1 代表亚洲   2 代表欧洲

    """动态信息（及时性）"""
    coins = IntField(min_value=0, default=0)      # 金币体系
    room = StringField(default='')                # 是否在某个房间内
    last_login = DictField(default={})            # 上次登录时间，字典格式，时间搓显示
    status = IntField(default=0)                  # 用户在线状态, 0 代表离线  1 代表在线 2 代表通话中
    hidden_online = IntField(default=0)  # 0代表正常，1代表隐藏

    meta = {'collection': 'user', "strict": False}


class Room(Document):
    """
        主播才有房间， 方便生成列表的存在
    """
    room_id = StringField(default="")               # 房间id
    owner_online = IntField(default=0)              # 房主是否在线，  0代表离线 1代表在线未通话 2代表通话中
    stream_id = IntField(default=0)                 # 流id
    name = StringField(default="")                  # 房间名字    主播名字
    head = StringField(default="")                  # 房间头像    主播的 头像
    country = StringField(default="")               # 房间国家    主播的国家
    lang = IntField(default=1)                      # 1 代表英语地区， 2 代表阿语地区
    area = IntField(default=1)                      # 1 代表亚洲， 2 代表欧洲

    meta = {'collection': 'room', "strict": False}


class UserGiftCoins(Document):
    """
        用户的礼物贡献值(做外面的个人总榜)
    """
    uid = StringField(default="")                   # 发送者
    aid = StringField(default="")                   # 接收者
    coins = IntField(default="")                    # 总价值
    c_time = IntField(default=0)                    # 创建时间

    meta = {"collection": "user_gift_coins", "strict": False}


class HandleImage(Document):
    """
    不合法的图片记录
    """
    uid = StringField(default='')
    url = StringField(default='')
    type = IntField(default=0)      # 1. 头像  2. banner 3. 房间头像
    c_time = IntField(default=0)

    meta = {'collection': 'handle_image', "strict": False}


class Follow(Document):
    """
        用户uid 关注了aid
    """
    uid = StringField(default="")                   # uid
    aid = StringField(default="")                   # aid
    c_time = IntField(default=0)                    # 关注时间

    meta = {"collection": "follow", "strict": False}


class Fans(Document):
    """
        uid 的粉丝 aid
    """
    uid = StringField(default="")                   # uid
    aid = StringField(default="")                   # aid
    c_time = IntField(default=0)                        # 被关注时间

    meta = {"collection": "fans", "strict": False}


class GiftSending(Document):
    """uid送的礼物记录"""
    uid = StringField(default="")                  # 送礼物的id
    aid = StringField(default="")                  # 接收礼物的id
    gid = IntField(default=0)
    c_time = IntField(default=0)

    meta = {'collection': 'gift_sending', "strict": False}


class Gift(Document):
    """

    """
    gid = IntField(default=0)
    gname = StringField(default="")                 # 礼物名字
    gicon = StringField(default="")                 # 礼物图标
    status = IntField(default=1)                    # 礼物状态，0代表失效，1代表使用
    price = IntField(default=0)                     # 礼物价格
    zipInfo = DictField(default={})                 # 礼物资源
    c_time = IntField(default=0)                    # 礼物创建时间
    order = IntField(default=0)                     # 礼物排序用

    meta = {'collection': 'gift', "strict": False}


class GiftSendNum(Document):
    """uid送的礼物总记录"""
    uid = StringField(default="")
    gid = IntField(default=0)
    price = IntField(default=0)
    gift_num = IntField(default=0)
    c_time = IntField(default=0)

    meta = {'collection': 'gift_send_num', "strict": False}


class GiftRevNum(Document):
    """uid收到的礼物总记录"""
    uid = StringField(default="")
    gid = IntField(default=0)
    gift_num = IntField(default=0)
    price = IntField(default=0)
    c_time = IntField(default=0)

    meta = {'collection': 'gift_rev_num', "strict": False}


class BlockUser(Document):
    """
        uid 的拉黑aid 们
    """
    uid = StringField(default="")                   # uid
    aid = StringField(default="")                   # aid
    c_time = IntField(default=0)                    # 拉黑时间

    meta = {"collection": "block_user", "strict": False}


class Audithead(Document):
    """
        头像审核记录
    """
    uid = StringField(default="")                   # uid
    head = StringField(default="")                   # head
    status = IntField(default=1)                    # 1为审核中,2为通过,3为不通过
    c_time = IntField(default=0)

    meta = {"collection": "audit_head", "strict": False}


# class AuditPhoto(Document):
#     """
#         个人图片审核记录
#     """
#     uid = StringField(default="")                   # uid
#     photo_list = ListField(default=[])              # 图片list 格式为[{"photo":图片1,"status":审核状态,"c_time"上传时间}, {"photo":图片2,"status":审核状态,"c_time"上传时间}]  status:1为审核中,2为通过,3为不通过
#     audit_num = IntField(default=1)                 # 未审核图片数
#     c_time = IntField(default=0)                    # 最后送审图片加入时间
#
#     meta = {"collection": "audit_photo", "strict": False}

class AuditPhoto(Document):
    uid = StringField(default="")                   # uid
    rid = StringField(default="")                   # uid
    photo = StringField(default="")              # 图片list 格式为[{"photo":图片1,"status":审核状态,"c_time"上传时间}, {"photo":图片2,"status":审核状态,"c_time"上传时间}]  status:1为审核中,2为通过,3为不通过
    status = IntField(default=1)                 # 未审核图片数
    c_time = IntField(default=0)                    # 最后送审图片加入时间

    meta = {"collection": "audit_photo", "strict": False}


class AuditVideo(Document):
    """
        视频审核记录
    """
    uid = StringField(default="")                   # uid
    video = StringField(default="")
    preview = StringField(default="")               # 视频预览图
    status = IntField(default=1)                    # 1为审核中,2为通过,3为不通过
    c_time = IntField(default=0)                    # 送审时间

    meta = {"collection": "audit_video", "strict": False}


class PhoneAccount(Document):
    """
        firebase 电话登录的用户
    """
    uid = StringField(default='')                           # 关联的uid
    account = StringField(default='', primary_key=True)     # 手机号码
    pwd = StringField(default='')                           # 密码
    c_time = IntField(default=0)                            # firebase 手机号码登录

    meta = {'collection': 'phone_account', "strict": False}


# class CallHistory(Document):
#     """
#         用户通话记录
#     """
#     uid = StringField(default='')  # 拨打电话的用户
#     aid = StringField(default='')  # 接听电话的用户
#     talk_time = IntField(default=0)   # 通话时间,以秒为单位
#     status = IntField(default=0)   # 状态,0无应答,1接通,2未接通
#     c_time = IntField(default=0)   # 记录时间
#
#     meta = {'collection': 'call_history', "strict": False}


class CallHistory(Document):
    """
        用户通话记录
    """
    uid = StringField(default='')       # 拨打电话的用户
    aid = StringField(default='')       # 接听电话的用户
    is_gender = IntField(default=0)     # 0 代表用户主动拨打， 1代表主播主动拨打
    status = IntField(default=0)        # 状态,0代表未接通，1通话中, 2 拒接， 3 代表主动挂断， 4 代表用户没钱了超时挂断,5 异常挂断
    c_time = IntField(default=0)        # 开始拨打时间
    start_time = IntField(default=0)    # 开始接通时间
    end_time = IntField(default=0)      # 结束时间
    hang_up = StringField(default="")       # 主动挂电话方， uid 或者 aid  或者空（未接通状态）
    coin_price = IntField(default=30)  # 聊天金币价格
    mins = IntField(default=0)        #通话时长
    coins = IntField(default=0)        #消耗的金币数
    meta = {'collection': 'call_history', "strict": False}


class Report(Document):
    """
        举报记录
    """
    aid = StringField(default='')  # 被举报人
    uid = StringField(default='')  # 举报人
    u_id = StringField(default='')  # 被举报主播的公会id
    reason = IntField(default=1)   # 举报原因,1,虚假信息,2,涩情内容,3,骚扰或令人不适言语,4,不合理要求
    # report_num = IntField(default=0)  # 被举报次数
    handle = StringField(default='')  # 处理方式
    c_time = IntField(default=0)   # 记录时间

    meta = {'collection': 'report', "strict": False}


class ReportNum(Document):
    """
        被举报人的被举报次数
    """
    aid = StringField(default='')  # 被举报人
    num_dict = DictField(default={1: 0, 2: 0, 3: 0, 4: 0})   # 被举报次数,字典结构,key为举报原因,value为举报次数

    meta = {'collection': 'report_num', "strict": False}


class Anchor(Document):
    uid = StringField(default='')
    rid = StringField(default='')               # 用户rid
    real_name = StringField(default='')      # 真实姓名
    nick_name = StringField(default='')      # 昵称
    phone = StringField(default=None)
    gender = IntField(default=2)             # 性别
    age = IntField(default=None)
    language = StringField(default='')

    left_coins = IntField(default=0)
    coin_price = IntField(default=30)        # 聊天金币价格
    u_id = StringField(default='')           # 所属工会uid
    u_name = StringField(default='')         # 所属公会名称
    c_time = IntField(default=None)          # 成为主播的时间戳
    valid = IntField(default=1)                 # 用户是否被封号。0代表被封号

    meta = {'collection': 'anchor', "strict": False}
