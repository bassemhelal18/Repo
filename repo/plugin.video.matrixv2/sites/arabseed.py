# -*- coding: utf-8 -*-



import os
import re
import xbmcaddon
from urllib.parse import unquote,quote
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser, cUtil
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

SITE_IDENTIFIER = 'arabseed'
SITE_NAME = 'Arabseed'
SITE_ICON = 'arabseed.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'asd.quest')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'category/foreign-movies/'
URL_MOVIES_Arabic = URL_MAIN + 'category/arabic-movies-5/'
URL_SERIES_English = URL_MAIN + 'category/foreign-series/'
URL_SERIES_Arabic = URL_MAIN + 'category/arabic-series/'
URL_MOVIES_Kids = URL_MAIN + 'category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%86%d9%8a%d9%85%d9%8a%d8%b4%d9%86/'
URL_SEARCH = URL_MAIN + 'find/?find=%s'

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
        oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    
    
    oRequest.addHeaderEntry('Referer', quote(sUrl))
    sHtmlContent = oRequest.request()
    
    pattern = 'class="MovieBlock.*?<a\s*href="(.*?)">.*?data-src="(.*?)".*?alt="(.*?)"'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    for sUrl, sThumbnail,sName in aResult:
        isTvshow, aResult = cParser.parse(sName,'الحلقة')
        if not isTvshow:
           isTvshow, aResult = cParser.parse(sName,'مسلسل')
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        sName = sName.replace('مترجمة','').replace('مترجم','').replace('فيلم','').replace('مسلسل','').split('الموسم')[0].split('الحلقة')[0]
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
        isMatchNextPage, sNextUrl = cParser.parseSingleResult(sHtmlContent,'<li><a class=\"next.page-numbers\" href=\"(.+?)\">')
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
    
    
    pattern = 'data-id="(.+?)" data-season="(.+?)"><i class="fa fa-folder"></i>الموسم <span>(.+?)</span></li>'  # start element
    
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if  isMatch:
       
     total = len(aResult)
     for dataid, dataseason,sSeason in aResult:
        sSeason = sSeason.replace("مترجم","").replace("مترجمة","").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace("الموسم الخامس","5").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10")
        oGuiElement = cGuiElement('Season'+' ' +sSeason, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setMediaType('season')
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('dataid', dataid)
        params.setParam('dataseason', dataseason)
        cGui().addFolder(oGuiElement, params, True, total)
    else:
        
        pattern = '<link rel="canonical" href="(.*?)".*?<meta property="og:title" content="(.*?)" />'  # start element
        isMatch, aResult = cParser.parse(sHtmlContent, pattern)
        if  isMatch:
          total = len(aResult)
          for sUrl,sSeason in aResult:
            
            sSeason = sSeason.replace(sName,'').replace('مسلسل','').split('الحلقة')[0].replace("مترجم","").replace("مترجمة","").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace("الموسم الخامس","5").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10").replace("الموسم","").strip()
            isSeason,sSeason = cParser.parse(sSeason, '\d+')
            sSeason=str(sSeason).replace("['","").replace("']","")
            if not isSeason:
              sSeason='1'
            oGuiElement = cGuiElement('Season'+' '+sSeason, SITE_IDENTIFIER, 'showEpisodes')
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
    dataid = params.getValue('dataid')
    dataseason = params.getValue('dataseason')
    
    if dataid:
     urlseason = URL_MAIN + 'wp-content/themes/Elshaikh2021/Ajaxat/Single/Episodes.php'
     Handler = cRequestHandler(urlseason)
     Handler.addParameters('post_id', dataid)
     Handler.addParameters('season', dataseason)
     sHtmlContent =Handler.request()
     
     pattern = 'href="([^<]+)">.*?<em>([^<]+)</em>'  # start element
     isMatch, aResult = cParser.parse(sHtmlContent, pattern)
     if  isMatch: 
      total = len(aResult)
      for sUrl, sEpisode in aResult:
        oGuiElement = cGuiElement('Episode ' + sEpisode, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setTVShowTitle(sShowName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(sEpisode)
        oGuiElement.setMediaType('episode')
        params.setParam('sUrl', sUrl)
        cGui().addFolder(oGuiElement, params, False, total)
    else:
       
       sStart = '<div class="ContainerEpisodesList"'
       sEnd = '<div style="clear: both;"></div>'
       sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
       pattern = 'href="([^<]+)">.*?<em>([^<]+)</em>'  # start element
       isMatch, aResult = cParser.parse(sHtmlContent, pattern)
       if  isMatch:
        total = len(aResult)
        for sUrl, sEpisode in aResult:
         oGuiElement = cGuiElement('Episode ' + sEpisode, SITE_IDENTIFIER, 'showHosters')
         oGuiElement.setTVShowTitle(sShowName)
         oGuiElement.setSeason(sSeason)
         oGuiElement.setEpisode(sEpisode)
         oGuiElement.setMediaType('episode')
         params.setParam('sUrl', sUrl)
         cGui().addFolder(oGuiElement, params, False, total)
    cGui().setView('episodes')
    cGui().setEndOfDirectory()


def showHosters():
    hosters = []
    sUrl = ParameterHandler().getValue('sUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    
    pattern = '<a href="([^<]+)" class="watchBTn">'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch: return
    for slink in aResult:
        oRequest = cRequestHandler(slink,caching=False)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1')
        oRequest.addHeaderEntry('referer', URL_MAIN)
        sHtmlContent4 = oRequest.request()
        
    sStart = '<h3>مشاهدة 1080</h3>'
    sEnd = '<div class="containerIframe">'
    sHtmlContent2 = cParser.abParse(sHtmlContent4, sStart, sEnd)
    
    if '<h3>مشاهدة 1080</h3>' in sHtmlContent2:
     sPattern = 'link="(.+?)"'
     isMatch,aResult = cParser.parse(sHtmlContent2, sPattern)
     
     if isMatch:
       for shost in aResult :
        
        sName = cParser.urlparse(shost)
        sQuality = '1080p'
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
        if 'youtube' in shost:
            continue
        if 'Gamezone' in sName:
            sName = 'Arabseed'
        elif shost.startswith('//'):
               shost = 'https:' + shost
        hoster = {'link': shost, 'name': sName, 'displayedName':sName+' '+sQuality, 'quality': sQuality} # Qualität Anzeige aus Release Eintrag
        hosters.append(hoster)
    
    sStart = '<h3>مشاهدة 720</h3>'
    sEnd = '<h3>مشاهدة 480</h3>'
    sHtmlContent0 = cParser.abParse(sHtmlContent4, sStart, sEnd)
    if '<h3>مشاهدة 720</h3>' in sHtmlContent0:
     sPattern = 'link="(.+?)"'
     isMatch,aResult = cParser.parse(sHtmlContent0, sPattern)
     if isMatch:
       for shost in aResult :
        sName = cParser.urlparse(shost)
        sQuality = '720p'
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
        if 'youtube' in shost:
            continue
        if 'Gamezone' in sName:
            sName = 'Arabseed'
        elif shost.startswith('//'):
               shost = 'https:' + shost
        hoster = {'link': shost, 'name': sName, 'displayedName':sName+' '+sQuality, 'quality': sQuality} # Qualität Anzeige aus Release Eintrag
        hosters.append(hoster)
    
    sStart = '<h3>مشاهدة 480</h3>'
    sEnd = '<h3>مشاهدة 1080</h3>'
    sHtmlContent1 = cParser.abParse(sHtmlContent4, sStart, sEnd)
    if '<h3>مشاهدة 480</h3>' in sHtmlContent1:
     sPattern = 'link="(.+?)"'
     isMatch,aResult = cParser.parse(sHtmlContent1, sPattern)
     if isMatch:
       for shost in aResult :
        sName = cParser.urlparse(shost)
        sQuality = '480p'
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
        if 'youtube' in shost:
            continue
        if 'Gamezone' in sName:
            sName = 'Arabseed'
        elif shost.startswith('//'):
               shost = 'https:' + shost
        hoster = {'link': shost, 'name': sName, 'displayedName':sName+' '+sQuality, 'quality': sQuality}
        hosters.append(hoster)
    else:
        sPattern = 'data-link="(.+?)" class'
        isMatch,aResult = cParser.parse(sHtmlContent4, sPattern)
        if isMatch:
          for shost in aResult :
             sName = cParser.urlparse(shost)
             if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
             if 'youtube' in shost:
               continue
             if 'Gamezone' in sName:
                sName = 'Arabseed'
             elif shost.startswith('//'):
               shost = 'https:' + shost
             hoster = {'link': shost, 'name': sName, 'displayedName':sName}
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

