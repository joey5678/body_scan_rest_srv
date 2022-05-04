from rediscluster import RedisCluster
from settings.evn_conf import startup_nodes

import red


class MyRedis():
    def __init__(self, ) -> None:
        pass
   
    def set(self, key, val, expiration_secs=0):
        return red.set_keyval(key, val, expiration_secs)

    def delete(self, k):
        return red.delete_key(k)

    def get(self, key, default=None):
        return red.get_keyval(key, default)

redis_conn = MyRedis()
