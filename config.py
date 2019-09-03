"""
代理池相关的配置信息
"""
# Mongodb数据库
NAME = 'proxy'
TABLE = 'proxy'
HOST = 'localhost'
PORT = 27017

# 供测试的url
TEST_URL = 'https://www.baidu.com/'  # 只获取请求头

# Pool 的低阈值和高阈值
POOL_LOWER_THRESHOLD = 100
POOL_UPPER_THRESHOLD = 1000

# 两个调度进程的周期
VALID_CHECK_CYCLE = 120  # 有效性检查周期
POOL_LEN_CHECK_CYCLE = 10  # 代理池容量检查周期
