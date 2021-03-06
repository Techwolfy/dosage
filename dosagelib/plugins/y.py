# SPDX-License-Identifier: MIT
# Copyright (C) 2004-2008 Tristan Seligmann and Jonathan Jacobs
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring
from .common import _WordPressScraper, _WPWebcomic


class YAFGC(_WordPressScraper):
    url = 'http://yafgc.net/'


class YoshSaga(_WPWebcomic):
    url = 'https://www.yoshsaga.com/'
    stripUrl = url + 'comic/%s/'
    firstStripUrl = stripUrl % 'introduction'
