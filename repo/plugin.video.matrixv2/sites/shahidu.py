# -*- coding: utf-8 -*-



import os
import re
import xbmcaddon
from urllib.parse import unquote,quote
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

SITE_IDENTIFIER = 'shahidu'
SITE_NAME = 'Shahid4u'
SITE_ICON = 'shahidu.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'shiid4u.cam')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'category/افلام-اجنبي'
URL_MOVIES_Arabic = URL_MAIN + 'category/افلام-عربي'
URL_SERIES_English = URL_MAIN + 'category/مسلسلات-اجنبي'
URL_SERIES_Arabic = URL_MAIN + 'category/مسلسلات-عربي'
URL_MOVIES_Kids = URL_MAIN + 'category/افلام-انمي'
URL_SEARCH = URL_MAIN + 'search?s=%s'

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
    sUrl2=sUrl
    oRequest = cRequestHandler(sUrl , ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    sHtmlContent = oRequest.request()
    
    sStart = '<div class="container my-3">'
    sEnd = '<nav aria-label="Page navigation"'
    sHtmlContent1 = cParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = 'href="([^"]+)".+?image.*?\((.+?)\);.+?class="title">(.+?)</h4>'
    isMatch, aResult = cParser.parse(sHtmlContent1, sPattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    
    for sUrl, sThumbnail,sName in aResult:
        isTvshow, aResult = cParser.parse(unquote(sUrl), 'مسلسل')
        if not isTvshow:
            isTvshow, aResult = cParser.parse(unquote(sUrl),'حلقة')
            if not isTvshow:
               isTvshow, aResult = cParser.parse(unquote(sUrl),'serie')
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        sName = sName.replace('مترجمة','').replace('مترجم','').replace('فيلم','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').split('الموسم')[0].split('الحلقة')[0].replace('سلسل','').replace('مشاهدة','').replace('التريلر','').strip()
        
        sYear=''
        m = re.search('([0-9]{4})', sName)
        if m:
            sYear = str(m.group(0))
            sName = sName.replace(sYear,'')
        if sName not in itemList:
            itemList.append(sName)
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
            params.setParam('sUrl', sUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)
            if sYear:
             params.setParam('sYear', sYear)
            oGui.addFolder(oGuiElement, params, isTvshow, total)
        
    if not sGui and not sSearchText:
        sNextPage = __checkForNextPage(sHtmlContent, sUrl2)
        logger.error('active: ' + sNextPage)
        if sNextPage:
         params.setParam('sUrl', sNextPage)
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
    
    
    sStart = 'جميع المواسم'
    sEnd = '<hr class'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<a href="(.+?)".+?>الموسم</span>.+?>(.+?)</span>'
    isMatch, aResult = cParser.parse(sHtmlContent, sPattern)
    if  isMatch:
       
     total = len(aResult)
     for sUrl,sSeason in aResult:
        sSeason = sSeason.replace("مترجم","").replace("مترجمة","").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10")
        oGuiElement = cGuiElement('Season'+' ' +sSeason, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setMediaType('season')
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sUrl', sUrl.strip())
        cGui().addFolder(oGuiElement, params, True, total)
    
    cGui().setView('seasons')
    cGui().setEndOfDirectory()

def showEpisodes():
    params = ParameterHandler()
    sUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    sThumbnail = params.getValue('sThumbnail')
    sSeason = params.getValue('season')
    sShowName = params.getValue('sName')
    
    pattern = 'href="([^"]+)" class="epss.+?</span>.+?>(.+?)</span>'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if  isMatch: 
      total = len(aResult)
      for sUrl, sEpisode in aResult:
        if "season/" in sUrl:
                continue 
        if 'http' not in sUrl:
           sUrl = URL_MAIN+sUrl
        oGuiElement = cGuiElement('Episode ' + sEpisode, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setTVShowTitle(sShowName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(sEpisode)
        oGuiElement.setMediaType('episode')
        params.setParam('sUrl', sUrl.replace('episode/','download/'))
        cGui().addFolder(oGuiElement, params, False, total)
    cGui().setView('episodes')
    cGui().setEndOfDirectory()


def showHosters():
    hosters = []
    sUrl = ParameterHandler().getValue('sUrl')
    if 'download/' not in sUrl:
      sUrl =sUrl.replace('film/','download/')
    sUrl2 = sUrl.replace('/download/','/watch/')
    sHtmlContent = cRequestHandler(sUrl2).request()
    sPattern = '"url":"([^"]+)",'
    isMatch,aResult = cParser.parse(sHtmlContent, sPattern)
     
    if isMatch:
       for shost in aResult :
        sName = cParser.urlparse(shost)
        sName =  sName.split('.')[-2]
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
        if 'youtube' in shost:
            continue
        if 'filegram' in sUrl:
            sUrl = sUrl + "$$" + URL_MAIN
        elif shost.startswith('//'):
               shost = 'https:' + shost
        hoster = {'link': shost, 'name': sName, 'displayedName':sName} # Qualität Anzeige aus Release Eintrag
        hosters.append(hoster)
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sStart = 'class="down-container">'
    sEnd = '<button style='
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = '<div\s*class="qual">.+?</i>(.+?)</h1>(.*?)<hr'
    isMatch,aResult = cParser.parse(sHtmlContent0, sPattern)
    if isMatch:
       for sQuality,shost in aResult :
        sQuality=sQuality.replace("سيرفرات تحميل","").strip()
        sHtmlContent1 = shost
        sPattern = 'href="([^"]+)'
        isMatch,aResult = cParser.parse(sHtmlContent1, sPattern)
        if isMatch:
         for sUrl in aResult:
          
          sName = cParser.urlparse(sUrl)
          if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
          if 'youtube' in shost:
            continue
          if 'filegram' in sUrl:
            sUrl = sUrl + "$$" + URL_MAIN
          elif shost.startswith('//'):
               shost = 'https:' + sUrl
          hoster = {'link': sUrl, 'name': sName, 'displayedName':sName+' '+sQuality, 'quality': sQuality} # Qualität Anzeige aus Release Eintrag
          hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    Request = cRequestHandler(sUrl, caching=False)
    Request.addHeaderEntry('Referer',URL_MAIN)
    Request.request()
    sUrl = Request.getRealUrl()  # hole reale sURL
    return [{'streamUrl': sUrl, 'resolved': False}]


def showSearch():
    sSearchText = cGui().showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    cGui().setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_SEARCH % cParser.quotePlus(sSearchText), oGui, sSearchText)

def __checkForNextPage(sHtmlContent, sUrl):
    
    oParser = cParser()
    sStart = '<ul class="pagination">'
    sEnd = '<div class="footer">'
    sHtmlContent0 = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = '<li class="page-item">.*?<button class="page-link cursor-pointer" type="button" aria-label="Page Button".*?onclick="(.*?)">(.*?)</button>' 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent0, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            if 'fa-solid fa-backward' not in aEntry[1]:
                 continue
            if '?page=' in sUrl:
                sUrl = sUrl.split('?page=')[0]
                aResult = sUrl+'?page='+aEntry[0].replace(')','').replace("updateQuery('page', ","")
            else:
                aResult = sUrl+'?page='+aEntry[0].replace(')','').replace("updateQuery('page', ","")
            
            return aResult

    