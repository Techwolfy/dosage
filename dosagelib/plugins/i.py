# SPDX-License-Identifier: MIT
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring
from re import compile, escape

from ..helpers import indirectStarter
from ..scraper import _BasicScraper, _ParserScraper
from ..util import tagre
from .common import _WordPressScraper, _WPNavi, _WPWebcomic


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


class ImperialGELF(_WordPressScraper):
    url = 'http://www.imperialgelf.com/'
    stripUrl = url + '?comic=%s'
    firstStripUrl = stripUrl % 'intro-page-1'


class Inhuman(_ParserScraper):
    url = 'https://www.inhuman-comic.com/'
    stripUrl = url + 'comic%s.php'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//div[@class="page"]//img'
    prevSearch = '//a[@class="prev"]'


class InternetWebcomic(_WPNavi):
    url = 'http://www.internet-webcomic.com/'
    stripUrl = url + '?p=%s'
    firstStripUrl = stripUrl % '30'
    help = 'Index format: n'


class Inverloch(_ParserScraper):
    stripUrl = 'https://www.seraph-inn.com/view.php?story=inverloch&page=%s'
    url = stripUrl % '763'
    firstStripUrl = stripUrl % '2'
    imageSearch = '//img[@class="page"]'
    prevSearch = '//p[@class="comic-nav"]/a[text()=" Previous"]'
    multipleImagesPerStrip = True
    endOfLife = True


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

    def namer(self, imageUrl, pageUrl):
        filename = imageUrl.rsplit('/', 1)[-1]
        return filename.rsplit('_', 1)[0] + '.' + filename.rsplit('.', 1)[-1]


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
        return filename.rsplit('_', 1)[0] + '.' + filename.rsplit('.', 1)[-1]


class ISO(_ParserScraper):
    url = 'http://www.hirezfox.com/isoarchives/'
    stripUrl = url + 'd/%s.html'
    firstStripUrl = stripUrl % '20090102'
    imageSearch = '//img[contains(@src, "isoarchives/comics/")]'
    prevSearch = '//a[text()="Previous Day"]'
    ignoreRobotsTxt = True


class ItsWalky(_WordPressScraper):
    url = 'http://www.itswalky.com/'
