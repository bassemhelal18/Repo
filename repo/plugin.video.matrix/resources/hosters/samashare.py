#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://sama-share.com/embed-shsaa6s49l55-750x455.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'samashare', '-[Vidpro]')
			
    def setUrl(self, sUrl):
        self._url = str(sUrl)
        #lien embed obligatoire
    
    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False
        host = 'https://'+self._url.split('/')[2]
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        
        sPattern =  """onclick="download_video.*?'(.*?)','(.*?)','(.*?)'"""
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
           for aEntry in aResult[1]:
               sId = aEntry[0]
               sMode= aEntry[1]
               sHash = aEntry[2]
               slink  = host + '/dl?op=download_orig'+'&id='+sId+'&mode='+sMode+'&hash='+sHash
               
               oRequest = cRequestHandler(slink)
               sHtmlContent2 = oRequest.request()
               
               sPattern =  'href="([^<]+)">Direct'
               aResult = oParser.parse(sHtmlContent2, sPattern)
               if aResult[0]:
                    
                    api_call =aResult[1][0]
                    
        sPattern =  '(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for i in aResult[1]:
                decoded = cPacker().unpack(i)
 
                if decoded:
                    r = re.search('file:"(.+?)",', decoded, re.DOTALL)
                    if r:
                        api_call = r.group(1)
                    r2 = re.search('src="(.+?)"', decoded, re.DOTALL)
                    if r2:
                        api_call = r2.group(1)


        if api_call:
            return True, api_call + '|User-Agent=' + UA 

        return False, False