# coding=utf-8

import threading
from concurrent.futures import ThreadPoolExecutor

th_local = threading.local()
executor = ThreadPoolExecutor(100)
