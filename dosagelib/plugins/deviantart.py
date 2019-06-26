# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2017 Tobias Gruetzmacher

from __future__ import absolute_import, division, print_function

from ..scraper import _ParserScraper


class DeviantArt(_ParserScraper):
    # Ugly xpath query for previous page, but it works
    imageSearch = '//a[contains(@class, "dev-page-download")]'
    prevSearch = ('//div[@class="text block"]//text()[contains(., "Prev")]/following-sibling::span//a',
                  '//div[@class="text block"]//text()[contains(., "Prev")]/following-sibling::a')

    def __init__(self, name, sub, first, last, adult=False, nav=None):
        super(DeviantArt, self).__init__('DeviantArt/' + name)

        self.baseUrl = 'https://%s.deviantart.com/' % sub
        self.stripUrl = self.baseUrl + 'art/%s'
        self.firstStripUrl = self.stripUrl % first

        # Currently only completed comics are supported
        self.url = self.stripUrl % last
        self.endOfLife = True

        self.adult = adult
        self.nav = nav

    def namer(self, imageUrl, pageUrl):
        name = pageUrl.rsplit('/', 1)[-1].split('?', 1)[0].rsplit('-', 1)
        ext = imageUrl.rsplit('.', 1)[-1]
        return '%s-%s.%s' % (name[1], name[0], ext)

    def getPrevUrl(self, url, data):
        # Missing/broken navigation links
        url = url.rsplit('/', 1)[-1].rsplit('?', 1)[0]
        if self.nav and url in self.nav:
            return self.stripUrl % self.nav[url]
        return super().getPrevUrl(url, data)


    @classmethod
    def getmodules(cls):
        return (
            cls('InOurShadow',
                'kitfox-crimson',
                'Legacy-page-1-424190315',
                last='In-Our-Shadow-page-382-763787452',
                adult=True,
                nav={
                    'Legacy-page-54-485534748': 'Legacy-page-53-485353333',
                    'Legacy-page-53-485353333': 'Legacy-page-52-485104882',
                    'Legacy-page-2-424191803': 'Legacy-page-1-424190315'
                }),
            cls('IndustrialRevelations',
                'kitfox-crimson',
                'Industrial-Revelations-preview-170390638',
                last='Industrial-Revelations-page-288-303170766',
                adult=True,
                nav={
                    'Industrial-Revelations-page-185-282604281': 'Industrial-Revelations-page-184-282339267',
                    'Industrial-revelations-no-152-213248246': 'Industrial-revelations-no-151-213246856',
                    'Industrial-revelations-no-150-213246659': 'Industrial-revelations-no-149-213119953',
                    'Industrial-revelations-no-139-210945001': 'Industrial-revelations-no-138-210639877',
                    'Industrial-revelations-no-123-204327167': 'Industrial-revelations-no-122-204012069',
                    'Industrial-revelations-no-121-204007584': 'Industrial-Revelations-no-120-203805821',
                    'Industrial-Revelations-no-119-203562132': 'Industrial-Revelations-no-118-203562028',
                    'Industrial-Revelations-no-117-203228234': 'Industrial-Revelations-no-116-203224415',
                    'Industrial-Revelations-10-178712131': 'Industrial-Revelations-9-178504708',
                    'Industrial-Revelations-1-176296710': 'Industrial-Revelations-cover-187850516',
                    'Industrial-Revelations-cover-187850516': 'Industrial-Revelations-preview-170390638'
                }),
            cls('RestoredGeneration',
                'kitfox-crimson',
                'Restored-Generation-cover-126584175',
                last='Restored-Generation-final-page-171362897',
                adult=True,
                nav={
                    'Restored-Generation-page-107-104094209': 'Restored-Generation-page-106-103367889',
                    'Restored-Generation-page-103-102978933': 'Restored-Generation-page-102-102903773',
                    'Restored-Generation-page-102-102903773': 'Restored-Generation-page-101-102812080',
                    'Restored-Generation-page-96-74505308': 'Restored-Generation-page-95-74414661'
                }),
            cls('SecondComing',
                'kitfox-crimson',
                'Second-Coming-page-1-154320736',
                last='Second-Coming-page-31-153056055',
                adult=True),
        )
