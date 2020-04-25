# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring
import json
import re

from ..scraper import _ParserScraper
from ..helpers import indirectStarter


class Tapastic(_ParserScraper):
    baseUrl = 'https://tapas.io/'
    imageSearch = '//article[contains(@class, "js-episode-article")]//img/@data-src'
    prevSearch = '//a[contains(@class, "js-prev-ep-btn")]'
    latestSearch = '//ul[contains(@class, "js-episode-list")]//a'
    starter = indirectStarter
    multipleImagesPerStrip = True
    ignoreRobotsTxt = True

    def __init__(self, name, url):
        super(Tapastic, self).__init__('Tapastic/' + name)
        self.url = self.baseUrl + 'series/' + url
        self.stripUrl = self.baseUrl + 'episode/%s'

    def fetchUrls(self, url, data, urlSearch):
        # Save link order for position-based filenames
        self.imageUrls = super().fetchUrls(url, data, urlSearch)
        return self.imageUrls

    def namer(self, imageUrl, pageUrl):
        # Construct filename from episode number and image position on page
        episodeNum = pageUrl.rsplit('/', 1)[-1]
        imageNum = self.imageUrls.index(imageUrl)
        imageExt = pageUrl.rsplit('.', 1)[-1]
        if len(self.imageUrls) > 1:
            filename = "%s-%d.%s" % (episodeNum, imageNum, imageExt)
        else:
            filename = "%s.%s" % (episodeNum, imageExt)
        return filename

    @classmethod
    def getmodules(cls):
        return (
            # Manually-added comics
            cls('AmpleTime', 'Ample-Time'),
            cls('NoFuture', 'NoFuture'),
            cls('OrensForge', 'OrensForge'),
            cls('RavenWolf', 'RavenWolf'),
            cls('TheCatTheVineAndTheVictory', 'The-Cat-The-Vine-and-The-Victory'),
            cls('TheGodsPack', 'The-Gods-Pack'),

            # START AUTOUPDATE
            # END AUTOUPDATE
        )
