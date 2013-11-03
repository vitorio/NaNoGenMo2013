import pickle
import urlparse
import json
import requests
from BeautifulSoup import BeautifulSoup
import html2text

STORY_URLS = pickle.load(open('ficly-story-urls.pickle', 'rb'))
skip_to = 18173
print len(STORY_URLS)

for ficlet in STORY_URLS:
    # Skip for interrupted scrapes
    if skip_to:
        if int(ficlet.split('/')[-1]) == skip_to:
            skip_to = False
            continue
        else:
            continue

    r = requests.get(ficlet)
    if r.status_code == requests.codes.ok:
        s = BeautifulSoup(r.text)

        prequels = s.find('div', {'id': 'prequels'}).findAll('a', rel='bookmark previous')
        sequels = s.find('div', {'id': 'sequels'}).findAll('a', rel='bookmark previous')
        if len(sequels) == 0 and len(prequels) == 0:
            print '{0} has no prequels or sequels'.format(ficlet)
            continue

        ficly_prequels = []
        for p in prequels:
            ficly_prequels.append({'ficly_prequel_int': int(p['href'].split('/')[-1]), 'ficly_prequel_url': p['href'], 'ficly_prequel_title': p.text})

        ficly_sequels = []
        for p in sequels:
            ficly_sequels.append({'ficly_sequel_int': int(p['href'].split('/')[-1]), 'ficly_sequel_url': p['href'], 'ficly_sequel_title': p.text})

        f = s.find('a', rel='self bookmark')
        ficly_story_url = f['href']
        ficly_story_int = int(ficly_story_url.split('/')[-1])
        ficly_story_title = f.text

        f = s.find('a', {'class': 'fn'})
        ficly_author_url = f['href']
        ficly_author_nickname = f.text

        f = s.find('img', {'class': 'photo'})
        ficly_author_avatar_url = urlparse.urljoin('http://ficly.com/', f['src']).split('?')[0]

        f = s.find('div', {'class': 'entry-content'})
        ficly_story = html2text.html2text(unicode(BeautifulSoup(f.renderContents(), convertEntities=BeautifulSoup.ALL_ENTITIES)))
        ficly_story = ficly_story.replace('\n\n', '\r\r')
        ficly_story = ficly_story.replace('\n', ' ')
        ficly_story = ficly_story.replace('\r\r', '\n\n')

        ficly = {'ficly_story_int': ficly_story_int,
                 'ficly_story_url': ficly_story_url,
                 'ficly_story_title': ficly_story_title,
                 'ficly_author_url': ficly_author_url,
                 'ficly_author_avatar_url': ficly_author_avatar_url,
                 'ficly_author_nickname': ficly_author_nickname,
                 'ficly_prequels': ficly_prequels,
                 'ficly_sequels': ficly_sequels,
                 'ficly_story': ficly_story}

        print ficly_story_int

        j = open('ficly-story-{0}.json'.format(ficly_story_int), 'wb')
        j.write(json.dumps(ficly))
    else:
        print 'Ficly problem: URL {0} returned status code {1}'.format(ficlet, r.status_code)
