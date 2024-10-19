# -*- coding: utf-8 -*-



import os
import re
import xbmcaddon
from urllib.parse import unquote
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from six.moves import urllib_parse, urllib_error
SITE_IDENTIFIER = 'topcinema'
SITE_NAME = 'Topcinema'
SITE_ICON = 'topcinema.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'web2.topcinema.cam')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'category/افلام-اجنبي/'
URL_SERIES_English = URL_MAIN + 'category/مسلسلات-اجنبي/'
URL_MOVIES_Kids = URL_MAIN + 'category/افلام-انمي/'
URL_SEARCH = URL_MAIN + '?s=%s'

#ToDo Serien auch auf reinen Filmseiten, prüfen ob Filterung möglich
def load(): # Menu structure of the site plugin
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_MOVIES_English)
    params.setParam('trumb', os.path.join(ART, 'MoviesEnglish.png'))
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502), SITE_IDENTIFIER, 'showEntries'), params)  
    params.setParam('sUrl', URL_SERIES_English)
    params.setParam('trumb', os.path.join(ART, 'TVShowsEnglish.png'))
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30514), SITE_IDENTIFIER, 'showEntries'), params) 
    params.setParam('sUrl', URL_MOVIES_Kids)
    params.setParam('trumb', os.path.join(ART, 'Kids.png'))
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30503), SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('trumb', os.path.join(ART, 'search.png'))
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30520), SITE_IDENTIFIER, 'showSearch'),params)  
    cGui().setEndOfDirectory()


