# coding=utf-8


_LEVEL = 'DEBUG'


def _file_handler(log_fname, formatter='simple'):
    return {
        'level': 'DEBUG',
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': formatter,
        'filename': 'log/%s.log' % log_fname,
        'maxBytes': 20 * 1048576, 'backupCount': 4,
        'encoding': 'utf-8'
    }


def _log_dict(handler, level="DEBUG"):
    return {'handlers': [handler], 'level': level, 'propagate': False}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
        },
        'print': {
            'format': '%(asctime)s %(message)s',
        }
    },
    'handlers': {
        'null': {'level': 'DEBUG', 'class': 'logging.NullHandler'},
        'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'simple'}
    },
    'loggers': {
        # 'root': _log_dict('null', level=_LEVEL),
    }
}

def _add(*names, formatter='simple'):
    for name in names:
        LOGGING.get("handlers")[name] = _file_handler(name, formatter=formatter)
        LOGGING.get("loggers")[name] = _log_dict(name, level=_LEVEL)


_add("error", "root", "async_register", "ago_log", "block_user", "make_list", "device_ban", "view", "token_check_log",
     "uid_token_log", "handle_eroticism", "feed_log", "promotion_log", "public_log", "test_api_log", "gen_rids", "ip",
     "login_out", "report_log","process_agora")
