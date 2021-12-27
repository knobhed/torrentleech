#VERSION: 1.1

import os
import json
import tempfile
import requests
from novaprinter import prettyPrinter
cookies = {'tluid':'1848517', 'tlpass':'8eabc8fa46bb347abd75eb88d2c03576f6bdb01e'}

class tl(object):
    url = 'https://www.torrentleech.org'
    name = 'TorrentLeech'
    supported_categories = {
        'all': [],
        'movies': [13,14,37,47,15],
        'tv': [26,27,32],
        'anime': [34,35],
        'games': [17],
        'software': [23],
        'music': [31],
        'books': [45]
    }

    def download_file(self, url):
        file, path = tempfile.mkstemp()
        file = os.fdopen(file, 'wb')
        response = requests.get(url, cookies=cookies)
        data = response.content
        file.write(data)
        file.close()
        return path + ' ' + url

    def download_torrent(self, info):
        print(self.download_file(info))

    def search(self, what, cat='all'):
        if cat == 'all':
            query = self.url + '/torrents/browse/list/exact/1/query/' + what
        else:
            categories = ','.join(str(x) for x in self.supported_categories[cat.lower()])
            query = self.url + '/torrents/browse/list/categories/' + categories + '/exact/1/query/' + what

        response = requests.get(query, cookies=cookies)
        obj = json.loads(response.text)['torrentList']
        results = list(filter(lambda x: x['seeders'] > 1, obj))

        for item in results:
            res = {
                'link': self.url + '/download/' + item['fid'] + '/' + item['filename'],
                'name': item['name'],
                'size': str(item['size']),
                'seeds': item['seeders'],
                'leech': item['leechers'],
                'engine_url': self.url,
                'desc_link': self.url + '/torrent/' + item['fid']
            }

            prettyPrinter(res)
