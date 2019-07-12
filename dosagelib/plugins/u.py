# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2017 Tobias Gruetzmacher

from __future__ import absolute_import, division, print_function

from re import compile, escape

from ..scraper import _BasicScraper, _ParserScraper
from ..helpers import indirectStarter
from ..util import tagre
from .common import _WordPressScraper, _WPNavi


class Underling(_WPNavi):
    url = 'http://underlingcomic.com/'
    firstStripUrl = url + 'page-one/'


class Undertow(_BasicScraper):
    url = 'http://undertow.dreamshards.org/'
    imageSearch = compile(tagre("img", "src", r'([^"]+\.jpg)'))
    prevSearch = compile(r'href="(.+?)".+?teynpoint')
    latestSearch = compile(r'href="(.+?)".+?Most recent page')
    starter = indirectStarter


class UnicornJelly(_BasicScraper):
    baseUrl = 'http://unicornjelly.com/'
    url = baseUrl + 'uni666.html'
    stripUrl = baseUrl + 'uni%s.html'
    firstStripUrl = stripUrl % '001'
    imageSearch = compile(r'</TABLE>(?:<FONT COLOR="BLACK">)?<IMG SRC="(images/[^"]+)" WIDTH=')
    prevSearch = compile(r'<A HREF="(uni\d{3}[bcs]?\.html)">(<FONT COLOR="BLACK">)?<IMG SRC="images/back00\.gif"')
    help = 'Index format: nnn'


class Unsounded(_ParserScraper):
    url = 'https://unsoundedupdates.tumblr.com/'
    baseUrl = 'http://www.casualvillain.com/Unsounded/'
    stripUrl = baseUrl + 'comic/ch%s/ch%s_%s.html'
    firstStripUrl = stripUrl % ('01', '01', '01')
    imageSearch = '//img[contains(@src, "pageart/")]'
    prevSearch = '//a[contains(@class, "back")]'
    multipleImagesPerStrip = True
    help = 'Index format: chapter-number'

    def starter(self):
        # Resolve double redirect for current page
        page = self.getPage(self.url)
        redirect = page.xpath('//a[.//img[@alt="Click Here for the newest page!"]]')[0]
        page = self.getPage(redirect.get('href'))
        redirect = page.xpath('//meta[@http-equiv="refresh"]')[0]
        return redirect.get('content').split('URL=', 1)[-1]

    def getPrevUrl(self, url, data):
        # Fix missing navigation link
        if url == self.baseUrl + 'comic/ch13/you_let_me_fall.html':
            return self.stripUrl % ('13', '13', '85')
        return super().getPrevUrl(url, data)

    def getIndexStripUrl(self, index):
        # Get comic strip URL from index
        chapter, num = index.split('-')
        return self.stripUrl % (chapter, chapter, num)


class UrgentTransformationCrisis(_WordPressScraper):
    url = 'http://www.catomix.com/utc/'
    firstStripUrl = url + 'comic/cover1'

    def namer(self, imageUrl, pageUrl):
        # Fix inconsistent filenames
        filename = imageUrl.rsplit('/', 1)[-1].rsplit('?', 1)[0]
        return filename.replace('FVLYHD', 'LYHDpage').replace('UTC084web', '20091218c')
