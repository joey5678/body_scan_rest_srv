# coding = utf-8
"""
    kafka 的topic
"""
# -----------------------通话中的大topic{ OnCall } -----------------------------
# 通话中的大topic
ONCALL = "OnCall"

# 不足30金币
NEED_RECHARGE = "need_recharge"

# 金币不足再拨打下一分钟, 直接挂断电话
CLOSE_PHONE = "close_phone"

# 发送房间内消息
PHONE_MESSAGE = "in_phone_message"

CLOSE_PHONE_NO_BALANCE = "close_phone_no_balance"

# 异常结束时给主播的结账信息
BOOKS_PHONE = "close_accounts"

# -----------------------用户状态大topic{ UserStatus } -----------------------------
# 用户登录
USER_LOGIN_IN = 'mars_login'

# 用户退出
USER_LOGIN_OUT = 'mars_logout'


# -----------------------外围的大topic{ OffCall } -----------------------------
# 外围大topic
OFFCALL = "OffCall"

# 申请通话
APPLY_CALL = "apply_call"

#发送礼物
SEND_GIFT = "send_gift"
CONNECT_CALL = "connect_call"
REJECT_CALL="reject_call"

#遮挡摄像头
BLOCK_CAMERA = "block_camera"
#进入房间
ENTER_ROOM = "enter_room"

#退出房间
LEAVE_ROOM ="leave_room"
#发送消息
SEND_MSG = "send_message"
