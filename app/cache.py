import os
import redis

from dotenv import load_dotenv

load_dotenv()

CACHE_NAME = os.getenv('CACHE_NAME')
CACHE_HOST = os.getenv('CACHE_HOST')
CACHE_PORT = os.getenv('CACHE_PORT')
CACHE_USER = os.getenv('CACHE_USER')
CACHE_EXPIRY = os.getenv('CACHE_EXPIRY')
CACHE_USER_PWD = os.getenv('CACHE_USER_PWD')


class Cache(object):
    def __init__(self, result_limit):
        self.result_limit = result_limit
        self.cache = redis.Redis(host=CACHE_HOST, port=CACHE_PORT, password=CACHE_USER_PWD, db=CACHE_NAME)
        self.key_count = len(self.cache.keys('*'))

    def get_cache_object(self):
        return getattr(self, 'cache')

    def search_result(self, keyword):
        result = self.cache.lrange(keyword, 0, 10)
        return [res.decode('utf-8') for res in result]

    def search_history(self, keyword):
        keyword = '*{0}*'.format(keyword)
        result = self.cache.keys(keyword)
        return [res.decode('utf-8') for res in result]

    def save_new_result(self, keyword, results):
        self.cache.delete(keyword)
        self.save_continued_result(keyword, results)

    def save_continued_result(self, keyword, results):
        self.cache.delete(keyword)
        self.cache.rpush(keyword, *results[-self.result_limit:])
        # self.cache.expire(keyword, CACHE_EXPIRY)
        self.key_count += 1
        return True
