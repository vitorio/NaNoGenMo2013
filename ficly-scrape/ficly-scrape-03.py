import json
import os
import pickle

json_count = 0

for a in os.listdir('.'):
    if os.path.isfile(a):
        if os.path.splitext(a)[1] == '.json':
            f = open(a, 'rb')
            json_count += 1
            ficly = json.loads(f.read())
            if len(ficly['ficly_prequels']) > 1:
                print '{0} has {1} prequels'.format(ficly['ficly_story_int'], len(ficly['ficly_prequels']))
            f.close()

print json_count

STORY_URLS = pickle.load(open('ficly-story-urls.pickle', 'rb'))
print len(STORY_URLS)

