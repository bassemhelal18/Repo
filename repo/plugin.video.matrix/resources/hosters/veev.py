#-*- coding: utf-8 -*-

import binascii
import json
import re
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from six.moves import urllib_parse
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'veev', '-[veev]')

    def _getMediaLinkForGuest(self, autoPlay = False):
        self._url = self._url.replace('/d/','/e/')
        VSlog(self._url)
        id = self._url.split('/e/')[-1]
        api_call = ''
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        sHtmlContent = oRequest.request()
        
        
        f = re.search(r'{\s*fc:\s*"([^"]+)', sHtmlContent)
        if f:
            ch = veev_decode(f.group(1))
            params = {
                'op': 'player_api',
                'cmd': 'gi',
                'file_code': id,
                'ch': ch
            }
            durl = urllib_parse.urljoin(self._url, '/dl') + '?' + urllib_parse.urlencode(params)
        
            oRequest = cRequestHandler(durl)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', self._url)
            sHtmlContent = oRequest.request()
            jresp = json.loads(sHtmlContent).get('file')
            api_call = decode_url(veev_decode(jresp.get('dv')[0].get('s')), build_array(ch)[0])
        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

def veev_decode(etext):
    result = []
    lut = {}
    n = 256
    c = etext[0]
    result.append(c)
    for char in etext[1:]:
        code = ord(char)
        nc = char if code < 256 else lut.get(code, c + c[0])
        result.append(nc)
        lut[n] = c + nc[0]
        n += 1
        c = nc

    return ''.join(result)


def js_int(x):
    return int(x) if x.isdigit() else 0


def build_array(encoded_string):
    d = []
    c = list(encoded_string)
    count = js_int(c.pop(0))
    while count:
        current_array = []
        for _ in range(count):
            current_array.insert(0, js_int(c.pop(0)))
        d.append(current_array)
        count = js_int(c.pop(0))

    return d


def decode_url(etext, tarray):
    ds = etext
    for t in tarray:
        if t == 1:
            ds = ds[::-1]
        ds = binascii.unhexlify(ds).decode('utf8')
        ds = ds.replace('dXRmOA==', '')

    return ds    
        
