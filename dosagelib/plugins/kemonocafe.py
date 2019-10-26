# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2017 Tobias Gruetzmacher

from __future__ import absolute_import, division, print_function

from ..scraper import _ParserScraper


class KemonoCafe(_ParserScraper):
    imageSearch = '//div[@id="comic"]//img'
    prevSearch = '//a[contains(@class, "comic-nav-previous")]'

    def __init__(self, name, sub, first, last=None, adult=False):
        super(KemonoCafe, self).__init__('KemonoCafe/' + name)

        self.url = 'https://%s.kemono.cafe/' % sub
        self.stripUrl = self.url + 'comic/%s/'
        self.firstStripUrl = self.stripUrl % first

        if last:
            self.url = self.stripUrl % last
            self.endOfLife = True

        if adult:
            self.adult = True

    def namer(self, imageUrl, pageUrl):
        # Strip date from filenames
        filename = imageUrl.rsplit('/', 1)[-1]
        if filename[4] == '-' and filename[7] == '-':
            filename = filename[10:]
        if filename[0] == '-' or filename[0] == '_':
            filename = filename[1:]
        # Fix duplicate filenames
        if 'paprika' in pageUrl and '69-2' in pageUrl:
            filename = filename.replace('69', '69-2')
        elif 'rascals' in pageUrl and '89-2' in pageUrl:
            filename = filename.replace('89', '90')
        elif 'rascals' in pageUrl and '133-2' in pageUrl:
            filename = filename.replace('133', '134')
        return filename


    @classmethod
    def getmodules(cls):
        return (
            cls('CaribbeanBlue', 'cb', 'page000', last='page325'),
            cls('IMew', 'imew', 'imew00', last='imew50'),
            cls('Knighthood', 'knighthood', 'kh0001'),
            cls('LasLindas', 'laslindas', 'll0001', adult=True),
            cls('Paprika', 'paprika', 'page000'),
            cls('PracticeMakesPerfect', 'pmp', 'title-001'),
            cls('Rascals', 'rascals', 'rascals-pg-0', adult=True),
            cls('TheEyeOfRamalach', 'theeye', 'theeye-page01'),
        )
