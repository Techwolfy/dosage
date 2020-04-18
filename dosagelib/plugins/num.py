# SPDX-License-Identifier: MIT
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring
from ..scraper import _ParserScraper
from .common import _WordPressScraper


class NineteenSeventySeven(_WordPressScraper):
    name = '1977'
    url = 'http://1977thecomic.com/'


class TwentyFirstCenturyFox(_ParserScraper):
	name = '21stCenturyFox'
	url = 'http://www.hirezfox.com/21cf/'
	stripUrl = url + 'd/%s.html'
	firstStripUrl = stripUrl % '20010820'
	imageSearch = '//img[contains(@src, "21cf/comics/")]'
	prevSearch = '//a[./img[contains(@src, "previous_day")]]'
	multipleImagesPerStrip = True
	ignoreRobotsTxt = True
