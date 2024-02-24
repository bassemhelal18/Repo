#-*- coding: utf-8 -*-

import base64
import re
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'voe', '-[voe]')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        r = re.search(r"let\s*(?:wc0|[0-9a-f]+)\s*=\s*'([^']+)", sHtmlContent)
        if r:
            import json
            r = json.loads(base64.b64decode(r.group(1)).decode('utf8',errors='ignore'))
            url = r.get('file') 
            return True, url + '|User-Agent=' + UA + '&Referer=' + self._url + '&Origin=' + self._url.rsplit('/', 2)[0]

        oParser = cParser()
        sPattern = '["\']hls["\']:\s*["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
        
