#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import progress, VSlog
import re
import base64

UA = 'ipad'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'faselhd', '-[faselHD]')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = ''
        self._url = self._url.replace('faselhd','master.m3u8')
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent',UA)
        sHtmlContent = oRequest.request()
        sPattern =  ',RESOLUTION=(.+?),.+?(http.+?m3u8)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))
            api_call = dialog().VSselectqual(qua, url)
 
            if api_call:
                return True, api_call + '|User-Agent=' + UA 

                    
                    
        
                
                