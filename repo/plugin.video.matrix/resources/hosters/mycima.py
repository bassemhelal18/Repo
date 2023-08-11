#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import re
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mycima', 'wecima')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)



        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequestHandler.request()
        
        oParser = cParser()
        
        sPattern = """format: '(.*?)', src: "(.*?)", type: 'video/mp4'"""
        aResult = oParser.parse(sHtmlContent,sPattern)
        list_url=[]
        list_q=[]
        for aEntry in aResult[1]:
                list_q.append(aEntry[0])
                list_url.append(aEntry[1]) 
				
        api_call = dialog().VSselectqual(list_q,list_url)
        api_call = api_call.replace(' ', '%20').replace('localhost', 'wecima.dev') +'|AUTH=TLS&verifypeer=false' + '&Referer=' 

        if api_call:
                    return True, api_call

        return False, False