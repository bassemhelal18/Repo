# -*- coding: utf-8 -*-


import base64
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

SITE_IDENTIFIER = 'cimanow'
SITE_NAME = 'Cimanow'
SITE_ICON = 'cimanow.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'cimanow.cc')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'category/افلام-اجنبية/'
URL_MOVIES_Arabic = URL_MAIN + 'category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9/'
URL_SERIES_English = URL_MAIN + 'category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/'
URL_SERIES_Arabic = URL_MAIN + 'category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/'
URL_MOVIES_Kids = URL_MAIN + 'category/افلام-انيميشن/'
URL_SEARCH = URL_MAIN + '?s=%s'

#ToDo Serien auch auf reinen Filmseiten, prüfen ob Filterung möglich
def load(): # Menu structure of the site plugin
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_MOVIES_English)
    params.setParam('trumb', os.path.join(ART, 'MoviesEnglish.png'))
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502), SITE_IDENTIFIER, 'showEntries'), params)  
    params.setParam('sUrl', URL_MOVIES_Arabic)
    params.setParam('trumb', os.path.join(ART, 'MoviesArabic.png'))
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30500), SITE_IDENTIFIER, 'showEntries'), params)  
    params.setParam('sUrl', URL_SERIES_English)
    params.setParam('trumb', os.path.join(ART, 'TVShowsEnglish.png'))
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30514), SITE_IDENTIFIER, 'showEntries'), params)  
    params.setParam('sUrl', URL_SERIES_Arabic)
    params.setParam('trumb', os.path.join(ART, 'TVShowsArabic.png'))
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511), SITE_IDENTIFIER, 'showEntries'), params)  
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
    oRequest = cRequestHandler(sUrl)
    
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # HTML Cache Zeit 6 Stunden
    
    sHtmlContent = oRequest.request()
    
    pattern = '<article aria-label="post">.*?<a href="([^"]+).+?<li aria-label="year">(.+?)</li>.+?<li aria-label="title">([^<]+)<em>.+?data-src="(.+?)" width'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    for sUrl, sYear, sName, sThumbnail in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        if sName not in itemList:
            itemList.append(sName)
            
            isTvshow, aResult = cParser.parse(unquote(sUrl), 'مسلسل')
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
            params.setParam('sUrl', sUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)
            params.setParam('sYear', sYear)

            oGui.addFolder(oGuiElement, params, isTvshow, total)
        
    if not sGui and not sSearchText:
        isMatchNextPage,page = cParser().parse(sHtmlContent, '<li class="active"><a\s*href="(.*?)">(.*?)</a>')
        sNextUrl=''
        for sUrl, sPage in page:
             sPage = int(sPage)+1
             logger.error('active: ' + str(sPage))
             if 'page/' in sUrl:
                 sUrl = sUrl.split('page')[0]
             sNextUrl = str(sUrl)+'/page/'+str(sPage)
             
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
    if 'adilbo' in sHtmlContent:
       sHtmlContent = prase_function(sHtmlContent)
       sHtmlContent =str(sHtmlContent.encode('latin-1'),'utf-8')
    
    pattern = '<a\s*href="([^<]+)">([^<]+)<em>'  # start element
    
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        cGui().showInfo()
        return
    total = len(aResult)
    for sUrl, sSeason in aResult:
        sSeason = sSeason.replace('الموسم','')
        oGuiElement = cGuiElement('Season'+ sSeason, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setMediaType('season')
        params.setParam('sUrl', sUrl.strip())
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
    if 'adilbo' in sHtmlContent:
       sHtmlContent = prase_function(sHtmlContent)
       sHtmlContent =str(sHtmlContent.encode('latin-1'),'utf-8')
    
    sStart = 'id="eps">'
    sEnd = '<footer>'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    
    pattern = 'href="([^"]+)".*?<em>(.*?)</em>'  # start element
    
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch: return
    total = len(aResult)
    for sUrl, sEpisode in aResult:
        oGuiElement = cGuiElement('Episode ' + sEpisode, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setTVShowTitle(sShowName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(sEpisode)
        oGuiElement.setMediaType('episode')
        params.setParam('sUrl', sUrl+'watching/')
        cGui().addFolder(oGuiElement, params, False, total)
    cGui().setView('episodes')
    cGui().setEndOfDirectory()


def showHosters():
    hosters = []
    sUrl = ParameterHandler().getValue('sUrl')
    if 'watching/' not in sUrl:
        sUrl= sUrl+ 'watching/'
    sHtmlContent = cRequestHandler(sUrl).request()
    if 'adilbo' in sHtmlContent:
       sHtmlContent = prase_function(sHtmlContent)
       sHtmlContent =str(sHtmlContent.encode('latin-1'),'utf-8')
    
    pattern = 'data-index="([^"]+)".+?data-id="([^"]+)"' 
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if isMatch:
     for sIndex ,sId in aResult:
            siteUrl = URL_MAIN + '/wp-content/themes/Cima%20Now%20New/core.php?action=switch&index='+sIndex+'&id='+sId
            hdr = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0','referer' : URL_MAIN}
            params = {'action':'switch','index':sIndex,'id':sId}                
            import requests
            St=requests.Session()
            sHtmlContent2= St.get(siteUrl,headers=hdr,params=params).text
            
            sPattern =  '<iframe.+?src="([^"]+)"'
            isMatch, aResult = cParser().parse(sHtmlContent2,sPattern)
            if isMatch:
             for sUrl in aResult:
              if 'cimanowtv' in sUrl:
                  sUrl = sUrl +'$$'+URL_MAIN
              sName = cParser.urlparse(sUrl)
              sName =  sName.split('.')[-2]
              if cConfig().isBlockedHoster(sName)[0]: continue 
              if 'youtube' in sUrl:
                continue
              elif sUrl.startswith('//'):
                sUrl = 'https:' + sUrl
              hoster = {'link': sUrl, 'name': sName, 'displayedName':sName} # Qualität Anzeige aus Release Eintrag
              hosters.append(hoster)
               
    
    sStart = '<ul class="tabcontent" id="download">'
    sEnd = '</section>'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    
    pattern = '<a href="(.+?)".+?class="fas fa-cloud-download-alt"></i>\s*(.+?)\s*<p'  # start element
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if isMatch:
        for sUrl ,sQuality in aResult:
            sName = cParser.urlparse(sUrl)
            
             # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
            if 'youtube' in sUrl:
                continue
            elif sUrl.startswith('//'):
                 sUrl = 'https:' + sUrl
            elif 'cimanow' in sUrl:
                sName = 'CimaNow'
                sUrl = sUrl +'|AUTH=TLS&verifypeer=false&Referer='+URL_MAIN
                
            hoster = {'link': sUrl, 'name': sName, 'displayedName':sName+' '+sQuality, 'quality': sQuality} # Qualität Anzeige aus Release Eintrag
            hosters.append(hoster)
    sStart = '</i>سيرفرات اخري :</span>'
    sEnd = '</section>'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    pattern = '<a href="(.*?)">\s*<i class="fa fa-download"></i>'  # start element
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if isMatch:
        for sUrl in aResult:
            sName = cParser.urlparse(sUrl)
            
             # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
            if 'youtube' in sUrl:
                continue
            if cConfig().isBlockedHoster(sName)[0]: continue
            elif sUrl.startswith('//'):
                 sUrl = 'https:' + sUrl
            
            hoster = {'link': sUrl, 'name': sName, 'displayedName':sName} # Qualität Anzeige aus Release Eintrag
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    if 'verifypeer'in sUrl:
        sUrl = sUrl.replace(' ','%20')
        return [{'streamUrl': sUrl, 'resolved': True}]
    
    return [{'streamUrl': sUrl, 'resolved': False}]

def showSearch():
    sSearchText = cGui().showKeyBoard()
    
    if not sSearchText: return
    
    _search(False, sSearchText)
    
    cGui().setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_SEARCH % cParser().quotePlus(sSearchText), oGui, sSearchText)

def prase_function(page): 
    if 'adilbo' in page:
     t_script = re.findall('<script.*?;.*?\'(.*?);', page, re.S)
     t_int = re.findall('/g.....(.*?)\)', page, re.S)
     if t_script and t_int:
         script = t_script[0].replace("'",'')
         script = script.replace("+",'')
         script = script.replace("\n",'')
         sc = script.split('.')
         
         for elm in sc:
             c_elm = base64.b64decode(elm+'==').decode()
             t_ch = re.findall('\d+', c_elm, re.S)
             if t_ch:
                nb = int(t_ch[0])+int(t_int[0])
                page = page + chr(nb)
    return page