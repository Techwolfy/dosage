# SPDX-License-Identifier: MIT
# Copyright (C) 2019-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring
from ..scraper import _ParserScraper
from ..helpers import indirectStarter


class Derideal(_ParserScraper):
    baseUrl = 'https://derideal.com/'
    imageSearch = ('//img[contains(@class, "comic-page")]', '//img[contains(@class, "comic-pag")]')
    prevSearch = '//a[contains(@data-bs-title, "Previous")]'
    latestSearch = '//a[contains(@data-bs-title, "Latest")]'
    starter = indirectStarter

    def __init__(self, name, sub, first, last=None, multipleImagesPerStrip=False):
        if name == 'Derideal':
            super(Derideal, self).__init__(name)
        else:
            super(Derideal, self).__init__('Derideal/' + name)

        self.url = self.baseUrl + sub
        self.stripUrl = self.url + '/%s/'
        self.firstStripUrl = self.stripUrl % first
        self.startUrl = self.firstStripUrl
        self.multipleImagesPerStrip = multipleImagesPerStrip

        self.pages = {}
        self.lastChapter = ''

        if last:
            self.endOfLife = True

    def starter(self):
        indexPage = self.getPage(self.url)
        self.chapters = indexPage.xpath('//div[contains(@class, "main-episodes")]//article//a/@href')
        self.currentChapter = len(self.chapters)
        return indirectStarter(self)

    def namer(self, imageUrl, pageUrl):
        filename = pageUrl.rstrip('/').rsplit('/', 1)[-1]
        filename = filename.replace('espanol-escape-25', 'escape-26')
        filename = filename.replace('espanol-w-a-l-l-y', 'w-a-l-l-y')
        filename = filename.replace('hogar-prision', 'home-prison')
        filename = filename.replace('strip', 'pe').replace('purpurina-effect', 'pe')
        filename = filename.replace('sector-de-seguridad', 'security-sector')
        if self.multipleImagesPerStrip:
            if pageUrl not in self.pages:
                self.pages[pageUrl] = 1
            else:
                filename = 'img' + str(self.pages[pageUrl]) + '-' + filename
                self.pages[pageUrl] += 1
        if self.lastChapter != '' and pageUrl != self.lastChapter:
            self.currentChapter -= 1
            self.lastChapter = ''
        filename = 'ch' + str(self.currentChapter) + '-' + filename
        if pageUrl in self.chapters:
            self.lastChapter = pageUrl
        return filename

    def getPrevUrl(self, url, data):
        # Fix missing navigation links between chapters
        if 'nova/xen-aftermath' in url:
            return self.stripUrl % 'xen-deadlock'
        elif 'nova/xen-deadlock' in url:
            return self.stripUrl % 'xen97-end'
        return super(Derideal, self).getPrevUrl(url, data)

    @classmethod
    def getmodules(cls):
        return (
            cls('Derideal', 'derideal', 'chimeras-cover'),
            cls('Legacy', 'derideal-legacy', 'the-dream-cover', last='derideal-is-on-hiatus'),
            cls('LostMemories', 'lost-memories', 'lost-memories-pixi', multipleImagesPerStrip=True),
            cls('LRE', 'RLE', 'the-leyend-of-the-rose-cover', last='lre-47-ending'),
            cls('Nova', 'nova', 'xen-prelude-cover', multipleImagesPerStrip=True),
            cls('ProjectPrime', 'project-prime', 'custus-part-i-cover'),
            cls('PurpurinaEffect', 'purpurina-effect', 'purpurina-effect-cover'),
            cls('TheVoid', 'the-void', 'the-void-cover', last='arma-2-42-end'),
        )
