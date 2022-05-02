# coding=utf-8
import logging
import uuid
from functools import wraps

from .settings import CTX
from .x_thread import th_local


lock_log = logging.getLogger("db_lock")
root_log = logging.getLogger("root")


def get_db_session(auto_create=True):
    ses = getattr(th_local, "db_session", None)
    if not ses and auto_create:
        ses = CTX.db_session_cls
        th_local.db_session = ses

    return ses


def new_db_session():
    return CTX.db_session_cls


class NewSubTransaction(object):
    """
    子事务
    """

    def __init__(self, ignore_exc=False):
        self.ignore_exc = ignore_exc
        self.session = new_db_session()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):

        if not exc_tb:
            self.session.commit()
            self.session.close()

        else:
            self.session.rollback()
            self.session.close()

            if self.ignore_exc:
                root_log.warning("%s - %s\n%s", exc_type, exc_val, exc_tb)
                return True


def mk_transaction_mgr(log=None):

    def transaction_mgr(func):
        @wraps(func)
        def _mgr(*args, **kwargs):
            lock_name = "{}:{}".format(func.__name__, uuid.uuid1())
            lock_log.debug("Lock start {}".format(lock_name))
            ret = None
            try:
                ret = func(*args, **kwargs)

            except Exception as e:
                log.exception(e)

                db_session = get_db_session(auto_create=False)
                if db_session:
                    db_session.rollback()
                    lock_log.debug("Lock rollback {}".format(lock_name))
            else:
                db_session = get_db_session(auto_create=False)
                if db_session:
                    db_session.commit()
                    lock_log.debug("Lock commit {}".format(lock_name))

            finally:
                db_session = get_db_session(auto_create=False)
                if db_session: db_session.close()

            return ret

        return _mgr

    return transaction_mgr


if __name__ == '__main__':
    print(new_db_session())


