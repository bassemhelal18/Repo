#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamtape', '-[Streamtape]')

    def _getMediaLinkForGuest(self, autoPlay = False):
        

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        src = re.findall(r'''ById\('.+?=\s*(["']//[^;<]+)''', sHtmlContent)
        if src:
            api_call = ''
            parts = src[-1].replace("'", '"').split('+')
            for part in parts:
                p1 = re.findall(r'"([^"]*)', part)[0]
                p2 = 0
                if 'substring' in part:
                    subs = re.findall(r'substring\((\d+)', part)
                    for sub in subs:
                        p2 += int(sub)
                api_call += p1[p2:]
            api_call += '&stream=1'
            api_call = 'https:' + api_call if api_call.startswith('//') else api_call
        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False