# coding=utf-8

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings.evn_conf import MYSQL_CONFIG

from . import SqlModelMixin

Base = declarative_base()
eng = create_engine(MYSQL_CONFIG, encoding='utf-8', echo=True, pool_size=20, max_overflow=10, pool_recycle=14000)
#eng = create_engine('sqlite:///foo.db')
Session = sessionmaker(bind=eng)


class User(Base, SqlModelMixin):
    __tablename__ = 't_user_info'
    rid =  Column(Integer, nullable=False,primary_key=True)
    uid =  Column(String(32), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    head = Column(String(255), nullable=False)
    gender = Column(Integer, nullable=False, default=0)
    logintype = Column(Integer, nullable=False, default=1)
    thirduid = Column(String(255), nullable=False)
    iscoach = Column(Integer, nullable=False, default=0)
    desc =  Column(String(255), nullable=True)
    birthday = Column(String(12), nullable=True)
    country = Column(String(255), nullable=False)
    phone =  Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    create_time = Column(DateTime, nullable=False)
    modify_time = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False,default=1)
    android_id =  Column(String(32), nullable=True)
    os = Column(Integer, nullable=False,default=0)
    iOS_key =  Column(String(32), nullable=True)
    training_effect = Column(Integer, nullable=False,default=0)
    training_method = Column(Integer, nullable=False,default=0)
    training_interval =  Column(Integer, nullable=False,default=0)
    height =  Column(Integer, nullable=False,default=0)
    weight =  Column(Integer, nullable=False,default=0)

class Course(Base, SqlModelMixin):
    __tablename__ = 't_room_history'
    id =  Column(Integer, nullable=False,primary_key=True)
    uid =  Column(String(32), nullable=False, unique=True)
    roomname = Column(String(255), nullable=False)
    roomhead = Column(String(255), nullable=True)
    roomdes =  Column(String(255), nullable=False)
    ctime = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    status = Column(Integer, nullable=False,default=0)

class Phone_histroy(Base, SqlModelMixin):
    __tablename__ = 't_call_history'
    id =  Column(Integer, nullable=False,primary_key=True)
    uid =  Column(String(32), nullable=False)
    aid =  Column(String(32), nullable=False)
    ctime = Column(DateTime, nullable=False)
    start_time =  Column(DateTime, nullable=False,default=0)
    end_time =  Column(DateTime, nullable=False,default=0)
    hang_up =   Column(String(32), nullable=True,default="")
    status = Column(Integer, nullable=False,default=0)

class Banner(Base, SqlModelMixin):
    __tablename__ = 't_banner_info'
    rid =  Column(Integer, nullable=False,primary_key=True)
    status = Column(Integer, nullable=False,default=1)
    type =  Column(Integer, nullable=False,default=1) ##baner类型，1-直播课，2-教练
    actual_id =  Column(String(32), nullable=False,default="") ##对应的具体的值
    banner_img  = Column(String(128), nullable=False,default="") ##图片地址
    ctime = Column(DateTime, nullable=False)

class Dict(Base, SqlModelMixin):
    __tablename__ = 't_dict_info'
    id =  Column(Integer, nullable=False,primary_key=True)
    type =  Column(Integer, nullable=False,default=1) ##字典类型 1-训练效果，2-训练时间间隔 3-训练方式 4-外围课程标签 5-单节课标签
    value  = Column(String(128), nullable=False,default="") ##字典描述
    ctime = Column(DateTime, nullable=False)
    language  = Column(String(16), nullable=False,default="cn") ##字典描述


class Live_Info(Base, SqlModelMixin):
    __tablename__ = 't_live_course'
    live_id =  Column(Integer, nullable=False,primary_key=True)
    uid =  Column(String(32), nullable=False,default="") ##教练ID
    live_name  = Column(String(255), nullable=False,default="") ##名字
    live_banner = Column(String(255), nullable=False,default="") ##课程头像
    live_date = Column(String(12), nullable=False,default="") ##课程日期
    start_time = Column(Integer, nullable=False)##课程开始时间
    end_time  = Column(Integer, nullable=False)##课程结束时间
    live_label = Column(String(64), nullable=False)##课程标签
    live_desc = Column(String(1024), nullable=False)##课程描述
    for_people = Column(String(1024), nullable=False)##适用人群
    taboo_people  = Column(String(1024), nullable=False)##禁忌人群
    training_preparation  = Column(String(1024), nullable=False)##训练准备
    body_response  = Column(String(1024), nullable=False)##身体反应
    live_duration=  Column(Integer, nullable=False,default=0)##直播时长，单位分钟
    status = Column(Integer, nullable=False,default=0)##0 等待开始 1 正在上课, 2 结束
    burn_calories =  Column(Integer, nullable=False,default=1)##消耗的卡路里
    ctime = Column(Integer, nullable=False)


class Follow(Base, SqlModelMixin):
    __tablename__ = 't_follow'
    id =  Column(Integer, nullable=False,primary_key=True)
    uid  = Column(String(32), nullable=False,default="") ##关注ID
    aid  = Column(String(32), nullable=False,default="") ##被关注ID
    ctime = Column(DateTime, nullable=False)

