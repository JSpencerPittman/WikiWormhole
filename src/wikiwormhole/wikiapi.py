import pywikibot
from wikiwormhole import constants
import requests
from typing import List
from datetime import datetime


def generate_wiki_page_from_title(title: str) -> pywikibot.Page:
    """
    Gets the wikipedia page referencing the given title.

    Args:
        title (str): title of the wikipedia page to search for.

    Returns:
        pywikibot.Page: an interface to the wikipedia page of interest.
    """

    # Interface for MediaWiki sites
    site = pywikibot.Site('en', 'wikipedia')

    # A MediaWiki page
    page = pywikibot.Page(site, title)

    return page


def generate_wiki_page_from_url(url: str) -> pywikibot.Page:
    """
    A wrapper around `get_wikipedia_page_from_title`. Accepts a URL for a wikipedia page from which the title is extracted.

    Args:
        url (str): URL of wikipedia page.

    Returns:
        pywikibot.Page: an interface to the wikipedia page of interest.
    """

    # Extract title
    title = url.split('/')[-1]

    return generate_wiki_page_from_title(title)


def retrieve_outgoing_links(page: pywikibot.Page) -> List[pywikibot.Page]:
    """
    Retrieve all outgoing links from the provided wiki page.

    Args:
        page (pywikibot.Page): the page containing outgoing links.

    Returns:
        List[pywikibot.Page]: a list of pages linked from the original page.
    """

    return [link for link in page.linkedPages() if link.namespace() == 0]


def retreive_pageviews(page: pywikibot.Page,
                       start_dt: datetime,
                       end_dt: datetime,
                       granularity: str) -> List[int]:
    """
    Retreive page views for a wiki page.

    Args:
        page (pywikibot.Page): wiki page to retreive views for.
        start_dt (datetime): time to start checking for page views.
        end_dt (datetime): time to stop checking for page views.

    Raises:
        Exception: start time must be before end time.
        Exception: granularity is not daily or monthly.
        Exception: request may fail.

    Returns:
        List[int]: returns page views per month.
    """

    # Verify end comes after start date.
    if start_dt >= end_dt:
        raise Exception(
            "WikiAPI.get_page_views: end date is before start date.")

    # Verify granularity is monthly or daily.
    if granularity not in ['DAILY', 'MONTHLY']:
        raise Exception(
            "WikiAPI.get_page_views: granularity must be either DAILY or MONTHLY.")

    # Headers for the API request.
    headers = {"Accept": "application/json",
               "User-Agent": f"WikiWormhole/1.0 ({constants.PAGEVIEWS_WEBSITE}; {constants.PAGEVIEWS_EMAIL_ADDRESS})"}

    # Format datetimes as timestamps.
    start_ts = _generate_timestamp(start_dt)
    end_ts = _generate_timestamp(end_dt)

    # Generate the URL for the pageviews API.
    uri_title = page.title().replace(' ', '_')
    generated_url = f"{constants.PAGEVIEWS_BASE_URL}/{uri_title}/{constants.PAGEVIEWS_QUERY_GRANULARITY}/{start_ts}/{end_ts}"

    # Retrieve JSON data from the API.
    response = requests.get(generated_url, headers=headers)

    # Did the request fail.
    if response.status_code != 200:
        raise Exception(
            f"PWikiAPI.get_page_views: invalid for URL request: {generated_url}")

    # Extract page views from JSON.
    return [d['views'] for d in response.json()['items']]


def _generate_timestamp(dt: datetime) -> str:
    """
    Generates a timestamp string from the provided datetime.

    Args:
        dt (datetime): datetime to be converted to string.

    Returns:
        str: resultant timestamp.
    """

    # Ensure digits are two characters long.
    def fmt(v: int) -> str:
        return str(v) if v >= 10 else f"0{v}"

    # Extract components of datetime
    year = dt.year
    month, day, hour = fmt(dt.month), fmt(dt.day), fmt(dt.hour)

    return f"{year}{month}{day}{hour}"
