# SPDX-License-Identifier: MIT
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring
from ..scraper import _ParserScraper
from ..helpers import indirectStarter
from .common import _WordPressScraper, _WPWebcomic


class YAFGC(_WordPressScraper):
    baseUrl = 'https://www.yafgc.net/'
    url = baseUrl + '?latest'
    stripUrl = baseUrl + 'comic/%s'
    firstStripUrl = stripUrl % 'bob-meets-gren'

    def __init__(self, name):
        super().__init__(name)
        self.session.add_throttle('www.yafgc.net', 3.0, 15.5)


class YearInHereafter(_ParserScraper):
    url = 'https://www.yihcomic.com/'
    stripUrl = url + 'pages/page%s.php'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//img[@class="page"]'
    prevSearch = '//a[./img[contains(@src, "prev")]]'
    latestSearch = '//a[./img[contains(@src, "latest")]]'
    starter = indirectStarter

    def getPrevUrl(self, url, data):
        # Fix broken page
        if 'page246.php' in url:
            return self.stripUrl % '245'
        return super(YearInHereafter, self).getPrevUrl(url, data)

    def fetchUrls(self, url, data, urlSearch):
        # Save link order for position-based filenames
        imageUrls = super().fetchUrls(url, data, urlSearch)
        # Fix broken page
        if 'page246.php' in url:
            imageUrls[0] = imageUrls[0].replace('247', '246')
        return imageUrls



class YoshSaga(_WPWebcomic):
    url = 'https://www.yoshsaga.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'introduction'
