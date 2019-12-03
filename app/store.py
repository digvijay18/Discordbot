import db
import cache
import search
import constants


class Store(object):
    def __init__(self, use_cache=False, cache_result_limit=5):
        self.results = []
        self.errors = None
        self.use_cache = use_cache
        self.db = db.DB()
        self.cache = None  # cache.Cache(cache_result_limit)
        self.engine = search.SearchByGoogle()
        self.searchable = [constants.RESULT]
        self.cacheable = [constants.RESULT]

    def search(self, keyword, op_type):
        # self.search_cache(keyword, op_type) or self.search_db(keyword, op_type)
        self.search_db(keyword, op_type)
        if not self.results and op_type in self.searchable:
            self.search_engine(keyword)
            self.save(keyword, self.results)
        results = self.results
        self.results = []
        return results

    def search_cache(self, keyword, op_type):
        method = 'search_{0}'.format(op_type)
        print('Searching Cache for: ', keyword, op_type)
        try:
            result = getattr(self.cache, method)(keyword)
            print('Results From Cache: ', str(result))
            self.results.extend(result)
            return not not result
        except AttributeError as exc:
            self.errors = str(exc)
            return False

    def search_db(self, keyword, op_type):
        method = 'query_{0}'.format(op_type)
        print('Searching DB For: ', keyword, op_type)
        try:
            result = getattr(self.db, method)(keyword)
            self.results.extend(result)
            print('Results From DB: ', self.results)
            if result and op_type in self.cacheable:
                pass
                # self.save_in_cache(keyword, result)
            return not not result
        except AttributeError as exc:
            self.errors = str(exc)
            return False

    def search_engine(self, keyword):
        print('Searching Google for: ', keyword)
        try:
            result, errors = self.engine.look_up(keyword)
            print('Results From Google: ', str(result))
            self.results.extend(result)
            return True
        except Exception as exc:
            self.errors = str(exc)
            return False

    def save(self, keyword, results):
        # self.save_in_cache(keyword, results)
        self.save_in_db(keyword, results)

    def save_in_cache(self, keyword, results):
        if not self.use_cache:
            return
        try:
            self.cache.save_new_result(keyword, results)
        except Exception as exc:
            pass

    def save_in_db(self, keyword, results):
        try:
            self.db.save_result(keyword, results)
        except Exception as exc:
            pass

    def __del__(self):
        self.db.close()
