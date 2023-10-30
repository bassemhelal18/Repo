#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog, VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'egybest', '[EgyBest]')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url).replace("eeggyy","")
        
    def _getMediaLinkForGuest(self, autoPlay = False):

        sReferer = ""
        url = self._url.split('|Referer=')[0]
        sReferer = self._url.split('|Referer=')[1]
        
        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
        
        sPattern = 'file: "([^"]+)".*?label: "([^"]+)",'
        aResult = oParser.parse(sHtmlContent,sPattern)
        list_url=[]
        list_q=[]
        for aEntry in aResult[1]:
                
                list_url.append(aEntry[0])
                list_q.append(aEntry[1]) 
				
        api_call = dialog().VSselectqual(list_q,list_url)
        if api_call:
                    return True, api_call+ '|User-Agent=' + UA

        return False, False