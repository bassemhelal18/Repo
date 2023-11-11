#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import resolveurl

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'resolver','-[resolver]')
        self.__sRealHost = ''

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR lightgray]'+ self._defaultDisplayName + self.__sRealHost + '[/COLOR]'

    def setRealHost(self, sName):
        self.__sRealHost = sName

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        hmf = resolveurl.HostedMediaFile(url = self._url)
        if hmf.valid_url():
            stream_url = hmf.resolve()
            if stream_url:
                return True, stream_url

        return False, False




