# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# french-stream /18117-la-frontire-verte-saison-1.html
# liens FVS io
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'fembed', '-[Fembed]')

    def setUrl(self, url):
        self._url = str(url)

    def _getMediaLinkForGuest(self, autoPlay = False):
        
        oRequestHandler = cRequestHandler(self._url)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'var video_source = "([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult:
            return True, aResult[1][0] + '|User-Agent=' + UA +'&Referer=https://sendvid.com/'

        return False, False