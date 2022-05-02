# coding=utf-8
import os
from elasticsearch import Elasticsearch

MYSQL_CONFIG = "mysql+mysqlconnector://appyunwei:appyunwei123@58f74d444593d.gz.cdb.myqcloud.com:14529/firenow"
# mysql测试环境和正式环境都有sql_server---亚马逊的endpoint
ES_ADDRESS = "172.25.234.193:9200"
KAFKA_ADDRESS ="172.25.234.193:9092"
redis_model = os.environ.get("redis_mode", 0)
startup_nodes = [
        {"host": "172.25.234.193", "port": "7000"},
        {"host": "172.25.234.193", "port": "7001"},
        {"host": "172.25.234.193", "port": "7002"},
        {"host": "172.25.234.193", "port": "7003"},
        {"host": "172.25.234.193", "port": "7004"},
        {"host": "172.25.234.193", "port": "7005"},
    ]

es = Elasticsearch(
    hosts=[ES_ADDRESS],
    sniff_on_start=True,
    sniff_on_connection_fail=True,
    sniffer_timeout=300
)
