# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2017 Tobias Gruetzmacher

from __future__ import absolute_import, division, print_function

from re import compile, escape

from ..scraper import _BasicScraper, _ParserScraper
from ..util import tagre
from .common import _WordPressScraper, _WPNavi


class IAmArg(_BasicScraper):
    url = 'http://iamarg.com/'
    rurl = escape(url)
    stripUrl = url + '%s/'
    firstStripUrl = stripUrl % '2011/05/08/05082011'
    imageSearch = compile(tagre("img", "src", r'(//iamarg.com/comics/\d+-\d+-\d+[^"]+)'))
    prevSearch = compile(tagre("a", "href", r'(%s\d+/\d+/\d+/[^"]+)' % rurl, after="prev"))
    help = 'Index format: yyyy/mm/dd/stripname'


class ICanBarelyDraw(_BasicScraper):
    url = 'http://www.icanbarelydraw.com/comic/'
    rurl = escape(url)
    stripUrl = url + '%s'
    firstStripUrl = stripUrl % '39'
    imageSearch = compile(tagre("img", "src", r'(%scomics/\d+-\d+-\d+-[^"]+)' % rurl))
    prevSearch = compile(tagre("a", "href", r'(%s\d+)' % rurl))
    help = 'Index format: number'


class IDreamOfAJeanieBottle(_WordPressScraper):
    url = 'http://jeaniebottle.com/'


class InOurShadow(_ParserScraper):
    # DeviantArt scraper; ugly xpath query for previous page, but it works
    url = 'https://kitfox-crimson.deviantart.com/art/In-Our-Shadow-page-382-763787452'
    firstStripUrl = 'https://kitfox-crimson.deviantart.com/art/Legacy-page-1-424190315'
    imageSearch = '//a[contains(@class, "dev-page-download")]'
    prevSearch = ('//div[@class="text block"]//text()[contains(., "Prev")]/following-sibling::span//a',
                  '//div[@class="text block"]//text()[contains(., "Prev")]/following-sibling::a')
    adult = True
    endOfLife = True

    def namer(self, imageUrl, pageUrl):
        name = pageUrl.rsplit('/', 1)[-1].split('?', 1)[0].rsplit('-', 1)
        ext = imageUrl.rsplit('.', 1)[-1]
        return '%s-%s.%s' % (name[1], name[0], ext)

    def getPrevUrl(self, url, data):
        # Missing/broken navigation links
        url = url.rsplit('?', 1)[0]
        if url == 'https://kitfox-crimson.deviantart.com/art/Legacy-page-54-485534748':
            return 'https://kitfox-crimson.deviantart.com/art/Legacy-page-53-485353333'
        elif url == 'https://kitfox-crimson.deviantart.com/art/Legacy-page-53-485353333':
            return 'https://kitfox-crimson.deviantart.com/art/Legacy-page-52-485104882'
        elif url == 'https://kitfox-crimson.deviantart.com/art/Legacy-page-2-424191803':
            return 'https://kitfox-crimson.deviantart.com/art/Legacy-page-1-424190315'
        return super().getPrevUrl(url, data)


class InternetWebcomic(_WPNavi):
    url = 'http://www.internet-webcomic.com/'
    stripUrl = url + '?p=%s'
    firstStripUrl = stripUrl % '30'
    help = 'Index format: n'


class IrregularWebcomic(_BasicScraper):
    url = 'http://www.irregularwebcomic.net/'
    stripUrl = url + '%s.html'
    firstStripUrl = stripUrl % '1'
    imageSearch = compile(r'<img .*src="(.*comics/.*(png|jpg|gif))".*>')
    prevSearch = compile(r'<a href="(/\d+\.html|/cgi-bin/comic\.pl\?comic=\d+)">Previous ')
    help = 'Index format: nnn'


class IslaAukate(_ParserScraper):
    url = 'https://overlordcomic.com/archive/default/latest'
    stripUrl = 'https://overlordcomic.com/archive/default/pages/%s'
    firstStripUrl = stripUrl % '001'
    imageSearch = '//div[@id="comicpage"]/img'
    prevSearch = '//nav[@class="comicnav"]/a[text()="Prev"]'


class IslaAukateColor(_ParserScraper):
    url = 'https://overlordcomic.com/archive/color/latest'
    stripUrl = 'https://overlordcomic.com/archive/color/pages/%s'
    firstStripUrl = stripUrl % '001'
    imageSearch = '//div[@id="comicpage"]/img'
    prevSearch = '//nav[@class="comicnav"]/a[text()="Prev"]'

    def namer(self, imageUrl, pageUrl):
        # Fix filenames of early comics
        filename = imageUrl.rsplit('/', 1)[-1]
        if filename[0].isdigit():
            filename = 'Aukate' + filename
        return filename


class ItsWalky(_WordPressScraper):
    url = 'http://www.itswalky.com/'
