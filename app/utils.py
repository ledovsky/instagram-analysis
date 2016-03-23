import csv
import requests
import json


def get_json(url, params=None):
    '''
    Wrapper around requests.get with custom header and json.loads
    todo: error handling
    '''

    headers = {
        'Cache-Control': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 39.0.2171.95 Safari/537.36',
        'Referrer': 'https://www.google.com/',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ru-RU,en-US,en;q=0.8'
    }
    r = requests.get(url, params=params, headers=headers)
    return json.loads(r.text)


class DictUnicodeProxy(object):
    '''
    This wrapper class is used to write dicts with unicode to csv files
    '''
    def __init__(self, d):
        self.d = d

    def __iter__(self):
        return self.d.__iter__()

    def get(self, item, default=None):
        i = self.d.get(item, default)
        if isinstance(i, unicode):
            return i.encode('utf-8')
        return i


def write_dict_list(dicts, path):
    '''
    Function to write dict list as csv file
    '''
    keys = dicts[0].keys()
    with open(path, 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        for d in dicts:
            dict_writer.writerow(DictUnicodeProxy(d))
