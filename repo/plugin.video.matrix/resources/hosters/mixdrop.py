#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
# from resources.lib.comaddon import dialog
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mixdrop', '-[Mixdrop]')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace("/f/","/e/").replace("mixdrop.co","mixdrop.to")

    def _getMediaLinkForGuest(self, autoPlay = False):
        
        api_call = ''

        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Cookie', 'hds2=1')
        sHtmlContent = oRequest.request()

        sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent,sPattern)

        if aResult[0] :
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = 'wurl="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                api_call = aResult[1][0]

            #else:
                #sPattern = 'vsrc\d+="([^"]+)"'
                #aResult = oParser.parse(sHtmlContent, sPattern)
                #if aResult[0] :
                #    api_call = aResult[1][0]

                #else:
                #    sPattern = 'furl="([^"]+)"'
                #    aResult = oParser.parse(sHtmlContent, sPattern)
                #    if aResult[0] :
                #        api_call = aResult[1][0]

            if api_call.startswith('//'):
                api_call = 'https:' + aResult[1][0]

            if api_call:
                return True, api_call

        return False, False
