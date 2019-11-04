# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2018 Tobias Gruetzmacher

from __future__ import absolute_import, division, print_function

import json
from re import compile, escape

from ..scraper import _BasicScraper, _ParserScraper
from ..helpers import bounceStarter, indirectStarter
from ..util import tagre
from .common import _TumblrScraper, _WordPressScraper, _WPNavi, _WPWebcomic


class CampComic(_BasicScraper):
    url = 'http://campcomic.com/comic/'
    rurl = escape(url)
    stripUrl = url + '%s'
    firstStripUrl = stripUrl % '6'
    imageSearch = compile(tagre("img", "src", r'(http://hw1\.pa-cdn\.com/camp/assets/img/katie/comics/[^"]+)'))
    prevSearch = compile(tagre("a", "href", r'(%s[^"]+)' % rurl, before="btn btnPrev"))
    help = 'Index Format: number'


class CaptainSNES(_BasicScraper):
    url = 'http://www.captainsnes.com/'
    rurl = escape(url)
    stripUrl = url + '%s/'
    firstStripUrl = stripUrl % '2001/07/10/the-mistake'
    imageSearch = compile(tagre("img", "src", r"(%scomics/[^']+)" % rurl,
                                quote="'"))
    prevSearch = compile(tagre("a", "href", r'(%s[^"]+)' % rurl) +
                         tagre("span", "class", "prev"))
    multipleImagesPerStrip = True
    help = 'Index format: yyyy/mm/dd/nnn-stripname'


class CarryOn(_ParserScraper):
    url = 'http://www.hirezfox.com/km/co/'
    stripUrl = url + 'd/%s.html'
    firstStripUrl = stripUrl % '20040701'
    imageSearch = '//div[@class="strip"]/img'
    prevSearch = '//a[text()="Previous Day"]'
    multipleImagesPerStrip = True

    def namer(self, imageUrl, pageUrl):
        # Fix filenames of early comics
        filename = imageUrl.rsplit('/', 1)[-1]
        if filename[0].isdigit():
            filename = 'co' + filename
        return filename


class CarryOnAliceBlueAndTheGardensOfQ(CarryOn):
    name = 'CarryOn/AliceBlueAndTheGardensOfQ'
    url = 'http://www.hirezfox.com/km/abgq/abgq1024/'
    firstStripUrl = url + 'd/20050401.html'

    def namer(self, imageUrl, pageUrl):
        # Fix filenames
        return 'abgq' + imageUrl.rsplit('/', 1)[-1]


class CarryOnLegendOfAnneBunny(CarryOn):
    name = 'CarryOn/LegendOfAnneBunny'
    url = 'http://www.hirezfox.com/km/loab/loab1024/'
    firstStripUrl = url + 'd/20040701.html'

    def namer(self, imageUrl, pageUrl):
        # Fix filenames of early comics
        filename = imageUrl.rsplit('/', 1)[-1]
        if filename[0].isdigit():
            filename = 'ab' + filename
        return filename


class CarryOnOfMouseAndMoon(CarryOn):
    name = 'CarryOn/OfMouseAndMoon'
    url = 'http://www.hirezfox.com/km/omam/omam1024/'
    firstStripUrl = url + 'd/20031101.html'
    ignoreRobotsTxt = True


class CarryOnPiratesOfPenumbra(CarryOn):
    name = 'CarryOn/PiratesOfPenumbra'
    url = 'http://www.hirezfox.com/km/pop/pop1024/'
    firstStripUrl = url + 'd/20040117.html'
    ignoreRobotsTxt = True


class CaseyAndAndy(_BasicScraper):
    url = 'http://www.galactanet.com/comic/'
    stripUrl = url + 'view.php?strip=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = compile(tagre("img", "src", r'(Strip\d+\.gif)'))
    prevSearch = compile(tagre("a", "href", r'(view\.php\?strip=\d+)') +
                         tagre("img", "src", r'previous\.gif'))
    help = 'Index format: number'


class CasuallyKayla(_BasicScraper):
    url = 'http://casuallykayla.com/'
    stripUrl = url + '?p=%s'
    firstStripUrl = stripUrl % '89'
    imageSearch = compile(tagre("img", "src",
                                r'(http://casuallykayla\.com/comics/[^"]+)'))
    prevSearch = compile(tagre("div", "class", r'nav-previous') +
                         tagre("a", "href", r'([^"]+)'))
    help = 'Index format: nnn'


