# SPDX-License-Identifier: MIT
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring
from ..scraper import _ParserScraper
from ..helpers import bounceStarter, indirectStarter
from .common import _WordPressSpliced


class Vexxarr(_ParserScraper):
    baseUrl = 'http://www.vexxarr.com/'
    url = baseUrl + 'Index.php'
    stripUrl = baseUrl + 'archive.php?seldate=%s'
    firstStripUrl = stripUrl % '010105'
    imageSearch = '//p/img'
    prevSearch = '//a[./img[contains(@src, "previous")]]'
    nextSearch = '//a[./img[contains(@src, "next")]]'
    starter = bounceStarter

    def namer(self, imageUrl, pageUrl):
        page = pageUrl.rsplit('=', 1)[-1]
        return '20%s-%s-%s' % (page[4:6], page[0:2], page[2:4])


class VGCats(_ParserScraper):
    url = 'https://www.vgcats.com/comics/'
    stripUrl = url + '?strip_id=%s'
    firstStripUrl = stripUrl % '0'
    imageSearch = '//table//img[contains(@src, "images/") and not(contains(@src, "patreon"))]'
    prevSearch = '//a[img[contains(@src, "back.")]]'
    help = 'Index format: n (unpadded)'


class VickiFox(_ParserScraper):
    url = 'http://www.vickifox.com/comic/strip'
    stripUrl = url + '?id=%s'
    firstStripUrl = stripUrl % '001'
    imageSearch = '//img[contains(@src, "comic/")]'
    prevSearch = '//button[@id="btnPrev"]/@value'

    def getPrevUrl(self, url, data):
        return self.stripUrl % self.getPage(url).xpath(self.prevSearch)[0]


class ViiviJaWagner(_ParserScraper):
    url = 'http://www.hs.fi/viivijawagner/'
    imageSearch = '//meta[@property="og:image"]/@content'
    prevSearch = '//a[d:class("prev")]'
    latestSearch = '//div[d:class("cartoon-content")]//a'
    starter = indirectStarter
    lang = 'fi'

    def namer(self, image_url, page_url):
        return page_url.rsplit('-', 1)[1].split('.')[0]


class VirmirWorld(_ParserScraper):
    url = 'http://world.virmir.com/'
    stripUrl = url + 'comic.php?story=%s&page=%s'
    firstStripUrl = stripUrl % ('1', '1')
    imageSearch = '//div[@class="comic"]//img'
    prevSearch = '//a[contains(@class, "prev")]'

    def getIndexStripUrl(self, index):
        index = index.split('-')
        return self.stripUrl % (index[0], index[1])


class VisionHaze(_ParserScraper):
    url = 'http://www.visionhaze.com/index.php'
    stripUrl = url + '?p=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//div[@class="page"]//img'
    prevSearch = '//a[contains(text(), "‹")]'


class VixenLogic(_WordPressSpliced):
    url = 'https://www.vixenlogic.com/'
    stripUrl = url + '%s/'
    firstStripUrl = stripUrl % 'vl0001'
    imageSearch = '//div[@id="one-comic-option"]//span[@class="default-lang"]//img'
    adult = True


class Vreakerz(_ParserScraper):
    url = 'http://vreakerz.angrykitten.nl/'
    stripUrl = url + '/Stories/read/%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//img[contains(@src, "storypages")]'
    prevSearch = '//a[@class="btn-prior"]'
