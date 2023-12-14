# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import requests
from resources.lib.comaddon import VSlog
from resources.lib.handler.requestHandler import cRequestHandler
import re
import base64
from urllib.parse import unquote
from resources.lib.parser import cParser
from bs4 import BeautifulSoup
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cMultiup:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):
        sHtmlContent = GetHtml(url)
        sPattern = '<form action="(.+?)" method="post"'
        result = re.findall(sPattern, sHtmlContent)
        if result:
         url = 'https://www.multiup.org' + ''.join(result[0])
        
        
        
        sHtmlContent = GetHtml(url)
        
        sPattern = 'link="([^"]+)".+?class="([^"]+)"'
        
        r = re.findall(sPattern, sHtmlContent, re.MULTILINE)
        
        if not r:
            return False

        for item in r:

            if 'bounce-to-right' in str(item[1]) and not 'download-fast' in item[0]:
                self.list.append(item[0])

        return self.list

class cMegamax:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        sHosterUrl = url.replace('download','iframe')
        oRequestHandler = cRequestHandler(sHosterUrl)
        sHtmlContent1 = oRequestHandler.request()
        sHtmlContent1 = sHtmlContent1.replace('&quot;','"')
        oParser = cParser()
        
        sVer = ''
        sPattern = '"version":"([^"]+)'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:
            for aEntry in (aResult[1]):
                sVer = aEntry

        s = requests.Session()            
        headers = {'Referer':sHosterUrl,
                                'Sec-Fetch-Mode':'cors',
                                'X-Inertia':'true',
                                'X-Inertia-Partial-Component':'web/files/mirror/video',
                                'X-Inertia-Partial-Data':'streams',
                                'X-Inertia-Version':sVer}

        r = s.get(sHosterUrl, headers=headers).json()
        
        for key in r['props']['streams']['data']:
            sQual = key['label'].replace(' (source)','')
            for sLink in key['mirrors']:
                sHosterUrl = sLink['link']
                sLabel = sLink['driver'].capitalize()
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'https:' + sHosterUrl
        
                    self.list.append(sHosterUrl+' ,'+sQual)
                    
                    
                    
        return self.list 

class cJheberg:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):

        if url.endswith('/'):
            url = url[:-1]

        idFile = url.rsplit('/', 1)[-1]
        NewUrl = 'https://api.jheberg.net/file/' + idFile
        sHtmlContent = GetHtml(NewUrl)

        sPattern = '"hosterId":([^"]+),"hosterName":"([^"]+)",".+?status":"([^"]+)"'
        r = re.findall(sPattern, sHtmlContent, re.DOTALL)
        if not r:
            return False

        for item in r:
            if not 'ERROR' in item[2]:
                urllink = 'https://download.jheberg.net/redirect/' + idFile + '-' + item[0]
                try:
                    url = GetHtml(urllink)
                    self.list.append(url)
                except:
                    pass

        return self.list


# modif cloudflare
def GetHtml(url, postdata=None):

    if 'download.jheberg.net/redirect' in url:
        oRequest = cRequestHandler(url)
        sHtmlContent = oRequest.request()
        url = oRequest.getRealUrl()
        return url
    else:
        sHtmlContent = ''
        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)

        if postdata != None:
            oRequest.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            oRequest.addHeaderEntry('Referer', 'https://download.jheberg.net/redirect/xxxxxx/yyyyyy/')

        elif 'download.jheberg.net' in url:
            oRequest.addHeaderEntry('Host', 'download.jheberg.net')
            oRequest.addHeaderEntry('Referer', url)

        oRequest.addParametersLine(postdata)

        sHtmlContent = oRequest.request()

        return sHtmlContent

