#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

# 直接连接redis
# conn = redis.StrictRedis(host='localhost', port=6379, password='foobared', decode_responses=True) # NOTE: 每次重新连接效率较低

# 连接池
pool = redis.ConnectionPool(
    host='localhost', port=6379, password='foobared', decode_responses=True)
conn = redis.StrictRedis(connection_pool=pool)


# 设置键值：19850052801="520" 且超时时间为10秒（值写入到redis时会自动转字符串）
conn.set('19850052801', 520, ex=10)
# 根据键获取值：如果存在获取值（获取到的是字节类型）；不存在则返回None
value1 = conn.get('15131255089')
value2 = conn.get('19850052801')
print(value1, value2)
