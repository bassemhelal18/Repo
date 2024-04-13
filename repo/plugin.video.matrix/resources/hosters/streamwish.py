from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import unicodedata

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamwish', '-[Streamwish]')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        self._url = self._url.replace('/f/','/e/').replace('/d/','/v/').replace('/e//','/e/')
        api_call = ''
        sReferer = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]            
            self._url = self._url.split('|Referer=')[0]
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', sReferer)
        sHtmlContent = oRequest.request()
        oParser = cParser()
       
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent = cPacker().unpack(data)

        sPattern = 'sources:\s*\[{file:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 

        sPattern = 'MDCore.wurl=["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 
            if api_call.startswith('//'):
                api_call = 'http:' + api_call

        if api_call:
            return True, api_call

        return False, False