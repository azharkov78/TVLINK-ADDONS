# -*- coding: utf-8 -*-

import os, sys

root_dir = os.path.dirname(sys.argv[0])
libs_dir = os.path.join(root_dir, 'libs')
ssv_file = os.path.join(libs_dir, 'soupsieve.whl')
bs4_file = os.path.join(libs_dir, 'beautifulsoup.whl')

sys.path.append(root_dir)
sys.path.append(libs_dir)
sys.path.insert(0, ssv_file)
sys.path.insert(0, bs4_file)

import utils
from utils import DEF_BROWSER
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.source = 'HDgo'
        self.site = 'http://hd9.hdgo.site'
        self.link = f'ext:{self.source}:'
        self.headers = {'User-Agent': DEF_BROWSER,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Referer': self.site}

    def getHeaders(self):
        return self.headers

    def Channels(self):
        LL = []
        for cnt in range(1, 39):
            if cnt == 1: sUrl = f"{self.site}"
            else: sUrl = f"{self.site}/page/{cnt}/"
            http = utils.getURL(sUrl, headers=self.headers)
            soup = BeautifulSoup(http, "html.parser")

            for tag in soup.find_all('div', {'class': 'short-img img-box'}):
                try:
                    img = tag.find('img').get('src')
                    title = tag.find('img').get('alt')
                    ids = utils.title_to_crc32(title)
                    url = tag.find('div').get('data-href')
                    data_ch = utils.getURL(url, headers=self.headers)
                    ch_urls = utils.mfind(data_ch, '?file=', '"')
                    if not ch_urls.startswith("http"): continue
                    if ' or ' in ch_urls:
                        lst_url = ch_urls.split(' or ')
                        lst_url = list(set(lst_url))
                        for ul in lst_url:
                            if "okkotv" in ul or ".mpd" in ul: continue
                            lnk = f"{self.link}{ul}"
                            LL.append((ids, title, self.source, lnk, f"{self.site}{img}"))
                    else:
                        if "okkotv" in ch_urls or ".mpd" in ch_urls: continue
                        lnk = f"{self.link}{ch_urls}"
                        LL.append((ids, title, self.source, lnk, f"{self.site}{img}"))
                except: pass

        if LL:
            # Loading a Tuple into a Database (source, Tuple)
            utils.ch_inputs_DB(self.source, LL)

    def getLink(self, lnk):
        return lnk
