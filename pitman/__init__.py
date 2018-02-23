# -*- coding: utf-8 -*-

import feedparser
import requests
from clint.textui import progress


PODCASTS = {
    'AMFM': 'http://www.cl-rec.com/pod/podcast',
    'CLR': 'http://www.cl-rec.com/pod/podcast',
    'Druckpunkt': 'https://hearthis.at/druckpunkt/rss/',
    'Drumcode': 'http://drumcode.libsyn.com/rss',
    'ElektronicForce': 'http://marcobailey.podomatic.com/rss2.xml',
    'Mobilee': 'http://mobilee-records.de/podcast/feed.xml',
    'RA': 'http://www.residentadvisor.net/xml/podcast.xml',
    'Sleaze': 'http://sleazerecordsuk.podbean.com/feed/',
    'Systematic': 'http://www.deejay-net.info/systpod/feed.xml',
    'Tronic': 'https://syndicast.co.uk/distribution/show/rss/tronic-radio',
}


class Pitman(object):

    def __init__(self, podcast='CLR'):
        if podcast not in PODCASTS.keys():
            raise IndexError("'%s' unknown Podcast" % (podcast))
        self.podcast = podcast
        self.url = PODCASTS[podcast]

    def parse(self, podcast='CLR'):
        req = requests.get(self.url)
        if req.status_code != 200:
            raise RuntimeError("Failed to fetch RSS feed '%s',"
                               "'http error %d'" % (self.url, req.status_code))
        raw = feedparser.parse(req.text)

        self.feed = []
        for chunk in raw['entries']:
            title = chunk['title']
            if podcast == 'CLR' and title.startswith('CLR Podcast |'):
                title = title.replace(u'\xa0', u' ')
                __, num, artist = title.split(' | ')
            elif podcast == 'CLR' and title.startswith('CLR Podcast I'):
                title = title.replace(u'\xa0', u' ')
                __, num, artist = title.split(' I ')
            elif title.startswith('DCR'):
                num, __, artist = title.partition(' - ')
                num = num.lstrip('DCR')
                artist = artist.partition(' - ')[2]
            elif title.startswith('mobileepod'):
                artist = chunk['subtitle'].lstrip('presented by')
                num = int(title.split(' ')[1].rstrip(':'))
            elif title.find('Sleaze Podcast') != -1:
                title = title.replace('(PT)', '-')
                artist, num = title.split(' - Sleaze Podcast ')
                num = num[:3]
            elif title.startswith('RA'):
                num = title.split('.')[1].split()[0]
                artist = chunk['author']
            elif title.startswith('Systematic'):
                num = title.split()[2][1:]
                if not num:
                    continue
                if chunk['subtitle'].find('by') != -1:
                    artist = chunk['subtitle'].split(' by ')[1]
                else:
                    artist = u'Marc Romboy'
            elif title.startswith('Elektronic Force Podcast'):
                    num = title.split()[3]
                    if title.find('with') != -1:
                        artist = title.split(' with ')[1]
                    else:
                        artist = 'Marco Bailey'
            elif title.startswith('[dppc#'):
                num = title.split()[0].rstrip(']:')[6:]
                artist = title.split(' von ')[0].split(' ', 1)[1].title()
            elif title.startswith('Tronic Radio'):
                num = title.split()[2].strip()
                artist = title.split('|')[1].strip()
            elif podcast == 'AMFM' and title.startswith('am/fm'):
                if title.find('|') > 0:
                    num = title.split('|')[1][:4]
                else:
                    num = title.split()[1]
                artist = 'Chris Liebing'
            else:
                continue

            if self.podcast in ['CLR', 'Mobilee', 'Druckpunkt', 'AMFM']:
                link = chunk['links'][0]['href']
                if self.podcast == 'Druckpunkt':
                    url = 'http://download2.hearthis.at/'
                    root = link.split('/')[3]
                    pod = link.split('/')[4]
                    link = '%s/?track=%s/%s' % (url, root, pod)
            elif self.podcast == 'Tronic':
                link = chunk['links'][0]['href']
            else:
                link = chunk['links'][1]['href']

            date = chunk['published_parsed']
            entry = {'num': int(num), 'artist': artist, 'link': link,
                     'date': date}
            self.feed.append(entry)

    def show(self, limit=0, verbose=False):
        total = len(self.feed)
        if limit < 0 or limit > total:
            raise ValueError("'%d' limit is out of range" % (limit))

        for num, entry in enumerate(self.feed):
            if limit > 0 and limit == num:
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
            filename = '%03d - %s - %d.mp3' % \
                (self.feed[episode]['num'],
                 self.feed[episode]['artist'].encode('utf-8'),
                 self.feed[episode]['date'].tm_year)
            stream = requests.get(url, stream=True)
            total_length = int(stream.headers.get('content-length'))

            with open(filename, 'wb') as f:
                for chunk in progress.bar(stream.iter_content(chunk_size=1024),
                                          label=url,
                                          expected_size=(total_length/1024)+1):
                    if chunk:
                        f.write(chunk)
