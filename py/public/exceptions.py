# coding=utf-8


class VldException(Exception):
    pass


class MissParamException(Exception):
    pass


class NotLoginException(Exception):
    pass


class OtherLoginException(Exception):
    pass


class InvalidADException(Exception):
    pass


class BannedException(Exception):
    pass


class UpdateException(Exception):
    pass


class BizFailException(Exception):

    def __init__(self, error_message="Server execution failed", error_code=6001, data={}):
        super(BizFailException, self).__init__(error_message)
        self.error_code = error_code
        self.data = data