class Catalyst(_BasicScraper):
    baseUrl = "http://catalyst.spiderforest.com/"
    rurl = escape(baseUrl)
    url = baseUrl + "comic.php?comic_id=415"
    stripUrl = baseUrl + "comic.php?comic_id=%s"
    firstStripUrl = stripUrl % '1'
    imageSearch = compile(tagre("img", "src", r'((?:%s)?comics/[^"]+)' % rurl))
    prevSearch = compile("<center>" +
                         tagre("a", "href",
                               r'(%scomic\.php\?comic_id=\d+)' % rurl))
    help = 'Index format: number'


class CatAndGirl(_ParserScraper):
    url = 'http://catandgirl.com/'
    imageSearch = '//div[@id="comic"]//img'
    prevSearch = '//a[@rel="prev"]'


class CatenaCafe(_WordPressScraper):
    name = 'CatenaManor/CatenaCafe'
    url = 'https://catenamanor.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'reboot-book1cover-small'


class CatenaManor(_ParserScraper):
    # Retrieve comic from the Internet Archive
    baseUrl = 'https://web.archive.org/web/20141027141116/http://catenamanor.com/'
    url = baseUrl + 'archives'
    stripUrl = baseUrl + '%s/'
    firstStripUrl = stripUrl % '2003/07'
    imageSearch = '//img[@class="comicthumbnail"]'
    multipleImagesPerStrip = True
    endOfLife = True
    strips = []

    def starter(self):
        # Retrieve archive links and select valid range
        archivePage = self.getPage(self.url)
        archiveStrips = archivePage.xpath('//div[@id="archivepage"]//a')
        valid = False
        for link in archiveStrips:
            if self.stripUrl % '2012/01' in link.get('href'):
                valid = True
            elif self.stripUrl % '2003/06' in link.get('href'):
                valid = False
            if valid:
                self.strips.append(link.get('href'))
        return self.strips.pop(0)

    def getPrevUrl(self, url, data):
        return self.strips.pop(0)


class CatsAndCameras(_WordPressScraper):
    url = 'http://catsncameras.com/'


class CatVersusHuman(_ParserScraper):
    url = 'http://www.catversushuman.com'
    imageSearch = '//div[@class="post-body entry-content"]//img'
    prevSearch = '//a[@id="Blog1_blog-pager-older-link"]'
    latestSearch = '//a[@rel="bookmark"]'
    starter = indirectStarter


class CavesAndCritters(_WPWebcomic):
    url = 'https://cavesandcritters.com/?ao_confirm'
    stripUrl = url + 'https://cavesandcritters.com/cnc_webcomic/%s/'
    firstStripUrl = stripUrl % '01_000'
    adult = True


class Centralia2050(_WordPressScraper):
    url = 'http://centralia2050.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'ch1cover'
    starter = bounceStarter

    def namer(self, imageUrl, pageUrl):
        page = pageUrl.rstrip('/').rsplit('/', 1)[-1].replace('chapter', 'ch')
        if 'page-' in page and 'ch-' not in page:
            page = 'ch-1-' + page
        ext = imageUrl.rsplit('.', 1)[-1]
        return page + '.' + ext


class ChainsawSuit(_WordPressScraper):
    url = 'http://chainsawsuit.com/comic/'
    stripUrl = url + 'archive/%s/'
    firstStripUrl = stripUrl % '2008/03/12/strip-338'
    prevSearch = '//img[@alt="previous"]/..'
    help = 'Index format: yyyy/mm/dd/stripname'


class Champ2010(_BasicScraper):
    baseUrl = 'http://jedcollins.com/champ2010/'
    rurl = escape(baseUrl)
    # the latest URL is hard coded since the comic is discontinued
    url = baseUrl + 'champ-12-30-10.html'
    stripUrl = baseUrl + '%s.html'
    firstStripUrl = stripUrl % 'champ1-1-10-fuck'
    imageSearch = compile(tagre("img", "src", r'(%scomics/[^"]+)' % rurl))
    prevSearch = compile(tagre("a", "href", r'(%s[^"]+)' % rurl,
                               after="Previous"))
    help = 'Index format: yy-dd-mm'


