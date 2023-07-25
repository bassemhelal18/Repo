# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'watchvideo', 'WatchVideo')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()

        # Dean Edwards Packer
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] :
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = '{file:"([^"]+)"\,label:"([^"]+)"}'
            aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] :
            # initialisation des tableaux
            url = []
            qua = []

            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # tableau
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
