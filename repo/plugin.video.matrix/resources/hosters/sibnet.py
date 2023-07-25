#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://video.sibnet.ru/shell.php?videoid=xxxxxx

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog

#from resources.lib.comaddon import #,VSlog


UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sibnet', 'Sibnet')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False
        urlmain = 'https://video.sibnet.ru'
        oRequestHandler = cRequestHandler(self._url)
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = 'src:.+?"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] :
            api_call= urlmain + aResult[1][0] + '|Referer=' + self._url


        if api_call:
            return True, api_call

        return False, False
