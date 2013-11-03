import pickle
import urlparse
import requests
## BeautifulSoup 4 is not parsing this page right and I don't know why
## import html5lib
## from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup

FICLY_RECENT = 'http://ficly.com/stories/recent'
## Manually incremented, set to 0 to start from the beginning
FICLY_PAGE = 0
## STORY_URLS = []
STORY_URLS = pickle.load(open('ficly-story-urls.pickle', 'rb'))

if FICLY_PAGE > 0:
    ## This is not a proper way to create a URL
    FICLY_NEXT = FICLY_RECENT + '?page={0}'.format(FICLY_PAGE)
else:
    FICLY_NEXT = FICLY_RECENT

while FICLY_NEXT is not None:
    r = requests.get(FICLY_NEXT)
    if r.status_code == requests.codes.ok:
        ## s = BeautifulSoup(r.text, 'html5lib')
        s = BeautifulSoup(r.text)

        sl = len(STORY_URLS)
        ## print s.find_all('a', rel='bookmark')
        for a in s.findAll('a', rel='bookmark'):
            if not a['href'] in STORY_URLS:
                STORY_URLS.append(a['href'])

        # Comment this out if FICLY_PAGE isn't starting from 0 (you're adding URLs from the back)
        if len(STORY_URLS) == sl:
            break

        pickle.dump(STORY_URLS, open('ficly-story-urls.pickle', 'wb'))
        if FICLY_PAGE == 0:
            FICLY_PAGE = 1
        else:
            FICLY_PAGE = urlparse.urlparse(FICLY_NEXT).query.split('=')[1]
        print 'Saved page {0}, up to {1} URLs'.format(FICLY_PAGE, len(STORY_URLS))

        n = s.find('a', rel='next')
        if n is None:
            FICLY_NEXT = None
        else:
            FICLY_NEXT = urlparse.urljoin(FICLY_RECENT, n['href'])
    else:
        print 'Ficly problem: URL {0} returned status code {1}'.format(FICLY_NEXT, r.status_code)
        # Naively assume there might be a next page
        FICLY_PAGE += 1
        FICLY_NEXT = FICLY_NEXT.split('=')[0] + '={0}'.format(FICLY_PAGE)