class ChannelAte(_WPNavi):
    url = 'http://www.channelate.com/'


class ChasingTheSunset(_BasicScraper):
    url = 'http://www.fantasycomic.com/'
    stripUrl = url + 'index.php?p=c%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = compile(r'(/cmsimg/.+?)".+?comic-img')
    prevSearch = compile(r'<a href="(.+?)" title="" ><img src="(images/eye-prev.png|images/cn-prev.png)"')
    help = 'Index format: n'


class Chester5000XYV(_WordPressScraper):
    url = 'http://jessfink.com/Chester5000XYV/'
    stripUrl = url + '?p=%s'
    firstStripUrl = stripUrl % '34'
    prevSearch = '//a[@rel="prev"]'
    adult = True
    help = 'Index format: n (unpadded)'

    def link_modifier(self, fromurl, tourl):
        """Bugfix for link to blog"""
        if tourl == self.stripUrl % '714':
            return self.stripUrl % '710'
        return tourl


class Chisuji(_WordPressScraper):
    url = 'http://www.chisuji.com/'
    stripUrl = url + '?p=%s'
    firstStripUrl = stripUrl % '266'
    prevSearch = '//div[@class="nav-previous"]/a'
    help = 'Index format: nnn'


class CigarroAndCerveja(_ParserScraper):
    url = 'http://www.cigarro.ca/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'reacquaintance'
    imageSearch = '//div[@id="comic"]//img',
    prevSearch = '//a[contains(text()," Prev")]',


class ClanOfTheCats(_WordPressScraper):
    url = 'http://www.cotclassic.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'coming-home-2'

    def getPrevUrl(self, url, data):
        # Fix broken navigation link
        return super(ClanOfTheCats, self).getPrevUrl(url, data).replace('/2954/', '/2002-06-22/')


class ClanOfTheCatsReunion(_WordPressScraper):
    name = 'ClanOfTheCats/Reunion'
    url = 'http://www.clanofthecats.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'cotc-reunion'


class Cloudscratcher(_ParserScraper):
    url = 'http://www.cloudscratcher.com/'
    stripUrl = url + 'comic.php?page=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//div[@id="main_content"]//img[contains(@src, "comic")]'
    prevSearch = '//a[./img[contains(@src, "previous-page")]]'
    latestSearch = '//a[@alt="Newest_Page"]'
    starter = indirectStarter


class Collar6(_TumblrScraper):
    url = 'http://collar6.tumblr.com/'
    firstStripUrl = url + 'post/138117470810/the-very-first-strip-from-when-i-thought-it-was'
    imageSearch = '//figure[@class="photo-hires-item"]//img'
    prevSearch = '//a[@class="previous-button"]'
    latestSearch = '//li[@class="timestamp"]/a'
    adult = True


class CollegeCatastrophe(_ParserScraper):
    url = 'https://www.tigerknight.com/cc'
    stripUrl = url + '/%s'
    firstStripUrl = stripUrl % '2000-11-10'
    imageSearch = '//img[@class="comic-image"]'
    prevSearch = '//a[@class="prev"]'
    endOfLife = True
    multipleImagesPerStrip = True


class Comedity(_BasicScraper):
    url = 'http://www.comedity.com/'
    stripUrl = url + 'index.php?strip_id=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = compile(r'<img src="(Comedity_files/.+?)"')
    prevSearch = compile(r'<a href="(/?index.php\?strip_id=\d+?)"> *<img alt=\"Prior Strip')
    help = 'Index format: n (no padding)'


class ComingUpViolet(_WordPressScraper):
    url = 'https://jadephoenix.org/comingupviolet/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'coming-up-violet'
    ignoreRobotsTxt = True


class CommanderKitty(_WPNavi):
    url = 'http://www.commanderkitty.com/'
    stripUrl = url + '%s/'
    firstStripUrl = stripUrl % '2009/01/03/good-to-be-back'
    endOfLife = True


class CommitStrip(_ParserScraper):
    baseUrl = 'https://www.commitstrip.com/en/'
    url = baseUrl + '?setLocale=1'  # ensure the language cookie is set
    stripUrl = baseUrl + '%s/'
    firstStripUrl = 'http://www.commitstrip.com/en/2012/02/22/interview/'  # non-TLS!

    latestSearch = '//section//a'
    starter = indirectStarter
    imageSearch = '//article/div//img'
    prevSearch = '//span[@class="nav-previous"]/a'
    help = 'Index format: yyyy/mm/dd/strip-name'

    def namer(self, image_url, page_url):
        parts = page_url.rstrip('/').rsplit('/')[-4:]
        return '-'.join(parts)


