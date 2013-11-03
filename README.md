# NaNoGenMo2013

Code in support of NaNoGenMo 2013: <https://github.com/dariusk/NaNoGenMo>

## ficly-scrape and ficly-json

Ficly ( http://ficly.com/stories and its predecessor Ficlets http://ficlets.ficly.com/ ) is a very-short-story writing community, where you have a 1024 character limit.  There are lots of tiny stories on the site, but also, you can fork any story and write prequels and sequels to it.  Some stories have multiple prequels and sequels, like an unintentional choose-your-own-adventure.

All of the Ficly and Ficlets content is licensed CC-BY-SA.

In late May 2013, I scraped all of Ficly and dumped 13,144 stories, all of which had at least one prequel or sequel, into a matching amount of JSON files (there should be no standalone 1k character stories).  Each JSON file records the ID, URL and title of the story; the author's avatar, name and URL; the IDs and URLs of prequels and sequels; and the story content in Markdown.

The scraper (in Python) is probably a little prickly, as it's mostly uncommented, but the .zip of 13k JSON files could be dumped straight into a JSON document store and worked with directly.

## Public domain license for original code

To the extent possible under law, I waive all copyright and related or neighboring rights to
ficly-scrape/ficly-scrape-01.py and
ficly-scrape/ficly-scrape-02.py and
ficly-scrape/ficly-scrape-03.py.
This work is published from: United States.

All other text and code remains under its original license:
* scraped Ficly content: CC-BY-SA
* html2text: GPL3
* six.py: MIT
* BeautifulSoup.py: new-style BSD
* BS4: MIT
* html5lib: MIT
* Requests: Apache 2.0
