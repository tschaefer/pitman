# -*- coding: utf-8 -*-

import feedparser
import requests
from clint.textui import progress


class Pitman(object):

    PODCASTS = {
        'CLR': 'http://www.cl-rec.com/pod/podcast',
        'Drumcode': 'http://drumcode.libsyn.com/rss',
        'Mobilee': 'http://mobilee-records.de/podcast/feed.xml',
        'Sleaze': 'http://sleazerecordsuk.podbean.com/feed/',
    }

    def __init__(self, podcast='CLR'):
        if podcast not in self.PODCASTS.keys():
            raise IndexError("'%s' unknown Podcast" % (podcast))
        self.podcast = podcast
        self.url = self.PODCASTS[podcast]

    def parse(self):
        raw = feedparser.parse(self.url)
        if raw['status'] != 200 and raw['status'] != 301:
            raise RuntimeError("Failed to fetch RSS feed '%s',"
                               "'http error %s'" % (self.url, raw['status']))

        self.feed = []
        for chunk in raw['entries']:
            if chunk['title'].startswith('CLR Podcast |'):
                title = chunk['title'].replace(u'\xa0', u' ')
                __, num, artist = title.split(' | ')
            elif chunk['title'].startswith('CLR Podcast I'):
                title = chunk['title'].replace(u'\xa0', u' ')
                __, num, artist = title.split(' I ')
            elif chunk['title'].startswith('DCR'):
                num, __, artist = chunk['title'].partition(' - ')
                num = num.lstrip('DCR')
                artist = artist.partition(' - ')[2]
            elif chunk['title'].startswith('mobileepod'):
                artist = chunk['subtitle'].lstrip('presented by')
                num = int(chunk['title'].split(' ')[1].rstrip(':'))
            elif chunk['title'].find('Sleaze Podcast') != -1:
                artist, num = chunk['title'].split(' - Sleaze Podcast ')
                num = num[:3]
            else:
                continue

            if self.podcast == 'Drumcode' or self.podcast == 'Sleaze':
                link = chunk['links'][1]['href']
            else:
                link = chunk['links'][0]['href']

            date = chunk['published_parsed']
            entry = {'num': int(num), 'artist': artist, 'link': link,
                     'date': date}
            self.feed.append(entry)

    def show(self, limit=0, verbose=False):
        total = len(self.feed)
        if limit < 0 or limit > total:
            raise ValueError("'%d' limit is out of range")

        for num, entry in enumerate(self.feed):
            if limit == num:
                break
            if not verbose:
                print '%03d - %s [%d]' % (entry['num'],
                                          entry['artist'].encode('utf-8'),
                                          entry['date'].tm_year)
            else:
                print '%03d - %s [%d] - %s' % (entry['num'],
                                               entry['artist'].encode('utf-8'),
                                               entry['date'].tm_year,
                                               entry['link'].encode('utf-8'))

    def search(self, terms):
        for term in terms:
            for entry in self.feed:
                if entry['artist'].lower().find(term.lower()) != -1:
                    print ("%03d - %s [%d]" % (entry['num'], entry['artist'],
                           entry['date'].tm_year))

    def get(self, episodes):
        for episode in episodes:
            for c, e in enumerate(self.feed):
                if e['num'] == episode:
                    episode = c
                    break
            try:
                url = self.feed[episode]['link']
            except IndexError:
                raise IndexError("No such episode found, '%d'" % (episode))
            filename = url.split('/')[-1]
            stream = requests.get(url, stream=True)
            total_length = int(stream.headers.get('content-length'))

            with open(filename, 'wb') as f:
                for chunk in progress.bar(stream.iter_content(chunk_size=1024),
                                          label=url,
                                          expected_size=(total_length/1024)+1):
                    if chunk:
                        f.write(chunk)
