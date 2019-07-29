# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2016 Tobias Gruetzmacher

from __future__ import absolute_import, division, print_function

from re import compile, escape

from ..scraper import _BasicScraper, _ParserScraper
from ..util import tagre
from ..helpers import bounceStarter, indirectStarter
from .common import _ComicControlScraper, _WordPressScraper, _WPNaviIn


class HagarTheHorrible(_BasicScraper):
    url = 'http://www.hagarthehorrible.net/'
    stripUrl = 'http://www.hagardunor.net/comicstrips_us.php?serietype=9&colortype=1&serieno=%s'
    firstStripUrl = stripUrl % '1'
    multipleImagesPerStrip = True
    imageSearch = compile(tagre("img", "src", r'(stripus\d+/(?:Hagar_The_Horrible_?|h)\d+[^ >]+)', quote=""))
    prevUrl = r'(comicstrips_us\.php\?serietype\=9\&colortype\=1\&serieno\=\d+)'
    prevSearch = compile(tagre("a", "href", prevUrl, after="Previous"))
    help = 'Index format: number'

    def starter(self):
        """Return last gallery link."""
        url = 'http://www.hagardunor.net/comics.php'
        data = self.getPage(url)
        pattern = compile(tagre("a", "href", self.prevUrl))
        for starturl in self.fetchUrls(url, data, pattern):
            pass
        return starturl


# "Hiatus", navigation missing
class _HappyJar(_WordPressScraper):
    url = 'http://www.happyjar.com/'


class HarkAVagrant(_BasicScraper):
    url = 'http://www.harkavagrant.com/'
    rurl = escape(url)
    starter = bounceStarter
    stripUrl = url + 'index.php?id=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = compile(tagre("img", "src", r'(%s[^"]+)' % rurl,
                                after='BORDER'))
    prevSearch = compile(tagre("a", "href", r'(%sindex\.php\?id=\d+)' % rurl) +
                         tagre("img", "src", "buttonprevious.png"))
    nextSearch = compile(tagre("a", "href", r'(%sindex\.php\?id=\d+)' % rurl) +
                         tagre("img", "src", "buttonnext.png"))
    help = 'Index format: number'

    def namer(self, image_url, page_url):
        filename = image_url.rsplit('/', 1)[1]
        num = page_url.rsplit('=', 1)[1]
        return '%s-%s' % (num, filename)


class HavocInc(_WordPressScraper):
    url = 'http://www.radiocomix.com/havoc-inc/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'havoc-cover'


class HeyFox(_WordPressScraper):
    url = 'http://www.steamclaw.com/heyfox/'
    stripUrl = url + 'archives/comic/%s'
    firstStripUrl = stripUrl % '11092004'
    adult = True


class HeyKitty(_WordPressScraper):
    url = 'http://heykittycomic.com/'
    stripUrl = url + '?comic=%s'
    firstStripUrl = stripUrl % 'it-begins'


class Hipsters(_WordPressScraper):
    url = 'http://www.hipsters-comic.com/'
    firstStripUrl = 'http://www.hipsters-comic.com/comic/hip01/'


class HijinksEnsue(_WPNaviIn):
    url = 'http://hijinksensue.com/'
    latestSearch = '//a[text()="Latest HijiNKS ENSUE"]'
    firstStripUrl = 'http://hijinksensue.com/comic/who-is-your-daddy-and-what-does-he-do/'
    starter = indirectStarter


class HijinksEnsueClassic(_WPNaviIn):
    url = 'http://hijinksensue.com/comic/open-your-eyes/'
    firstStripUrl = 'http://hijinksensue.com/comic/a-soul-as-black-as-eyeliner/'
    endOfLife = True


class HijinksEnsueConvention(_WPNaviIn):
    url = 'http://hijinksensue.com/comic/emerald-city-comicon-2015-fancy-sketches-part-4/'
    firstStripUrl = 'http://hijinksensue.com/comic/whatever-dad-im-outta-here/'
    endOfLife = True


class HijinksEnsuePhoto(_WPNaviIn):
    url = 'http://hijinksensue.com/comic/emerald-city-comicon-2015-fancy-photo-comic-part-2/'
    firstStripUrl = 'http://hijinksensue.com/comic/san-diego-comic-con-fancy-picto-comic-pt-1/'
    endOfLife = True


class Holystone(_WordPressScraper):
    url = 'http://www.holystone-comic.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'prologue-page-1'
    starter = bounceStarter
    ignoreRobotsTxt = True
    indexOffset = True

    def namer(self, imageUrl, pageUrl):
        # Fix inconsistent filenames
        missingIndex = {
            'chapter-7-page-36-no-one': '372',
            'interlude-seven-fracture': '324',
            'chapter-7-page-37-tear': '317.5',
            'chapter-7-page-10-only-one': '291.5',
            'chapter-7-seeds-of-the-past': '282.5',
            'interlude-six-containment': '281.5',
            'ch-6-pg-29-midnight': '273',
            'interlude-5-intervention': '232.5',
            'ch-5-pg-22-another-way': '213',
            'chapter-5-unforgiven-tresspasses': '191',
            'interlude-four_downfall': '179.5',
            'chapter-4-old-world-order': '142',
            'interesting-things': '55',
            'chapter-two-high-seas-contention': '48',
            'the-horizon': '38',
            'belay': '33',
            'chapter-one-chance-encounters': '0'
        }
        incorrectIndex = {
            'understand',
            'trouble',
            'beasts',
            'powers',
            'dangerous',
            'good-luck',
            'children',
            'divisions',
            'qarin',
            'future-khen'
        }
        # Fix missing and incorrect indices
        page = pageUrl.rstrip('/').rsplit('/', 1)[-1]
        if page in missingIndex:
            page = missingIndex[page] + '-' + page
        elif page in incorrectIndex:
            page = '2' + page[1:]
        # Fix offset
        if page != '287-embrace':
            self.indexOffset = False
        if self.indexOffset:
            page = page.split('-', 1)
            page[0] = str(int(page[0]) + 10)
            page = page[0] + '-' + page[1]
        return page + '.' + imageUrl.rsplit('.', 1)[-1]


class Housepets(_WordPressScraper):
    url = 'http://www.housepetscomic.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = '2008/06/02/when-boredom-strikes'


class HowToBeAWerewolf(_ComicControlScraper):
    url = 'http://howtobeawerewolf.com/'
    stripUrl = url + 'comic/%s'
    firstStripUrl = stripUrl % 'coming-february-3rd'

    def namer(self, imageUrl, pageUrl):
        filename = imageUrl.rsplit('/', 1)[-1]
        if filename[0].isdigit():
            filename = filename.split('-', 1)[1]
        return filename