class cVidsrcto:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        oParser = cParser()
        
        
        oRequest = cRequestHandler(url)
        sHtmlContent = oRequest.request()
        
        

        sPattern = 'data-id="(.*?)"'
        aResult = oParser.parse(sHtmlContent, sPattern) 
        if (aResult[0]):
          sources_code = aResult[1][0]
          sources = self.get_sources(sources_code)
          sPattern = "'.*?': '(.*?)'"
          aResult = oParser.parse(sources, sPattern)
          if aResult[0]:
            for aEntry in aResult[1]:
                source = aEntry
                source_url = self.get_source_url(source)
                if "vidplay" in source_url:
                   sHosterUrl =self.handle_vidplay(source_url)
                   self.list.append(sHosterUrl)
                elif "filemoon" in source_url:
                   sHosterUrl = self.handle_filemoon(source_url)
                   self.list.append(sHosterUrl)
        return self.list 
        
    
    def get_sources(self, data_id) -> dict:
        req = requests.get(f"https://vidsrc.to/ajax/embed/episode/{data_id}/sources")
        data = req.json()

        return {video.get("title"): video.get("id") for video in data.get("result")}      
    
    def get_source_url(self, source_id) -> str:
        req = requests.get(f"https://vidsrc.to/ajax/embed/source/{source_id}")
        data = req.json()

        encrypted_source_url = data.get("result", {}).get("url")
        return self.decrypt_source_url(encrypted_source_url)

    def decrypt_source_url(self, source_url) -> str:
        encoded = self.decode_base64_url_safe(source_url)
        decoded = self.decode(encoded)
        decoded_text = decoded.decode('utf-8')

        return unquote(decoded_text)       
    
    def decode_base64_url_safe(self, s) -> bytearray:
        standardized_input = s.replace('_', '/').replace('-', '+')
        binary_data = base64.b64decode(standardized_input)

        return bytearray(binary_data)
    
    def decode(self, str) -> bytearray:
        key_bytes = bytes('8z5Ag5wgagfsOuhz', 'utf-8')
        j = 0
        s = bytearray(range(256))

        for i in range(256):
            j = (j + s[i] + key_bytes[i % len(key_bytes)]) & 0xff
            s[i], s[j] = s[j], s[i]

        decoded = bytearray(len(str))
        i = 0
        k = 0

        for index in range(len(str)):
            i = (i + 1) & 0xff
            k = (k + s[i]) & 0xff
            s[i], s[k] = s[k], s[i]
            t = (s[i] + s[k]) & 0xff
            decoded[index] = str[index] ^ s[t]

        return decoded

    def handle_vidplay(self, url) -> str:
        key = self.encode_id(url.split('/e/')[1].split('?')[0])
        data = self.get_futoken(key, url)

        req = requests.get(f"https://vidplay.site/mediainfo/{data}?{url.split('?')[1]}&autostart=true", headers={"Referer": url})
        req_data = req.json()

        if type(req_data.get("result")) == dict:
            return req_data.get("result").get("sources", [{}])[0].get("file")
        return None

    def handle_filemoon(self, url) -> str:
        req = requests.get(url)
        matches = re.search(r'return p}\((.+)\)', req.text)
        processed_matches = []

        if not matches:
            raise Exception("No values found")
        
        split_matches = matches.group(1).split(",")
        corrected_split_matches = [",".join(split_matches[:-3])] + split_matches[-3:]
        
        for val in corrected_split_matches:
            val = val.strip()
            val = val.replace(".split('|'))", "")
            if val.isdigit() or (val[0] == "-" and val[1:].isdigit()):
                processed_matches.append(int(val))
            elif val[0] == "'" and val[-1] == "'":
                processed_matches.append(val[1:-1])

        processed_matches[-1] = processed_matches[-1].split("|")
        unpacked = self.unpack(*processed_matches)
        hls_url = re.search(r'file:"([^"]*)"', unpacked).group(1)
        return hls_url
    
    def encode_id(self, v_id) -> str:
        key1, key2 = requests.get('https://raw.githubusercontent.com/Claudemirovsky/worstsource-keys/keys/keys.json').json() 
        decoded_id = self.key_permutation(key1, v_id).encode('Latin_1')
        encoded_result = self.key_permutation(key2, decoded_id).encode('Latin_1')
        encoded_base64 = base64.b64encode(encoded_result)

        return encoded_base64.decode('utf-8').replace('/', '_')
    
    def get_futoken(self, key, url) -> str:
        req = requests.get("https://vidplay.site/futoken", {"Referer": url})
        fu_key = re.search(r"var\s+k\s*=\s*'([^']+)'", req.text).group(1)
        
        return f"{fu_key},{','.join([str(ord(fu_key[i % len(fu_key)]) + ord(key[i])) for i in range(len(key))])}"
    
    def int_2_base(self, x, base) -> str:
        charset = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/")

        if x < 0:
            sign = -1
        elif x == 0:
            return 0
        else:
            sign = 1

        x *= sign
        digits = []

        while x:
            digits.append(charset[int(x % base)])
            x = int(x / base)
        
        if sign < 0:
            digits.append('-')
        digits.reverse()

        return ''.join(digits)
    
    def unpack(self, p, a, c, k, e=None, d=None) -> str:
        for i in range(c-1, -1, -1):
            if k[i]: p = re.sub("\\b"+self.int_2_base(i,a)+"\\b", k[i], p)
        return p
    
    def key_permutation(self, key, data) -> str:
        state = list(range(256))
        index_1 = 0

        for i in range(256):
            index_1 = ((index_1 + state[i]) + ord(key[i % len(key)])) % 256
            state[i], state[index_1] = state[index_1], state[i]

        index_1 = index_2 = 0
        final_key = ''

        for char in range(len(data)):
            index_1 = (index_1 + 1) % 256
            index_2 = (index_2 + state[index_1]) % 256
            state[index_1], state[index_2] = state[index_2], state[index_1]

            if isinstance(data[char], str):
                final_key += chr(ord(data[char]) ^ state[(state[index_1] + state[index_2]) % 256])
            elif isinstance(data[char], int):
                final_key += chr((data[char]) ^ state[(state[index_1] + state[index_2]) % 256])

        return final_key

