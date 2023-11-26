from __future__ import annotations
import requests
from enum import Enum
from datetime import ( date, timezone, datetime, time )
import constants

def get_page_views(subject: str,
                   start: datetime,
                   finish: datetime,
                   granularity: str):
    if start >= finish:
            raise Exception("Error: get_page_views: please make sure start is before finish.")

    headers = {"Accept": "application/json",
                "User-Agent": f"WikiWormhole/1.0 ({constants.PAGEVIEWS_WEBSITE}; {constants.PAGEVIEWS_EMAIL_ADDRESS})"}

    start_timestamp = _generate_timestamp(start)
    finish_timestamp = _generate_timestamp(finish)
    generated_url = f"{constants.PAGEVIEWS_BASE_URL}/{subject}/{granularity}/{start_timestamp}/{finish_timestamp}"

    res = requests.get(generated_url, headers=headers)

    if res.status_code != 200:
        raise Exception("Error: PageViewsAPI: invalid URL request")
    
    json_data = res.json()
    views = [d['views'] for d in json_data['items']]

    return views

def _generate_timestamp(dt: datetime):
    expand = lambda v: str(v) if v >= 10 else f"0{v}"
    year = dt.year
    month, day, hour = expand(dt.month), expand(dt.day), expand(dt.hour)
    timestamp = f"{year}{month}{day}{hour}"
    return timestamp
    