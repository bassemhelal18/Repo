#-*- coding: utf-8 -*-


import requests 
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog



class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sendme', '[Send.Me]')

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self._url = str(sUrl)

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        s = requests.Session()
        file_id = self._url.split("/")[-1]
       
        data = {"op": "download2", "id": file_id}
                
        link = s.post("https://send.cm/", data=data, allow_redirects=False)
        
        if "Location" in link.headers:
            api_call=link.headers["Location"]+"|Referer=https://send.cm/"
           
        
        
        

        if api_call:
            return True, api_call

        return False, False
        