class CommitStripFr(CommitStrip):
    baseUrl = 'https://www.commitstrip.com/fr/'
    url = baseUrl + '?setLocale=1'  # ensure the language cookie is set
    stripUrl = baseUrl + '%s/'
    firstStripUrl = 'http://www.commitstrip.com/fr/2012/02/22/interview/'  # non-TLS!
    lang = 'fr'


class CompanyY(_BasicScraper):
    url = 'http://company-y.com/'
    rurl = escape(url)
    stripUrl = url + '%s/'
    firstStripUrl = stripUrl % '2009/08/14/coming-soon'
    imageSearch = compile(tagre("img", "src", r'(%scomics/[^"]+)' % rurl))
    prevSearch = compile(tagre("div", "class", r"nav-previous") +
                         tagre("a", "href", r'(%s[^"]+)' % rurl))
    help = 'Index format: yyyy/mm/dd/strip-name'


class Concession(_ParserScraper):
    url = 'http://concessioncomic.com/'
    stripUrl = url + 'index.php?pid=%s'
    firstStripUrl = stripUrl % '20060701'
    imageSearch = '//div[@id="comic"]/img[not(@class="preload")]'
    prevSearch = '//a[@class="nav-prev"]'
    adult = True
    endOfLife = True


class CorydonCafe(_ParserScraper):
    url = 'http://corydoncafe.com/'
    imageSearch = "//center[2]//img"
    prevSearch = '//a[@title="prev"]'
    multipleImagesPerStrip = True


class CourtingDisaster(_WordPressScraper):
    url = 'http://www.courting-disaster.com/'
    firstStripUrl = 'http://www.courting-disaster.com/comic/courting-disaster-17/'


class CraftedFables(_WordPressScraper):
    url = 'http://www.caf-fiends.net/comicpress/'
    prevSearch = '//a[@rel="prev"]'


class CrapIDrewOnMyLunchBreak(_BasicScraper):
    url = 'http://crap.jinwicked.com/'
    stripUrl = url + '%s/'
    firstStripUrl = stripUrl % '2003/07/30/jin-and-josh-decide-to-move'
    imageSearch = compile(tagre("img", "src", r'(http://crap\.jinwicked\.com/comics/[^"]+)'))
    prevSearch = compile(tagre("a", "href", r'([^"]+)', after="prev"))
    help = 'Index format: yyyy/mm/dd/name'


class CrimsonDark(_BasicScraper):
    url = 'http://www.davidcsimon.com/crimsondark/'
    stripUrl = url + 'index.php?view=comic&strip_id=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = compile(r'src="(.+?strips/.+?)"')
    prevSearch = compile(r'<a href=[\'"](/crimsondark/index\.php\?view=comic&amp;strip_id=\d+)[\'"]><img src=[\'"]themes/cdtheme/images/active_prev.png[\'"]')
    help = 'Index format: n (unpadded)'


class CrimsonFlag(_ParserScraper):
    url = 'http://crimsonflagcomic.com/'
    stripUrl = url + 'comic.php?comicID=%s'
    firstStripUrl = stripUrl % '1'
    imageSearch = '//img[@class="comicimage"]'
    prevSearch = '//a[contains(@class, "prev")]'


class CritterCoven(_WordPressScraper):
    url = 'http://crittercoven.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'critter-coven'


class CrossTimeCafe(_ParserScraper):
    stripUrl = 'http://www.whiteponyproductions.com/ctc/%s.htm'
    url = stripUrl % 'present'
    firstStripUrl = stripUrl % 'ctc0001'
    imageSearch = '//img[not(contains(@src, "graphics/"))]'
    prevSearch = '//a[.//text()="Back"]'
    multipleImagesPerStrip = True
    endOfLife = True


