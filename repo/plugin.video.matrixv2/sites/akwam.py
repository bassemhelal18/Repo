# -*- coding: utf-8 -*-


import os,re
import xbmcaddon
from urllib.parse import unquote
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

SITE_IDENTIFIER = 'akwam'
SITE_NAME = 'Akwam'
SITE_ICON = 'akwam.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'ak.sv')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'movies?section=30'
URL_MOVIES_Arabic = URL_MAIN + 'movies?section=29'
URL_SERIES_English = URL_MAIN + 'series?section=30'
URL_SERIES_Arabic = URL_MAIN + 'series?section=29'
URL_MOVIES_Kids = URL_MAIN + 'movies?category=30'
URL_SEARCH = URL_MAIN + 'search?q=%s'

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
    oRequest = cRequestHandler(sUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # HTML Cache Zeit 6 Stunden
    sHtmlContent = oRequest.request()
    
    
    pattern = '<span class="label quality">.*?</span>.+?<a href="([^<]+)" class="box">.+?data-src="([^<]+)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">([^<]+)</span>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    for sUrl, sThumbnail, sName, sYear in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        sName = sName.split('الموسم')[0]
        
        if sName not in itemList:
            itemList.append(sName)
            
            isTvshow, aResult = cParser.parse(unquote(sUrl), 'series')
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
            params.setParam('sUrl', sUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)
            params.setParam('sYear', sYear)

            oGui.addFolder(oGuiElement, params, isTvshow, total)
        
    if not sGui and not sSearchText:
        isMatchNextPage, sNextUrl = cParser.parseSingleResult(sHtmlContent,'<a class="page-link" href="([^<]+)" rel="next".*?aria-label')
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
    oRequest=cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    
    
    pattern = 'meta property=".+?title".+?content="([^<]+)".+?/>.+?<meta property=".+?image".+?content="([^<]+)".+?/>.+?<link rel=".+?" href="(.+?)">'  # start element
    
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    
    if  isMatch:
     total = len(aResult)
     for sSeason,sThumbnail,sUrl in aResult:
        sSeason = sSeason.replace(str(sName),'')
        sSeason = sSeason.replace(" | اكوام","").replace("الموسم العاشر","10").replace("الموسم الحادي عشر","11").replace("الموسم الثاني عشر","12").replace("الموسم الثالث عشر","13").replace("الموسم الرابع عشر","14").replace("الموسم الخامس عشر","15").replace("الموسم السادس عشر","16").replace("الموسم السابع عشر","17").replace("الموسم الثامن عشر","18").replace("الموسم التاسع عشر","19").replace("الموسم العشرون","20").replace("الموسم الحادي و العشرون","21").replace("الموسم الثاني و العشرون","22").replace("الموسم الثالث و العشرون","23").replace("الموسم الرابع والعشرون","24").replace("الموسم الخامس و العشرون","25").replace("الموسم السادس والعشرون","26").replace("الموسم السابع و العشرون","27").replace("الموسم الثامن والعشرون","28").replace("الموسم التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الموسم الحادي و الثلاثون","31").replace("الموسم الثاني والثلاثون","32").replace("الموسم الثالث و الثلاثون","33").replace("الموسم الأول","1").replace("الموسم الاول","1").replace("الموسم الثاني","2").replace("الموسم الثالث","3").replace("الموسم الثالث","3").replace("الموسم الرابع","4").replace("الموسم الخامس","5").replace("الموسم السادس","6").replace("الموسم السابع","7").replace("الموسم الثامن","8").replace("الموسم التاسع","9")
        isSeason,sSeason = cParser.parse(sSeason, '\d+')
        if not isSeason:
         sSeason='1'
        sSeason=str(sSeason).replace("['","").replace("']","")
        sSeason=str(sSeason).replace("['","").replace("']","")
        oGuiElement = cGuiElement('Season'+' ' +sSeason.strip(), SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setMediaType('season')
        params.setParam('sUrl', sUrl.strip())
        params.setParam('sThumbnail', sThumbnail)
        cGui().addFolder(oGuiElement, params, True, total)
    
    
    pattern = '<a href="([^<]+)" class="text-white- ml-2 btn btn-light mb-2">(.+?)</a>'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if  isMatch:
     total = len(aResult)
     for sUrl,sSeason in aResult:
        sSeason = sSeason.replace(sName,'')
        sSeason = sSeason.replace(" | اكوام","").replace("الموسم العاشر","10").replace("الموسم الحادي عشر","11").replace("الموسم الثاني عشر","12").replace("الموسم الثالث عشر","13").replace("الموسم الرابع عشر","14").replace("الموسم الخامس عشر","15").replace("الموسم السادس عشر","16").replace("الموسم السابع عشر","17").replace("الموسم الثامن عشر","18").replace("الموسم التاسع عشر","19").replace("الموسم العشرون","20").replace("الموسم الحادي و العشرون","21").replace("الموسم الثاني و العشرون","22").replace("الموسم الثالث و العشرون","23").replace("الموسم الرابع والعشرون","24").replace("الموسم الخامس و العشرون","25").replace("الموسم السادس والعشرون","26").replace("الموسم السابع و العشرون","27").replace("الموسم الثامن والعشرون","28").replace("الموسم التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الموسم الحادي و الثلاثون","31").replace("الموسم الثاني والثلاثون","32").replace("الموسم الثالث و الثلاثون","33").replace("الموسم الأول","1").replace("الموسم الاول","1").replace("الموسم الثاني","2").replace("الموسم الثالث","3").replace("الموسم الثالث","3").replace("الموسم الرابع","4").replace("الموسم الخامس","5").replace("الموسم السادس","6").replace("الموسم السابع","7").replace("الموسم الثامن","8").replace("الموسم التاسع","9")
        
        isSeason,sSeason = cParser.parse(sSeason, '\d+')
        if not isSeason:
         sSeason='1'
        sSeason=str(sSeason).replace("['","").replace("']","")
        oGuiElement = cGuiElement('Season'+' '+sSeason.strip(), SITE_IDENTIFIER, 'showEpisodes')
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
    sThumbnail = params.getValue('sThumbnail')
    oRequest=cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    sSeason = params.getValue('season')
    sShowName = params.getValue('sName')
    
    
    sStart = 'class="header-link text-white">الحلقات</span>'
    sEnd = '<div class="widget-4 widget widget-style-1 more mb-4">'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    
    pattern = 'class="text-white">(.+?)</a>.+?<a href="([^<]+)">.+?<img src="([^<]+)" class="img-fluid" alt='  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch: return
    total = len(aResult)
    for sEpisode,sUrl, sThumbnail in aResult:
        issEpisode, sEpisode = cParser.parseSingleResult(sEpisode, 'حلقة (.*?) :')
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
    oRequest=cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    
    
    sPattern =  'href="(http[^<]+/watch/.+?)"' 
    aResult = cParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        murl =  aResult[1][0]
        oRequest = cRequestHandler(murl)
        sHtmlContent = oRequest.request()

    sPattern =  'href="(http[^<]+/watch/.+?)".*?>اضغط هنا</span>'  
    aResult = cParser.parse(sHtmlContent,sPattern)
    
    if aResult[0]:
        murl =  aResult[1][0]
        oRequest = cRequestHandler(murl)
        sHtmlContent = oRequest.request()
        

    pattern = '<source.+?src="(.+?)".+?size="(.+?)"'  # start element
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if isMatch:
        for sUrl ,sQuality in aResult:
            sName = cParser.urlparse(sUrl)
            
             # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
            if 'youtube' in sUrl:
                continue
            elif sUrl.startswith('//'):
                 sUrl = 'https:' + sUrl
            elif 'downet' in sUrl:
                sName = 'Akwam'
                sUrl = sUrl + '|AUTH=TLS&verifypeer=false' + '&Referer=' + URL_MAIN
                sQuality = sQuality + 'p'
            hoster = {'link': sUrl, 'name': sName, 'displayedName':sName+' '+sQuality, 'quality': sQuality, 'resolveable': True} # Qualität Anzeige aus Release Eintrag
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters

def getHosterUrl(sUrl=False):
    return [{'streamUrl': sUrl, 'resolved': True}]


def showSearch():
    sSearchText = cGui().showKeyBoard()
    
    if not sSearchText: return
    
    _search(False, sSearchText)
    
    cGui().setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_SEARCH % cParser.quotePlus(sSearchText), oGui, sSearchText)

