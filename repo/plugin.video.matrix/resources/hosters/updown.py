from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'updown', '-[UPdown]')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        sReferer=''
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]            
            self._url = self._url.split('|Referer=')[0]
        if'embed' in self._url:
            self._url = self._url.replace('embed-','')
            self._url = self._url.split('-')[0]
        if 'https'  in self._url:
            d = re.findall('https://(.*?)/([^<]+)',self._url)

        else:
            d = re.findall('http://(.*?)/([^<]+)',self._url)

        for aEntry in d:
            sHost= aEntry[0]
            sID= aEntry[1]
            if '/' in sID:
               sID = sID.split('/')[0]
        
        sLink= 'https://'+sHost+'/embed-'+sID+'.html'
        api_call = ''

        oRequest = cRequestHandler(sLink)
        oRequest.addHeaderEntry('Referer', sReferer)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        

        sPattern = '(eval\(function\(p,a,c,k,e,d.+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        import unicodedata

        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent2 = cPacker().unpack(data)
            
            sPattern = "file:'(.+?)'"
            aResult = oParser.parse(sHtmlContent2, sPattern)

            if aResult[0]:
                api_call = aResult[1][0]     
        else:
            api_call = api_call

        if api_call:
            return True, api_call

        return False, False