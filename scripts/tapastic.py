#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2017 Tobias Gruetzmacher
"""
Script to get a list of Tapastic comics and save the info in a
JSON file for further processing.
"""
from __future__ import absolute_import, division, print_function

from six.moves.urllib.parse import urlsplit, parse_qs

from scriptutil import ComicListUpdater
from dosagelib.util import check_robotstxt


class TapasticUpdater(ComicListUpdater):
    def collect_results(self):
        # Retrieve the first 10 top comics list pages
        url = 'https://tapas.io/comics?browse=ALL&sort_type=LIKE&pageNumber='
        count = 10

        data = [self.get_url(url + str(i), robot=False) for i in range(0, count)]
        for page in data:
            for comiclink in page.xpath('//a[@class="preferred title"]'):
                comicurl = comiclink.attrib['href']
                name = comiclink.text
                self.add_comic(name, comicurl)

    def get_entry(self, name, url):
        shortName = name.replace(' ', '').replace('\'', '')
        titleNum = int(parse_qs(urlsplit(url).query)['title_no'][0])
        url = url.rsplit('/', 1)[0].replace('/series/', '')
        return u"cls('%s', '%s', %d)," % (shortName, url, titleNum)


if __name__ == '__main__':
    TapasticUpdater(__file__).run()
