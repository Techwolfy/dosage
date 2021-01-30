# SPDX-License-Identifier: MIT
# Copyright (C) 2019-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring
from ..scraper import _ParserScraper


class TheCyantianChronicles(_ParserScraper):
    baseUrl = 'https://cyantian.net/'
    stripUrl = baseUrl + 'comic/%s/'
    imageSearch = '//div[@id="one-comic-option"]//img'
    prevSearch = '//a[@class="previous-comic"]'

    def __init__(self, name, series, first, last=None, nav=None):
        super(TheCyantianChronicles, self).__init__('TheCyantianChronicles/' + name)

        self.url = self.baseUrl + 'series/' + series + '/'
        self.firstStripUrl = self.stripUrl % first

        if last:
            self.endOfLife = True

    def isfirststrip(self, url):
        # Strip series identifier
        return super(TheCyantianChronicles, self).isfirststrip(url.rsplit('?', 1)[0])

    @classmethod
    def getmodules(cls):
        return (
            cls('Akaelae', 'akaelae', '05182003', last='01202010'),
            cls('Artwork', 'art-gallery', '07162003'),
            cls('CampusSafari', 'original-campus-safari', '10012000', last='03282008'),
            cls('CampusSafariReboot', 'campus-safari', 'campus-safari-chapter-0'),
            cls('CesileesDiary', 'cesilees-diary', '12062001-2', last='05312006'),
            cls('Darius', 'darius', '03102010', last='darius-end'),
            cls('DracoVulpes', 'draco-vulpes', 'draco-vulpes'),
            cls('GenoworksSaga', 'genoworks-saga', '07012004'),
            cls('GralenCraggHall', 'kiet', '07152002', last='chapter-6-05'),
            cls('Kiet', 'kiet-2', 'kiet-c01'),
            cls('NoAngel', 'no-angel', '08112001', last='12142006'),
            cls('RandomRamblings', 'gallery', 'cookie-war'),
            cls('SinkOrSwim', 'sink-or-swim', 'sink-or-swim', last='ricochete-and-seraphim'),
            cls('VincentAndFilaire', 'vincent-and-filaire', 'vincent-and-filaire'),
        )


class Shivae(_ParserScraper):
    url = 'https://shivae.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % '09202001'
    imageSearch = '//div[@id="one-comic-option"]//img'
    prevSearch = '//a[@class="previous-comic"]'

    def isfirststrip(self, url):
        # Strip series identifier
        return super(Shivae, self).isfirststrip(url.rsplit('?', 1)[0])


class ShivaeComics(_ParserScraper):
    baseUrl = 'https://shivae.net/'
    stripUrl = baseUrl + 'comic/%s/'
    imageSearch = '//div[@id="one-comic-option"]//img'
    prevSearch = '//a[@class="previous-comic"]'

    def __init__(self, name, series, first, last=None, nav=None):
        super(ShivaeComics, self).__init__('Shivae/' + name)

        self.url = self.baseUrl + 'series/' + series + '/'
        self.firstStripUrl = self.stripUrl % first

        if last:
            self.endOfLife = True

    def isfirststrip(self, url):
        # Strip series identifier
        return super(ShivaeComics, self).isfirststrip(url.rsplit('?', 1)[0])

    @classmethod
    def getmodules(cls):
        return (
            cls('Pure', 'pure', '2002-02-27', last='chapter-6-page-1'),
            cls('SerinFairyHunter', 'pure', 'character-serin'),
            cls('SivineBlades', 'sivine', '2002-06-30', last='2008-10-24'),
        )
