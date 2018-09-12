# -*- coding:utf-8 -*-
import redis  # redis数据库链接


class RedisClient():
    def __init__(self):
        # 创建对本机数据库的连接对象
        self.conn = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    # 存储
    def set(self, key_, value_):
        self.conn.set(key_, value_)

    def set_expire(self, key_, value_, expire=120):
        self.conn.set(key_, value_)
        self.conn.expire(key_, expire)

    # 读取
    def get(self, key_):
        # 从数据库根据键（key）获取值
        return self.conn.get(key_)

    def hset(self, name_, key_, value_):
        self.conn.hset(name_, key_, value_)

    def hget(self, name_, key_):
        self.conn.hget(name_, key_)

    def hdelall(self, name_):
        for key in self.conn.hkeys(name_):
            self.conn.hdel(name_, key)



