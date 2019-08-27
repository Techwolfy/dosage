# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2017 Tobias Gruetzmacher

from __future__ import absolute_import, division, print_function

import requests

from ..helpers import indirectStarter
from ..scraper import _ParserScraper


class Katbox(_ParserScraper):
    imageSearch = ('//div[@class="webcomic-image"]//img',
                   '//div[contains(@class, "webcomic-media")]//img')
    prevSearch = '//a[contains(@class, "previous-webcomic-link")]'
    latestSearch = ('//div[@class="post-webcomic"]//a[contains(@class, "last-webcomic-link")]',
                    '//a[contains(@class, "last-webcomic-link")]')

    def __init__(self, name, sub, comic, first, last=None, adult=False, fixNames=False):
        super(Katbox, self).__init__('Katbox/' + name)

        baseUrl = 'http://%s.katbox.net/' % sub
        if sub == 'ourworld' or sub == 'bone' or sub == 'rascals':
            baseUrl = baseUrl.replace('katbox', 'katboxad')

        self.stripUrl = baseUrl + 'comics/%s/'
        if (sub == 'cervelet' or
            sub == 'ourworld' or
            sub == 'bone' or
            (sub == 'rascals' and comic == 'project-zero')):
            self.stripUrl = self.stripUrl.replace('comics', 'comic')
            self.multipleImagesPerStrip = True
        if comic:
            self.stripUrl = self.stripUrl % (comic + '/%s')

        self.firstStripUrl = self.stripUrl % first
        self.url = self.firstStripUrl

        if last:
            self.url = self.stripUrl % last
            self.starter = super().starter
            self.endOfLife = True

        if adult:
            self.adult = True

        if fixNames:
            self.namer = self.dateNamer

    def starter(self):
        # Set age-gate cookies
        if self.adult:
            ageGateCookie = requests.cookies.create_cookie(domain='.katbox.net', name='age_gate', value='18')
            self.session.cookies.set_cookie(ageGateCookie)
            self.session.get(self.url + '?webcomic_birthday=1')
        return indirectStarter(self)

    def fetchUrls(self, url, data, urlSearch):
        self.imageUrls = super().fetchUrls(url, data, urlSearch)
        # Special case for broken navigation in Addictive Science
        if url == 'http://cervelet.katbox.net/comic/addictive-science/easter-egg-5/':
            self.imageUrls = ('http://cervelet.katbox.net/wp-content/uploads/sites/11/ad.Science644.jpg',
                              'http://cervelet.katbox.net/wp-content/uploads/sites/11/ad.Science645.jpg',
                              'http://cervelet.katbox.net/wp-content/uploads/sites/11/ad.Science646.jpg',
                              'http://cervelet.katbox.net/wp-content/uploads/sites/11/ad.Science647.jpg',
                              'http://cervelet.katbox.net/wp-content/uploads/sites/11/ad.Science648.jpg')
        return self.imageUrls

    def dateNamer(self, imageUrl, pageUrl):
        page = self.getPage(pageUrl)
        postDateTime = page.xpath('//div[@class="post-details"]//time')[0].get('datetime')
        index = postDateTime.rsplit('-', 1)[0].replace(':', '-')
        title = pageUrl.rsplit('/', 2)[-2]
        if len(self.imageUrls) > 1:
            title = title + '_' + str(self.imageUrls.index(imageUrl))
        ext = imageUrl.rsplit('.', 1)[-1]
        return  "%s_%s.%s" % (index, title, ext)

    def getPrevUrl(self, url, data):
        # Special case for broken navigation in Addictive Science
        if url == self.stripUrl % 'easter-egg-5':
            return self.stripUrl % 'school-stuff-13'
        # Special case for broken navigation in False Start
        if url == self.stripUrl % 'issue-6-page-18':
            return self.stripUrl % 'issue-6-page-17'
        return super().getPrevUrl(url, data)


    @classmethod
    def getmodules(cls):
        return (
            cls('AddictiveScience', 'cervelet', 'addictive-science', 'page-1', fixNames=True),
            cls('CaribbeanBlue', 'nekonny', 'cblue', 'caribbean-blue', last='326-the-end'),
            cls('Debunkers', 'nixie', 'debunkers', 'nixie-the-debunker'),
            cls('DesertFox', 'desertfox', None, 'origins-1', adult=True, fixNames=True),
            cls('Draconia', 'razorfox', None, 'chapter-1-page-1', adult=True),
            cls('Eorah', 'hiorou', 'eorah', 'eorah-title'),
            cls('EtherealWorlds', 'sahtori', 'oasis', '1-nightly-wanderings'),
            cls('FalseStart', 'bone', 'false-start', 'issue-1-cover', adult=True, fixNames=True),
            cls('IMew', 'nekonny', 'imew', 'imew', last='addictive-imew-16'),
            cls('ItsyBitsyAdventures', 'silverblaze', 'iba', 'fight-the-machine'),
            cls('Knighthood', 'chalo', 'knighthood', 'knighthood-1'),
            cls('KnuckleUp', 'rascals', 'knuckle-up', 'knuckle-up-prologue-i', adult=True),
            cls('LasLindas', 'chalo', 'las-lindas', 'day-one', adult=True),
            cls('Olivia', 'kadath', 'olivia', 'misplaced-virtues-title-page', adult=True),
            cls('OurWorld', 'ourworld', None, 'title-page'),
            cls('Paprika', 'nekonny', 'paprika', '001-revolution'),
            cls('PracticeMakesPerfect', 'nekonny', 'pmp', '001-procrastination'),
            cls('ProjectZero', 'rascals', 'project-zero', 'project-zero-cover', adult=True),
            cls('Rascals', 'godai', 'rascals', 'rascals-cover', adult=True),
            cls('RascalsGoyoku', 'rascals', 'goyoku', 'goyoku-prologue1', adult=True),
            cls('TheEyeOfRamalach', 'avencri', 'theeye', 'boxes-and-memories'),
            cls('TheSprawl', 'snowdon', 'sprawl', 'the-sprawl-log01-print-edition-available-now', adult=True),
            cls('TruckOff', 'fox-pop', 'truck-off', 'prologue-00'),
            cls('UberQuest', 'kozmiko', 'uberquest', 'uberquest-chapter-i-temporal-adventure'),
            cls('VampireHunterBoyfriends', 'bone', 'vhb', 'vampire-hunter-boyfriends-chapter-1-cover', adult=True),

            # Comics that have left the Katbox
            #cls('ArtificialIncident', 'sage', 'ai', 'issue-one-life-changing'),
            #cls('PeterAndCompany', 'peterverse', 'peter-and-company', 'strip-1'),
            #cls('PeterAndWhitney', 'peterverse', 'peter-and-whitney', 'comic-1-graduation-day'),
            #cls('Yosh', 'sage', 'yosh', 'introduction'),
        )
