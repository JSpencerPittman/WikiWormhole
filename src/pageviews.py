from __future__ import annotations
import requests
from enum import Enum
from datetime import ( date, timezone, datetime, time )
import constants

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

    def get_page_views(self):
        headers = {"Accept": "application/json",
                   "User-Agent": f"WikiWormhole/1.0 ({constants.PAGEVIEWS_WEBSITE}; {constants.PAGEVIEWS_EMAIL_ADDRESS})"}
    
        res = requests.get(self._generate_url(), headers=headers)

        if res.status_code != 200:
            raise Exception("Error: PageViewsAPI: invalid URL request")
        
        json_data = res.json()
        self.views = [d['views'] for d in json_data['items']]

        return self.views

    def _generate_url(self):
        start_timestamp = PageViewsAPI._generate_timestamp(self.start)
        finish_timestamp = PageViewsAPI._generate_timestamp(self.finish)
        return f"{constants.PAGEVIEWS_BASE_URL}/{self.subject}/{self.granularity.value}/{start_timestamp}/{finish_timestamp}"

    @staticmethod
    def _generate_timestamp(dt: datetime):
        expand = lambda v: str(v) if v >= 10 else f"0{v}"
        year = dt.year
        month, day, hour = expand(dt.month), expand(dt.day), expand(dt.hour)
        timestamp = f"{year}{month}{day}{hour}"
        return timestamp
    