class CtrlAltDel(_ParserScraper):
    url = 'https://cad-comic.com/'
    stripUrl = url + 'comic/%s'
    firstStripUrl = stripUrl % 'nice-melon'
    imageSearch = '//div[@class="comicpage"]/a/img'
    prevSearch = '//a[@rel="prev"]'
    ignoreRobotsTxt = True

    def getPrevUrl(self, url, data):
        # Reimplement JS-only navigation logic
        postId = data.xpath('//article/@class')[0].split(' ', 1)[0].replace('post-', '')
        query = '?action=get_nav_post&nav_type=previous&post_id=' + postId
        prev = self.getPage(self.url + 'wp-admin/admin-ajax.php' + query).text_content()
        return json.loads(prev)['url']

    def namer(self, imageUrl, pageUrl):
        # Fix inconsistent filenames
        return imageUrl.rsplit('/', 1)[-1].replace('ENG_', 'cad-')


class CucumberQuest(_BasicScraper):
    url = 'http://cucumber.gigidigi.com/'
    rurl = escape(url)
    stripUrl = url + 'cq/%s/'
    firstStripUrl = stripUrl % 'page-1'
    startUrl = url + 'recent.html'
    starter = indirectStarter
    imageSearch = (
        compile(tagre("img", "src", r'(%swp-content/uploads/\d+/\d+/\d+[^"]+)' % rurl)),
        compile(tagre("img", "src", r'(%swp-content/uploads/\d+/\d+/ch\d+[^"]+)' % rurl)),
        compile(tagre("img", "src", r'(%swp-content/uploads/\d+/\d+/bonus[^"]+)' % rurl)),
    )
    prevSearch = compile(tagre("a", "href", r'(%scq/[^"]+/)' % rurl, after="previous"))
    latestSearch = compile(r'window\.location="(/cq/[^"]+/)"')
    help = 'Index format: stripname'


class Curtailed(_WordPressScraper):
    url = 'https://www.curtailedcomic.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % '001-sneeze'

    def shouldSkipUrl(self, url, data):
        """Skip pages without images."""
        return 'comic/sitrep-1' in url or 'comic/be-right-back' in url


class Curvy(_ParserScraper):
    url = 'http://www.c.urvy.org/'
    stripUrl = url + '?date=%s'
    firstStripUrl = stripUrl % '20080329'
    imageSearch = '//div[@id="theActualComic"]//img'
    prevSearch = '//div[@class="aNavbar"]//p[2]/a'
    help = 'Index format: yyyymmdd'


class CutLoose(_ParserScraper):
    url = 'https://www.cutloosecomic.com/'
    stripUrl = url + 'archive/comic/%s'
    firstStripUrl = stripUrl % '2016/02/02'
    imageSearch = '//img[@id="comic-container"]'
    prevSearch = '//a[@title="Previous Comic"]'
    nextSearch = '//a[@title="Next Comic"]'
    starter = bounceStarter
    adult = True

    def namer(self, imageUrl, pageUrl):
        postDate = pageUrl.rsplit('/', 3)
        filename = imageUrl.rsplit('/', 1)[-1]
        return '%s-%s-%s_%s' % (postDate[1], postDate[2], postDate[3], filename)


class CyanideAndHappiness(_BasicScraper):
    url = 'http://www.explosm.net/'
    stripUrl = url + '%s/'
    firstStripUrl = stripUrl % '15'
    imageSearch = compile(tagre("img", "src", r'(//files.explosm.net/comics/[^"]+)', before="main-comic"))
    prevSearch = compile(tagre("a", "href", r'(/comics/\d+/)', after="nav-previous"))
    nextSearch = compile(tagre("a", "href", r"(/comics/\d+/)", after="nav-next"))
    help = 'Index format: n (unpadded)'

    def shouldSkipUrl(self, url, data):
        """Skip pages without images."""
        return "/comics/play-button.png" in data[0]

    def namer(self, image_url, page_url):
        imgname = image_url.split('/')[-1]
        # only get the first 100 chars for the image name
        imgname = imgname[:100]
        imgnum = page_url.split('/')[-2]
        return '%s_%s' % (imgnum, imgname)


class CynWolf(_ParserScraper):
    url = 'https://cynwolf.net/'
    stripUrl = url + '%s/'
    firstStripUrl = stripUrl % '2008/because'
    imageSearch = '//section[contains(@class, "comic")]//img'
    prevSearch = '//a[text()="\u2190"]'
    multipleImagesPerStrip = True
    endOfLife = True
