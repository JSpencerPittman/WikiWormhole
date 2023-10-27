import pywikibot

def get_wikipedia_page_from_title(title):
    site = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(site, title)
    return page

def get_wikipedia_page_from_url(url):
    title = url.split('/')[-1]
    return get_wikipedia_page_from_title(title)
