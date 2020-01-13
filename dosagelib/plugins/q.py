# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring

from __future__ import absolute_import, division, print_function

from re import compile, escape
from ..scraper import _BasicScraper, _ParserScraper
from ..util import tagre


class QuantumVibe(_ParserScraper):
    url = 'https://www.quantumvibe.com/'
    stripUrl = url + 'strip?page=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//img[contains(@src, "disppageV3?story=qv")]'
    prevSearch = '//a[./img[contains(@src, "nav/prevstrip")]]'


class QuestionableContent(_ParserScraper):
    url = 'http://www.questionablecontent.net/'
    stripUrl = url + 'view.php?comic=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//img[contains(@src, "comics/")]'
    prevSearch = '//a[text()="Previous"]'
    help = 'Index format: n (unpadded)'


class Qwantz(_BasicScraper):
    baseUrl = 'http://www.qwantz.com/'
    url = baseUrl + 'index.php'
    rurl = escape(baseUrl)
    stripUrl = url + '?comic=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = compile(tagre("img", "src", r'(%scomics/[^"]+)' % rurl))
    prevSearch = compile(tagre("a", "href", r'(%sindex\.php\?comic=\d+)' % rurl, before="prev"))
    help = 'Index format: n'