class cVidsrcnet:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        oParser = cParser()
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        sources = {attr.text: attr.get("data-hash") for attr in soup.find_all("div", {"class": "server"})}
        
        sPattern = "'.*?': '(.*?)'"
        aResult = oParser.parse(sources, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                source = aEntry
                req_1 = requests.get(f"https://rcp.vidsrc.me/rcp/{source}", headers={"Referer": url})
                soup = BeautifulSoup(req_1.text, "html.parser")

                encoded = soup.find("div", {"id": "hidden"}).get("data-h")
                seed = soup.find("body").get("data-i")

                decoded_url = self.decode_src(encoded, seed)
                if decoded_url.startswith("//"):
                   decoded_url = f"https:{decoded_url}"

                req_2 = requests.get(decoded_url, allow_redirects=False, headers={"Referer": f"https://rcp.vidsrc.me/rcp/{source}"})
                location = req_2.headers.get("Location")
                VSlog(location)
        
                if "vidsrc.stream" in location:
                  sHosterUrl= self.handle_vidsrc_stream(location, f"https://rcp.vidsrc.me/rcp/{source}")
                  self.list.append(sHosterUrl)
                if "2embed.cc" in location:
                  sHosterUrl = ''
                  self.list.append(sHosterUrl)
                if "multiembed.mov" in location:
                   sHosterUrl = self.handle_multiembed(location, f"https://rcp.vidsrc.me/rcp/{source}")
                   self.list.append(sHosterUrl)
        return self.list     
    
    def hunter_def(self, d, e, f) -> int:
        '''Used by self.hunter'''
        g = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/")
        h = g[0:e]
        i = g[0:f]
        d = list(d)[::-1]
        j = 0
        for c,b in enumerate(d):
            if b in h:
                j = j + h.index(b)*e**c
    
        k = ""
        while j > 0:
            k = i[j%f] + k
            j = (j - (j%f))//f
    
        return int(k) or 0
    
    def hunter(self, h, u, n, t, e, r) -> str:
        '''Decodes the common h,u,n,t,e,r packer'''
        r = ""
        i = 0
        while i < len(h):
            j = 0
            s = ""
            while h[i] is not n[e]:
                s = ''.join([s,h[i]])
                i = i + 1
    
            while j < len(n):
                s = s.replace(n[j],str(j))
                j = j + 1
    
            r = ''.join([r,''.join(map(chr, [self.hunter_def(s,e,10) - t]))])
            i = i + 1
    
        return r

    def decode_src(self, encoded, seed) -> str:
        '''decodes hash found @ vidsrc.me embed page'''
        encoded_buffer = bytes.fromhex(encoded)
        decoded = ""
        for i in range(len(encoded_buffer)):
            decoded += chr(encoded_buffer[i] ^ ord(seed[i % len(seed)]))
        return decoded
    
    def decode_base64_url_safe(self, s) -> bytearray:
        standardized_input = s.replace('_', '/').replace('-', '+')
        binary_data = base64.b64decode(standardized_input)

        return bytearray(binary_data)

    def handle_vidsrc_stream(self, url, source) -> str:
        '''Main vidsrc, get urls from here its fast'''
        req = requests.get(url, headers={"Referer": source})

        hls_url = re.search(r'file:"([^"]*)"', req.text).group(1)
        hls_url = re.sub(r'\/\/\S+?=', '', hls_url).replace('#2', '')

        try:
            hls_url = base64.b64decode(hls_url).decode('utf-8') # this randomly breaks and doesnt decode properly, will fix later, works most of the time anyway, just re-run
        except Exception: 
            return self.handle_vidsrc_stream(url, source)

        set_pass = re.search(r'var pass_path = "(.*?)";', req.text).group(1)
        if set_pass.startswith("//"):
            set_pass = f"https:{set_pass}"

        requests.get(set_pass, headers={"Referer": source})
        return hls_url
    
    def handle_2embed(self, url, source) -> str:
        '''Site provides ssl error :( cannot fetch from here''' # this site works now, ill reverse in future
        pass

    def handle_multiembed(self, url, source) -> str:
        '''Fallback site used by vidsrc'''
        req = requests.get(url, headers={"Referer": source})
        matches = re.search(r'escape\(r\)\)}\((.*?)\)', req.text)
        processed_values = []

        if not matches:
            print("[Error] Failed to fetch multiembed, this is likely because of a captcha, try accessing the source below directly and solving the captcha before re-trying.")
            print(url)
            return

        for val in matches.group(1).split(','):
            val = val.strip()
            if val.isdigit() or (val[0] == '-' and val[1:].isdigit()):
                processed_values.append(int(val))
            elif val[0] == '"' and val[-1] == '"':
                processed_values.append(val[1:-1])

        unpacked = self.hunter(*processed_values)
        hls_url = re.search(r'file:"([^"]*)"', unpacked).group(1)
        return hls_url