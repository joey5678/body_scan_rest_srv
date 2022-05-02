from rediscluster import RedisCluster
from settings.evn_conf import startup_nodes


redis_conn = RedisCluster(startup_nodes=startup_nodes, skip_full_coverage_check=True)
