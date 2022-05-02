# coding=utf-8
import logging
import sys
import time
from functools import wraps

p_log = logging.getLogger("process")


def mk_stop_process_handler(executor, p_name="Main"):

    def stop_process_handler(signum, frame):
        p_log.info("{} process stop".format(p_name))

        time.sleep(1)
        if executor:
            executor.shutdown()

        sys.exit(0)

    return stop_process_handler


def simple_wrap_task(task):

    @wraps(task)
    def _task(*args, **kwargs):
        try:
            ret = task(*args, **kwargs)
            return ret

        except Exception as e:
            p_log.exception(e)

    return _task
