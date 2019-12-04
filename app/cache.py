"""
This file contains the cache which is basically a Redis instance. Currently,
it is not in use as Heroku doesn't provide free redis instance.
"""

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
        """
        This method returns the underlying Redis connection object in case
        you want to use the redis commands directly.
        """
        return getattr(self, 'cache')

    def search_result(self, keyword):
        """
        This method searches for result corresponding to the field search
        keywords. If the result is found, then it is returned and the search
        does not go downstream (to DB or the Google Search).
        """
        result = self.cache.lrange(keyword, 0, 10)
        return [res.decode('utf-8') for res in result]

    def search_history(self, keyword):
        """
        This method searches the search history for the provided keywords. If
        a result is found, then it is returned from Cache level and does not
        go down the search hierarchy (to DB).
        """
        keyword = '*{0}*'.format(keyword)
        result = self.cache.keys(keyword)
        return [res.decode('utf-8') for res in result]

    def save_new_result(self, keyword, results):
        """
        This method flushes the pre-existing result for the key and then loads
        the newly searched results (from DB or Google) into the cache.
        """
        self.cache.delete(keyword)
        self.save_continued_result(keyword, results)

    def save_continued_result(self, keyword, results):
        """
        This method can be used to push results on top of existing results (i.e.
        without removing the pre-existing results on a key). Currently, this
        facility is not under use.
        """
        self.cache.rpush(keyword, *results[-self.result_limit:])
        # self.cache.expire(keyword, CACHE_EXPIRY)
        self.key_count += 1
        return True
