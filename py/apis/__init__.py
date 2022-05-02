# coding = utf-8

def _set_public_lib_ctx():
    """
    配置公共库环境,测试
    """
    from public.settings import CTX

    from models.sql_models import Session
    from settings import trans

    CTX.translate_resources = trans.msgs  # 翻译资源
    CTX.db_session_cls = Session  # mysql db session
