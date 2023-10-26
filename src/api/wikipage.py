import pywikibot

def get_python_wikipedia_content():
    site = pywikibot.Site('en', 'wikipedia')  # Connect to the English Wikipedia
    page = pywikibot.Page(site, "Olentzero")
    # return [link for link in page.linkedPages() if link.namespace() == 0]
    return page.text

if __name__ == "__main__":
    content = get_python_wikipedia_content()
    print(content)
