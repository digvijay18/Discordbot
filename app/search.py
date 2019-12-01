from googlesearch import search as Search


class SearchByGoogle(object):
    def __init__(self, domain='com', retry=True, retry_count=3, result_count=5, pause=3):
        self.retry = retry
        self.pause = pause
        self.results = []
        self.domain = domain
        self.retry_count = retry_count
        self.results_start = 0
        self.results_fetched = 0
        self.results_stop = result_count
        self.errors = False

    def _search(self, keyword, start, stop):
        results = Search(keyword, tld=self.domain, num=5, start=start, stop=stop, pause=self.pause)
        for result in results:
            self.results_fetched += 1
            self.results.append(result)
        return False

    def look_up(self, keyword):
        if not self.retry:
            retries_left = 1
        else:
            retries_left = self.retry_count

        results_start = self.results_start
        results_stop = self.results_stop

        while retries_left:
            results_start += self.results_fetched
            results_stop -= self.results_fetched
            try:
                _continue = self._search(keyword, results_start, results_stop)
                if not _continue:
                    break
            except Exception as excp:
                retries_left -= 1
                if retries_left == 0:
                    self.errors = str(excp)

        return self.results, self.errors
