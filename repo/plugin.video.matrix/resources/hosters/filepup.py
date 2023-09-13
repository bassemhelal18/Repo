#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filepup', 'FilePup')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        oRequestHandler = cRequestHandler(self._url)
        #oRequestHandler.addParameters('login', '1')
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = 'type: "video\/mp4", *src: "([^<>"{}]+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] :
            return True, aResult[1][0]

        return False, False
