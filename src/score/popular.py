import pywikibot
from api import wikipage
from api.pageviews import PageViewsAPI
import constants

def popularity_score(page, 
                     length_weight=-1, 
                     outbound_weight=-1,
                     views_weight=-1):
    score = 0

    if length_weight != -1:
        score += length_weight * page_length(page)
    if outbound_weight != -1:
        score += outbound_weight * outgoing_links(page)
    if views_weight != -1:
        score += views_weight * views(page)

    return score

def page_length(page):
    return len(page.text)

def outgoing_links(page):
    return len(wikipage.get_outgoing_links(page))

def views(page):
    subject = page.title()
    granularity = PageViewsAPI.Granularity[constants.PAGEVIEWS_QUERY_GRANULARITY]
    pv_api = PageViewsAPI(
        subject,
        constants.PAGEVIEWS_QUERY_START,
        constants.PAGEVIEWS_QUERY_END,
        granularity
    )
    return pv_api.get_page_views()[0]