class Coach(Base, SqlModelMixin):
    __tablename__ = 't_coach_info'
    rid =  Column(Integer, nullable=False,primary_key=True)
    uid = Column(String(32), nullable=False,default="")
    banner_img =  Column(String(255), nullable=False,default="") ##教练封面图
    fdesc  = Column(String(255), nullable=False,default="") ##教练介绍
    total_trainees  = Column(Integer, nullable=False,default=0) ##跟练人数
    training_category  = Column(String(255), nullable=False,default="") ##训练大类
    custom_label  = Column(String(255), nullable=False,default="") ##自定义标签
    create_time = Column(DateTime, nullable=False)
    coach_head_img =  Column(String(255), nullable=False,default="") ##自定义标签
    coach_type = Column(Integer,default=0)###0-静默教练，1-全能教练，2-私人教练
    language =  Column(String(16), nullable=False,default="cn") ##自定义标签

class Course(Base, SqlModelMixin):
    __tablename__ = 't_course_info'
    course_id =  Column(Integer, nullable=False,primary_key=True)
    uid = Column(String(32), nullable=False,default="")
    course_name =  Column(String(255), nullable=False,default="") ##名字
    course_img  = Column(String(255), nullable=False,default="") ##课程封面
    fdesc  = Column(String(255), nullable=False,default="") ##课程描述
    course_duration  = Column(Integer, nullable=False,default=0) ##课程时长
    burn_calories  = Column(Integer, nullable=False,default=0) ##消耗卡路里
    total_trainees = Column(Integer, nullable=False,default=0) ##跟练人数
    total_course  = Column(Integer, nullable=False,default=0) ##课时总数
    training_category  = Column(String(255), nullable=False,default="") ##训练大类
    create_time = Column(DateTime, nullable=False)
    label = Column(String(255), nullable=False,default="") ##课程标签
    course_type =  Column(Integer, nullable=False,default=0) ##课程类别 0-点播课，1-直播课 2-精确纠错课 3-播放视频
    language =  Column(String(16), nullable=False,default="cn") ##自定义标签


class Course_class(Base, SqlModelMixin):
    __tablename__ = 't_course_class'
    class_id =  Column(Integer, nullable=False,primary_key=True)
    course_id =  Column(Integer, nullable=False,default=0)
    class_name  = Column(String(255), nullable=False,default="")
    class_img = Column(String(255), nullable=False,default="")
    class_desc = Column(String(255), nullable=False,default="")
    class_duration = Column(Integer, nullable=False,default=0) ##课时时长
    burn_calories = Column(Integer, nullable=False,default=0) ##课时时长
    custom_label =  Column(String(255), nullable=False,default="") ##名字
    create_time = Column(DateTime, nullable=False)
    content_url = Column(String(255), nullable=False,default="") ##url地址
    language =  Column(String(16), nullable=False,default="cn") ##自定义标签

class Training_plan(Base, SqlModelMixin):
    __tablename__ = 't_training_plan'
    training_id =  Column(Integer, nullable=False,primary_key=True)
    uid = Column(String(32), nullable=False,default="")
    class_id =  Column(Integer, nullable=False,default=0)##t_course_class 或者是t_live_course 里面的live_id
    class_type =  Column(Integer, nullable=False,default=0)##t类型 1-直播课 2-本地课程
    training_time =Column(Integer, nullable=False,default=0)##训练时长
    burn_calories =Column(Integer, nullable=False,default=0)##消耗卡路里
    training_date = Column(String(12), nullable=False,default="")#训练日期
    create_time = Column(DateTime, nullable=False)
    modify_time = Column(DateTime, nullable=False)


class Training_overview(Base, SqlModelMixin):
    __tablename__ = 't_training_overview'
    id =  Column(Integer, nullable=False,primary_key=True)
    uid = Column(String(32), nullable=False,default="")
    training_time =  Column(Integer, nullable=False,default=0)##训练时长
    burn_calories =  Column(Integer, nullable=False,default=0)##消耗卡路里
    training_date = Column(String(12), nullable=False,default="")#训练日期
    create_time = Column(DateTime, nullable=False)
    modify_time = Column(DateTime, nullable=False)

class Certificate_list(Base, SqlModelMixin):
    __tablename__ = 't_certificate_list'
    id =  Column(Integer, nullable=False,primary_key=True)
    uid = Column(String(32), nullable=False,default="")
    certificate_id =  Column(Integer, nullable=False,default=0)##证书ID
    get_date =  Column(String(12), nullable=False,default="")#证书获取的具体日期
    get_month = Column(String(12), nullable=False,default="")#证书获取的年月
    create_time = Column(DateTime, nullable=False)

class Certificate_info(Base, SqlModelMixin):
    __tablename__ = 't_certificate_info'
    id =  Column(Integer, nullable=False,primary_key=True)
    certificate_name = Column(String(255), nullable=False,default="")
    certificate_url =  Column(String(255), nullable=False,default="")#证书获取的具体日期
    status = Column(Integer, nullable=False,default=1)#证书获取的年月
    create_time = Column(DateTime, nullable=False)

class Medal_info(Base, SqlModelMixin):
    __tablename__ = 't_medal_info'
    medal_id =  Column(Integer, nullable=False,primary_key=True)
    medal_name =  Column(String(255), nullable=False,default="")#证书名称
    medal_url = Column(String(255), nullable=False,default="")#证书获取的年月
    medal_type =  Column(Integer, nullable=False,default=0)##勋章类型 可以去取字典表里面字典 type为5的数据
    status =  Column(Integer, nullable=False,default=0)##状态
    create_time = Column(DateTime, nullable=False)

class Medal_list(Base, SqlModelMixin):
    __tablename__ = 't_medal_list'
    id =  Column(Integer, nullable=False,primary_key=True)
    uid = Column(String(32), nullable=False,default="")
    medal_id =  Column(Integer, nullable=False,default=0)##状态
    create_time = Column(DateTime, nullable=False)

# Base.metadata.create_all(eng)  # 创建所有表结构
