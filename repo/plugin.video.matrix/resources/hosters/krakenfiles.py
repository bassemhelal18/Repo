from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker





class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'krakenfiles', '-[krakenfiles]')
			
    def _getMediaLinkForGuest(self, autoPlay = False):
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        
       # (.+?) .+? ([^<]+)

        sPattern =  'data-src-url="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        
        for aEntry in aResult[1]:
                
           api_call = 'https:'+ aEntry
          
        if api_call:
                    return True, api_call

        return False, False