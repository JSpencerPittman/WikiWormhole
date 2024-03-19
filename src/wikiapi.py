import pywikibot
from typing import List


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
