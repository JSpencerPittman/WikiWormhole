from __future__ import annotations
import requests
from enum import Enum
from datetime import ( date, timezone, datetime, time )

PAGEVIEWS_BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents"

class PageViewsAPI(object):
    class Granularity(Enum):
        HOURLY = 'hourly'
        DAILY = 'daily'
        MONTHLY = 'monthly'

    def __init__(self, 
                 subject: str,
                 start: datetime,
                 finish: datetime,
                 granularity: PageViewsAPI.Granularity):
        if start >= finish:
            raise Exception("Error: PageViewsAPI: please make sure start is before finish.")

        self.subject = subject
        self.start = start
        self.finish = finish
        self.granularity = granularity

    def get(self):
        headers = {"Accept": "application/json",
                   "User-Agent": "WikiWormhole/1.0 (https://github.com/JSpencerPittman; jspencerpittman@gmail.com)"}
        res = requests.get(self._generate_url(), headers=headers)
        print(res.text)

    def _generate_url(self):
        start_timestamp = PageViewsAPI._generate_timestamp(self.start)
        finish_timestamp = PageViewsAPI._generate_timestamp(self.finish)
        return f"{PAGEVIEWS_BASE_URL}/{self.subject}/{self.granularity.value}/{start_timestamp}/{finish_timestamp}"

    @staticmethod
    def _generate_timestamp(dt: datetime):
        expand = lambda v: str(v) if v >= 10 else f"0{v}"
        year = dt.year
        month, day, hour = expand(dt.month), expand(dt.day), expand(dt.hour)
        timestamp = f"{year}{month}{day}{hour}"
        return timestamp
    

if __name__ == "__main__":
    start = datetime(2015, 10, 1, 0)
    finish = datetime(2015, 11, 1, 0)
    pvapi = PageViewsAPI("Albert_Einstein", start, finish, PageViewsAPI.Granularity.MONTHLY)
    print(pvapi.get())
    # get_page_views("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/2015100100/2015103100")