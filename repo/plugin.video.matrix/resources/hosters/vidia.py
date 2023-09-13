# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidia', 'Vidia')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] :
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = '{file:"([^"]+)"}'
            aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] :
            api_call = aResult[1][0].replace(',', '').replace('master.m3u8', 'index-v1-a1.m3u8')

        if api_call:
            return True, api_call

        return False, False
