# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2016 Tobias Gruetzmacher

from __future__ import absolute_import, division, print_function

from .common import _ParserScraper


class NamirDeiter(_ParserScraper):
    imageSearch = '//img[contains(@src, "comics/")]'
    prevSearch = ('//a[@rel="prev"]',
                  '//a[./img[contains(@src, "previous")]]',
                  '//a[contains(text(), "Previous")]')

    def __init__(self, name, baseUrl, first, last=None):
        if name == 'NamirDeiter':
            super(NamirDeiter, self).__init__(name)
        else:
            super(NamirDeiter, self).__init__('NamirDeiter/' + name)

        self.url = 'http://' + baseUrl + '/'
        self.stripUrl = self.url + 'comics/index.php?date=%s'

        if first:
            self.firstStripUrl = self.stripUrl % first
        else:
            self.firstStripUrl = self.url + 'comics/'

        if last:
            self.url = self.stripUrl % last
            self.endOfLife = True

    @classmethod
    def getmodules(cls):
        return (
            cls('ApartmentForTwo', 'www.apartmentfor2.com', None),
            cls('NamirDeiter', 'www.namirdeiter.com', None, last='20150410'),
            cls('NicoleAndDerek', 'nicoleandderek.com', None),
            cls('OneHundredPercentCat', 'ndunlimited.com/100cat', None, last='20121001'),
            cls('SpareParts', 'www.sparepartscomics.com', '20031022', last='20080331'),
            cls('TheNDU', 'www.thendu.com', None),
            cls('WonderKittens', 'wonderkittens.com', None),
            cls('YouSayItFirst', 'www.yousayitfirst.com', '20040220', last='20130125')
        )


class UnlikeMinerva(_ParserScraper):
    name = 'NamirDeiter/UnlikeMinerva'
    baseUrl = 'http://www.unlikeminerva.com/archive/index.php'
    stripUrl = baseUrl + '?week=%s'
    url = stripUrl % '127'
    firstStripUrl = stripUrl % '26'
    imageSearch = '//img[contains(@src, "archive/")]'
    prevSearch = '//a[./img[contains(@src, "previous")]]'
    multipleImagesPerStrip = True
    endOfLife = True
