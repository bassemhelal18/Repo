# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
from resources.lib.packer import cPacker
import requests
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'tuktuk', '-[TukTuk]')

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = ''

        oParser = cParser()

        headers = {'User-Agent': UA,
                   'Referer': self._url
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text
        
        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])
            
        list_url = []
        list_q = []
        sPattern = '[[*?](.*?)[]*?](https.*?.mp4)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            for aEntry in aResult[1]:
                list_url.append(aEntry[1])
                list_q.append(aEntry[0])
            if list_url:
                api_call = dialog().VSselectqual(list_q, list_url)

        if api_call:
            return True, api_call+ '|User-Agent=' + UA + '&Referer=' + self._url 

        return False, False
