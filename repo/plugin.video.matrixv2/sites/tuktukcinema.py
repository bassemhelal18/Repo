# -*- coding: utf-8 -*-



import os
import re
from resources.lib.multihost import cMegamax
import xbmcaddon
from urllib.parse import unquote,quote
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

SITE_IDENTIFIER = 'tuktukcinema'
SITE_NAME = 'Tuktukcinema'
SITE_ICON = 'tuktukcinema.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'eg1.tuktuksu.cfd')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'category/movies-1/افلام-اجنبي/'
URL_SERIES_English = URL_MAIN + 'category/series-9/مسلسلات-اجنبي/'
URL_MOVIES_Kids = URL_MAIN + 'category/anime-6/افلام-انمي/'
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
    
    oRequest = cRequestHandler(sUrl , ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    sHtmlContent = oRequest.request()
    
    
    sPattern = '<div class="Block--Item">.*?<a.*?href="(.*?)" title="(.*?)">.*?src="(.*?)" alt'
    isMatch, aResult = cParser.parse(sHtmlContent, sPattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    
    for sUrl,sName,sThumbnail in aResult:
        isTvshow, aResult = cParser.parse(unquote(sUrl), 'مسلسل')
        if not isTvshow:
            isTvshow, aResult = cParser.parse(unquote(sUrl),'حلقة')
            if not isTvshow:
               isTvshow, aResult = cParser.parse(unquote(sUrl),'serie')
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        sName = sName.replace('مترجمة','').replace('مترجم','').replace('فيلم','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').split('الموسم')[0].split('الحلقة')[0].replace('سلسل','').replace('مشاهدة','').replace('التريلر','').strip()
        if 'data-src' in sThumbnail:
           sThumbnail= sThumbnail+'"'
           isthumb,sThumbnail= cParser.parseSingleResult(sThumbnail,'data-src="(.*?)"')
           sThumbnail = str(sThumbnail)
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
        isMatchNextPage, sNextUrl = cParser.parseSingleResult(sHtmlContent,'<a class="next page-numbers" href="(.+?)">')
        if isMatchNextPage:
            params.setParam('sUrl', URL_MAIN[:-1]+sNextUrl)
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
    sEnd = '<section class="allepcont getMoreByScroll">'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    logger.error('active: ' + sHtmlContent)
    sPattern = 'href="(.+?)".+?<img src=".+?" alt="([^<]+)" data-srccs="([^<]+)"'
    isMatch, aResult = cParser.parse(sHtmlContent, sPattern)
    if  isMatch:
       
     total = len(aResult)
     for sUrl,sSeason,sThumbnail in aResult:
        sSeason = sSeason.replace("مترجم","").replace("الموسم","").replace("مترجمة","").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10")
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
    sStart = '<section class="allepcont getMoreByScroll">'
    sEnd = '<section class="otherser"'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    
    pattern = '<a href="(.+?)"\s*title.*?class="epnum">.*?<span>الحلقة</span>\s*(.*?)\s*</div>'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if  isMatch: 
      total = len(aResult)
      for sUrl, sEpisode in aResult:
        
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
    
    sHtmlContent = cRequestHandler(sUrl).request()
    
    pattern = '<a class="watchAndDownlaod" href="(.+?)">'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch: return
    for slink in aResult:
        from requests import get
        
        headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                  'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8,en-GB;q=0.7',
                  'Referer':slink.split('watch/')[0]}
        sHtmlContent4 = get(slink,headers=headers).text
        
    sPattern = 'data-link="(.+?)" class='
    isMatch,aResult = cParser.parse(sHtmlContent4, sPattern)
    if isMatch:
       for shost in aResult :
        if 'megamax' in shost or 'tuktukcimamulti' in shost:
            sHtmlContent2 = cMegamax().GetUrls(shost)
            for item in sHtmlContent2:
                    shost = item.split(',')[0].split('=')[1]
                    sQuality = item.split(',')[1].split('=')[1]
                    
                    sName = cParser.urlparse(shost)
                    if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
                    if 'youtube' in shost:
                       continue
                    elif shost.startswith('//'):
                       shost = 'https:' + shost
                    hoster = {'link': shost, 'name': sName, 'displayedName':sName+' '+ sQuality, 'quality': sQuality} # Qualität Anzeige aus Release Eintrag
                    hosters.append(hoster)

        else:
         sName = cParser.urlparse(shost)
         sName =  sName.split('.')[-2]
         if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
         if 'youtube' in shost:
            continue
         if 'goveed' in shost:
            shost = shost+'$$'+URL_MAIN
         elif shost.startswith('//'):
               shost = 'https:' + shost
         hoster = {'link': shost, 'name': sName, 'displayedName':sName} # Qualität Anzeige aus Release Eintrag
         hosters.append(hoster)
    
    
    sPattern = sPattern = '<a target="_NEW" href="(.+?)" class="download--item">'
    isMatch,aResult = cParser.parse(sHtmlContent4, sPattern)
    if isMatch:
       for shost in aResult :
        
        sName = cParser.urlparse(shost)
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
        if 'youtube' in shost:
            continue
        elif shost.startswith('//'):
               shost = 'https:' + shost
        hoster = {'link': shost, 'name': sName, 'displayedName':sName} # Qualität Anzeige aus Release Eintrag
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


    