# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2017 Tobias Gruetzmacher

from __future__ import absolute_import, division, print_function

from re import compile, escape

from ..scraper import _BasicScraper, _ParserScraper
from ..helpers import bounceStarter, indirectStarter, xpath_class
from ..util import tagre
from .common import (_ComicControlScraper, _WordPressScraper, _WPNaviIn,
                     WP_LATEST_SEARCH)


class Lackadaisy(_ParserScraper):
    url = 'https://www.lackadaisy.com/comic.php'
    stripUrl = url + '?comicid=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//div[@id="content"]/img'
    prevSearch = '//div[@class="prev"]/a'
    nextSearch = '//div[@class="next"]/a'
    help = 'Index format: n'
    starter = bounceStarter

    def namer(self, imageUrl, pageUrl):
        # Use comic id for filename
        num = pageUrl.rsplit('=', 1)[-1]
        ext = imageUrl.rsplit('.', 1)[-1]
        return 'lackadaisy_%s.%s' % (num, ext)


class Laiyu(_WordPressScraper):
    url = 'http://www.flowerlarkstudios.com/comicpage/preliminary-concepts/welcome/'
    firstStripUrl = url
    latestSearch = WP_LATEST_SEARCH
    starter = indirectStarter


class LastResort(_WordPressScraper):
    url = 'http://www.lastres0rt.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'that-sound-you-hear-is-a-shattered-stereotype'


class LeastICouldDo(_ParserScraper):
    url = 'http://www.leasticoulddo.com/'
    stripUrl = url + 'comic/%s'
    firstStripUrl = stripUrl % '20030210'
    imageSearch = '//div[@id="content-comic"]//img'
    prevSearch = '//a[@rel="prev"]'
    latestSearch = '//a[@id="latest-comic"]'
    starter = indirectStarter
    help = 'Index format: yyyymmdd'


class LetsSpeakEnglish(_ComicControlScraper):
    url = 'http://www.marycagle.com'


class LifeAintNoPonyFarm(_WordPressScraper):
    url = 'http://sarahburrini.com/en/'
    firstStripUrl = url + 'comic/my-first-webcomic/'
    multipleImagesPerStrip = True


class LifeAsRendered(_ParserScraper):
    # Reverse navigation doesn't work properly, so search forward instead
    stripUrl = 'http://kittyredden.com/archive/lifeasrendered/%s'
    url = stripUrl % 'lar01'
    firstStripUrl = stripUrl % 'lar05/lar0578'
    imageSearch = '//div[@class="comic"]//img'
    prevSearch = ('//a[text()="NEXT"]',
                  '//a[text()="NEXT ACT"]',
                  '//a[text()="THE END"]')
    textSearch = '//div[@class="description"]//text()'
    adult = True
    endOfLife = True
    nav = {
        'lar01/lar0104': 'lar01/lar0105',
        'lar01/lar0117': 'lar01/lar0118',
        'lar03-A/lar0352': 'lar03-A/lar0353',
        'lar03-A/lar0357': 'lar03-A/lar0358',
        'lar03ex/lar03ex08': 'lar03ex/lar03ex09',
        'lar03ex/lar03ex09': 'lar03ex/lar03ex10',
        'lar04/lar0459': 'lar04ex',
        'lar05/lar0503': 'lar05/lar0504',
        'lar05/lar0528': 'lar05/lar0529',
        'lar05/lar0552': 'lar05/lar0553'
    }

    def namer(self, imageUrl, pageUrl):
        # Fix inconsistent filenames
        filename = imageUrl.rsplit('/', 1)[-1]
        filename = filename.replace('ReN', 'N').replace('N01P', 'A02S')
        if filename == 'A05Pex.png':
            filename = 'A05P28ex.png'
        return filename

    def imageUrlModifier(self, imageUrl, data):
        # Fix broken image links
        imageUrl = imageUrl.replace('A03S0.png', 'A03S09.png')
        imageUrl = imageUrl.replace('A04P0.png', 'A04P05.png')
        imageUrl = imageUrl.replace('A05P05c.png', 'A05P04c.png')
        return imageUrl

    def getPrevUrl(self, url, data):
        # Fix broken navigation links
        segments = url.rstrip('/').rsplit('/', 2)
        url = segments[1] + '/' + segments[2]
        if self.nav and url in self.nav:
            return self.stripUrl % self.nav[url]
        return super().getPrevUrl(url, data)

    def fetchText(self, url, data, textSearch, optional):
        # Save final summary text
        if url == self.firstStripUrl:
            url = self.stripUrl % 'larend'
            data = self.getPage(url)
            return super().fetchText(url, data, textSearch, optional)
        return None


class LittleGamers(_BasicScraper):
    url = 'http://www.little-gamers.com/'
    stripUrl = url + '%s/'
    firstStripUrl = stripUrl % '2000/12/01/99'
    imageSearch = compile(tagre("img", "src", r'(http://little-gamers\.com/comics/[^"]+)'))
    prevSearch = compile(tagre("a", "href", r'(http://www\.little-gamers\.com/[^"]+)', before="comic-nav-prev-link"))
    help = 'Index format: yyyy/mm/dd/name'


class LittleTales(_ParserScraper):
    url = 'http://www.little-tales.com/'
    stripUrl = url + 'index.php?Strip=%s'
    firstStripUrl = stripUrl % '1'
    url = stripUrl % '450'
    imageSearch = '//img[contains(@src, "strips/")]'
    prevSearch = '//a[./img[@alt="BACK"]]'
    nextSearch = '//a[./img[@alt="FORWARD"]]'
    starter = bounceStarter
    nav = {
        '517': '515',
        '449': '447'
    }

    def namer(self, imageUrl, pageUrl):
        page = pageUrl.rsplit('=', 1)[-1]
        ext = imageUrl.rsplit('.', 1)[-1]
        return page + '.' + ext

    def getPrevUrl(self, url, data):
        # Skip missing pages with broken navigation links
        page = url.rsplit('=', 1)[1]
        if page in self.nav:
            return self.stripUrl % self.nav[page]
        return super().getPrevUrl(url, data)



class LoadingArtist(_ParserScraper):
    url = 'http://www.loadingartist.com/latest'
    imageSearch = '//div[@class="comic"]//img'
    prevSearch = "//a[contains(concat(' ', @class, ' '), ' prev ')]"


class LoFiJinks(_WPNaviIn):
    url = 'http://hijinksensue.com/comic/learning-to-love-again/'
    firstStripUrl = 'http://hijinksensue.com/comic/lo-fijinks-everything-i-know-anout-james-camerons-avatar-movie/'
    endOfLife = True


class LookingForGroup(_ParserScraper):
    url = 'https://www.lfg.co/'
    stripUrl = url + 'page/%s/'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//div[@id="comic-img"]//img'
    prevSearch = '//a[@class="comic-nav-prev"]'
    latestSearch = '//div[@id="feature-lfg-footer"]/a[contains(@href, "page/")]'
    starter = indirectStarter
    help = 'Index format: nnn'

    def namer(self, imageUrl, pageUrl):
        page = pageUrl.rstrip('/').rsplit('/', 1)[-1]
        page = page.replace('2967', '647')
        ext = imageUrl.rsplit('.', 1)[-1]
        return page + '.' + ext
