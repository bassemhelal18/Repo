#-*- coding: utf-8 -*-

from six.moves import urllib_parse
import requests 
from resources.hosters.hoster import iHoster
from resources.lib import helpers
from resources.lib.comaddon import VSlog
from resources.lib.handler.requestHandler import cRequestHandler

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sendme', '[Send.Me]')

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self._url = str(sUrl)

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        s=requests.Session()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent',UA)
        oRequest.addHeaderEntry('Referer','https://send.cm/')
        oRequest.disableSSL()
        sHtmlContent = oRequest.request()
        data=helpers.get_hidden(sHtmlContent)
        
        link = s.post("https://send.cm/", data=data, allow_redirects=False)
        
        if "Location" in link.headers:
            data = str(link.headers['Location']).replace(' ','%20')
            api_call=data+"|Referer=https://send.cm/"
           
        if api_call:
            return True, api_call

        return False, False
        
