#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidzstore', 'VidzStore')

    #Extraction du lien et decodage si besoin
    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  'file: "([^"]+)\"'
        aResult = oParser.parse(sHtmlContent, sPattern)


        if (aResult[0]):
            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