def showEntries(sUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    isTvshow = False
    if not sUrl: sUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(sUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # HTML Cache Zeit 6 Stunden
    sHtmlContent = oRequest.request()
    
    
    
    pattern = '<div class="Small--Box">.*?<a href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    for sUrl,sName,sThumbnail  in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        sName = sName.replace('مترجمة','').replace('مترجم','').replace('فيلم','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').split('الموسم')[0].split('الحلقة')[0].replace('سلسل','')
        sYear=''
        m = re.search('([0-9]{4})', sName)
        if m:
            sYear = str(m.group(0))
            sName = sName.replace(sYear,'')
        if sName not in itemList:
            itemList.append(sName)
            
            isTvshow, aResult = cParser.parse(unquote(sUrl), 'مسلسل')
            if not isTvshow:
              isTvshow, aResult = cParser.parse(unquote(sUrl),'حلقة')
              if not isTvshow:
               isTvshow, aResult = cParser.parse(unquote(sUrl),'serie')
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
            params.setParam('sUrl', sUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)
            params.setParam('sYear', sYear)

            oGui.addFolder(oGuiElement, params, isTvshow, total)
        
    if not sGui and not sSearchText:
        isMatchNextPage, sNextUrl = cParser.parseSingleResult(sHtmlContent,'''<li class="active"><a href=.+?<a href="(.+?)"''')
        if isMatchNextPage:
            params.setParam('sUrl', sNextUrl)
            params.setParam('trumb', os.path.join(ART, 'Next.png'))
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        
        oGui.setView('tvshows' if isTvshow else 'movies')
        oGui.setEndOfDirectory()



def showSeasons():
    params = ParameterHandler()
    sUrl = params.getValue('sUrl')
    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    
    
    sStart = '<section class="allseasonss"'
    sEnd = '<div class="row">'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = 'href="([^"]+)" title.+?<span>الموسم</span>(.+?)</div>.*?data-src="(.*?)"'
    isMatch, aResult = cParser.parse(sHtmlContent, sPattern)
    
    if  isMatch:
     total = len(aResult)
    
     for sUrl,sSeason,sThumbnail in aResult:
        sSeason = sSeason.replace('الموسم','').replace('موسم','')
        oGuiElement = cGuiElement('Season'+' ' +sSeason, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setMediaType('season')
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sUrl', sUrl)
        cGui().addFolder(oGuiElement, params, True, total)
    
    cGui().setView('seasons')
    cGui().setEndOfDirectory()

def showEpisodes():
    params = ParameterHandler()
    sUrl = params.getValue('sUrl')
    sThumbnail = params.getValue('sThumbnail')
    sHtmlContent = cRequestHandler(sUrl).request()
    sSeason = params.getValue('season')
    sShowName = params.getValue('sName')
    
    sStart = '<div class="row">'
    sEnd = '</section>'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = 'href="([^"]+)".+?class="epnum">.+?<span>الحلقة</span>(.+?)</div>'
    isMatch, aResult = cParser.parse(sHtmlContent,sPattern)
    if not isMatch: return
    total = len(aResult)
    for sUrl, sEpisode in aResult:
        sEpisode = sEpisode.replace('الحلقة','').replace('حلقة','').replace('الحلقه','').replace('حلقه','')
        oGuiElement = cGuiElement('Episode ' + sEpisode, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setTVShowTitle(sShowName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(sEpisode)
        oGuiElement.setMediaType('episode')
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sUrl', sUrl)
        cGui().addFolder(oGuiElement, params, False, total)
    cGui().setView('episodes')
    cGui().setEndOfDirectory()


def showHosters():
    hosters = []
    sUrl = ParameterHandler().getValue('sUrl')
    sUrl3 = sUrl+'watch/'
    sHtmlContent = cRequestHandler(sUrl3).request()
    sUrl2 = sUrl3.replace('/watch','/download')
    
    pattern = 'data-id="(.+?)" data-server="([^"]+)' 
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if isMatch:
     for dataid ,dataserver in aResult:
            
        urlframe= '{}wp-content/themes/movies2023/Ajaxat/Single/Server.php'.format(URL_MAIN)
        Handler = cRequestHandler(urlframe)
        Handler.addHeaderEntry('Origin',URL_MAIN[:-1])
        Handler.addHeaderEntry('Referer',urllib_parse.quote(sUrl3, '/:=&?'))
        Handler.addHeaderEntry('Sec-Fetch-Mode','cors')
        Handler.addHeaderEntry('X-Requested-With','XMLHttpRequest')
        Handler.addHeaderEntry('Sec-Fetch-Dest','empty')
        Handler.addHeaderEntry('Sec-Fetch-Site','same-origin')
        Handler.addParameters('id', dataid)
        Handler.addParameters('i', dataserver)
        sHtmlContent2 =Handler.request()
        
        sPattern =  '<iframe.+?src="([^"]+)"'
        isMatch, aResult = cParser().parse(sHtmlContent2,sPattern)
        if isMatch:
            for sUrl in aResult:
                sName = cParser.urlparse(sUrl)
                if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
                if 'youtube' in sUrl:
                  continue
                if 'trgsfjll.sbs' in sUrl:
                  sUrl = sUrl + "$$" + URL_MAIN
                if 'vidhidepro' in sUrl:
                  sUrl = sUrl + "$$" + URL_MAIN
                elif sUrl.startswith('//'):
                    sUrl = 'https:' + sUrl
                hoster = {'link': sUrl, 'name': sName, 'displayedName':sName} # Qualität Anzeige aus Release Eintrag
                hosters.append(hoster)
    
    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent = oRequestHandler.request() 

    sStart = '<div class="DownloadBox">'
    sEnd = '<script'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)    
    sPattern = 'href="([^"]+)".+?<p>(.+?)</p>'
    isMatch, aResult = cParser().parse(sHtmlContent, sPattern)
    if isMatch:
        for sUrl ,sQuality in aResult:
            sName = cParser.urlparse(sUrl)
            if cConfig().isBlockedHoster(sName)[0]: continue
             # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
            if 'youtube' in sUrl:
                continue
            if 'trgsfjll.sbs' in sUrl:
                 sUrl = sUrl + "$$" + URL_MAIN
            if 'vidhidepro' in sUrl:
                sUrl = sUrl + "$$" + URL_MAIN
            elif sUrl.startswith('//'):
                 sUrl = 'https:' + sUrl
            
            hoster = {'link': sUrl, 'name': sName, 'displayedName':sName+' '+sQuality, 'quality': sQuality} # Qualität Anzeige aus Release Eintrag
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters

def getHosterUrl(sUrl=False):
    
    return [{'streamUrl': sUrl, 'resolved': False}]
    

def showSearch():
    sSearchText = cGui().showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    cGui().setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_SEARCH % cParser.quotePlus(sSearchText), oGui, sSearchText)

