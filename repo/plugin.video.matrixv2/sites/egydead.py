# -*- coding: utf-8 -*-




import os
import re,requests
from resources.lib.multihost import cMegamax
import xbmcaddon
from urllib.parse import unquote,quote
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

SITE_IDENTIFIER = 'egydead'
SITE_NAME = 'Egydead'
SITE_ICON = 'egydead.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'a120.egyrbyeteuh.sbs')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'category/افلام-اجنبي/'
URL_SERIES_English = URL_MAIN + 'series-category/مسلسلات-اجنبي/'
URL_MOVIES_Kids = URL_MAIN + 'category/افلام-كرتون/'
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
        oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<li class="movieItem">.+?href="([^<]+)" title="([^<]+)">.+?<img src="([^<]+)">'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    for sUrl, sName,sThumbnail  in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        
        sName = sName.replace('مترجمة','').replace('الجزء','الموسم').replace('مترجم','').replace('فيلم','').replace('مشاهدة','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').split('الموسم')[0].split('الحلقة')[0].replace('سلسل','').replace("كول سيما","").replace("جميع مواسم","").replace("كامل","").strip()
        sYear=''
        m = re.search('([0-9]{4})', sName)
        if m:
            sYear = str(m.group(0))
            sName = sName.replace(sYear,'').strip()
        if sName not in itemList:
            itemList.append(sName)
            
            isTvshow, aResult = cParser.parse(unquote(sUrl), 'مسلسل')
            if not isTvshow:
              isTvshow, aResult = cParser.parse(unquote(sUrl),'حلقة')
              if not isTvshow:
               isTvshow, aResult = cParser.parse(unquote(sUrl),'series')
               if not isTvshow:
                isTvshow, aResult = cParser.parse(unquote(sUrl),'episodes')
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
            params.setParam('sUrl', sUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)
            params.setParam('sYear', sYear)

            oGui.addFolder(oGuiElement, params, isTvshow, total)
        
    if not sGui and not sSearchText:
        isMatchNextPage, sNextUrl = cParser.parseSingleResult(sHtmlContent,'<li><a class=\"next.page-numbers\" href=\"(.+?)\">')
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

    
    sStart = '<div class="seasons-list">'
    sEnd = '<div class="singleBottomArea">'
    sHtmlContent1 = cParser.abParse(sHtmlContent, sStart, sEnd)
    if '<div class="seasons-list">' in sHtmlContent1:
     sPattern = 'class="movieItem">.*?href="(.+?)" title="([^<]+)">.*?<img src="([^<]+)"'  # start element
     isMatch, aResult = cParser.parse(sHtmlContent1, sPattern)
     if  isMatch:
       total = len(aResult)
    
       for sUrl,sSeason,sThumbnail in aResult:
        sSeason = sSeason.replace(sName,'').replace('الجزء','الموسم').replace('مترجمة','').replace('كامل','').replace('مترجم','').replace('فيلم','').replace('مشاهدة','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').replace("الموسم العاشر","10").replace("الموسم الحادي عشر","11").replace("الموسم الثاني عشر","12").replace("الموسم الثالث عشر","13").replace("الموسم الرابع عشر","14").replace("الموسم الخامس عشر","15").replace("الموسم السادس عشر","16").replace("الموسم السابع عشر","17").replace("الموسم الثامن عشر","18").replace("الموسم التاسع عشر","19").replace("الموسم العشرون","20").replace("الموسم الحادي و العشرون","21").replace("الموسم الثاني و العشرون","22").replace("الموسم الثالث و العشرون","23").replace("الموسم الرابع والعشرون","24").replace("الموسم الخامس و العشرون","25").replace("الموسم السادس والعشرون","26").replace("الموسم السابع و العشرون","27").replace("الموسم الثامن والعشرون","28").replace("الموسم التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الموسم الحادي و الثلاثون","31").replace("الموسم الثاني والثلاثون","32").replace("الموسم الثالث و الثلاثون","33").replace("الموسم الأول","1").replace("الموسم الاول","1").replace("الموسم الثاني","2").replace("الموسم الثالث","3").replace("الموسم الثالث","3").replace("الموسم الرابع","4").replace("الموسم الخامس","5").replace("الموسم السادس","6").replace("الموسم السابع","7").replace("الموسم الثامن","8").replace("الموسم التاسع","9").replace('موسم','').strip()
        sYear=''
        m = re.search('([0-9]{4})',sSeason)
        if m:
            sYear = str(m.group(0))
            sSeason = sSeason.replace(sYear,'')
        isSeason,sSeason = cParser.parse(sSeason, '\d+')
        if not isSeason:
         sSeason='1'
        
        sSeason=str(sSeason).replace("['","").replace("']","")
        oGuiElement = cGuiElement('Season'+' ' +sSeason, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setMediaType('season')
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sUrl', sUrl)
        if sYear:
         params.setParam('sYear', sYear)
        cGui().addFolder(oGuiElement, params, True, total)
    else:
        Handler = cRequestHandler(sUrl)
        Handler.addParameters('View', '1')
        sHtmlContent =Handler.request()
        
        sStart = '<div class="seasons-list">'
        sEnd = '<div class="clr">'
        sHtmlContent1 = cParser.abParse(sHtmlContent, sStart, sEnd)
        
        sPattern = 'class="movieItem">.*?href="(.+?)" title="([^<]+)">.*?<img src="([^<]+)"'  # start element
        isMatch, aResult = cParser.parse(sHtmlContent1, sPattern)
        if  isMatch:
          total = len(aResult)
    
          for sUrl,sSeason,sThumbnail in aResult:
           sSeason = sSeason.replace(sName,'').replace('الجزء','الموسم').replace('مترجمة','').replace('كامل','').replace('مترجم','').replace('فيلم','').replace('مشاهدة','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').replace("الموسم العاشر","10").replace("الموسم الحادي عشر","11").replace("الموسم الثاني عشر","12").replace("الموسم الثالث عشر","13").replace("الموسم الرابع عشر","14").replace("الموسم الخامس عشر","15").replace("الموسم السادس عشر","16").replace("الموسم السابع عشر","17").replace("الموسم الثامن عشر","18").replace("الموسم التاسع عشر","19").replace("الموسم العشرون","20").replace("الموسم الحادي و العشرون","21").replace("الموسم الثاني و العشرون","22").replace("الموسم الثالث و العشرون","23").replace("الموسم الرابع والعشرون","24").replace("الموسم الخامس و العشرون","25").replace("الموسم السادس والعشرون","26").replace("الموسم السابع و العشرون","27").replace("الموسم الثامن والعشرون","28").replace("الموسم التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الموسم الحادي و الثلاثون","31").replace("الموسم الثاني والثلاثون","32").replace("الموسم الثالث و الثلاثون","33").replace("الموسم الأول","1").replace("الموسم الاول","1").replace("الموسم الثاني","2").replace("الموسم الثانى","2").replace("الموسم الثالث","3").replace("الموسم الثالث","3").replace("الموسم الرابع","4").replace("الموسم الخامس","5").replace("الموسم السادس","6").replace("الموسم السابع","7").replace("الموسم الثامن","8").replace("الموسم التاسع","9").replace('موسم','').strip()
           sYear=''
           m = re.search('([0-9]{4})',sSeason)
           if m:
              sYear = str(m.group(0))
           sSeason = sSeason.replace(sYear,'')
           isSeason,sSeason = cParser.parse(sSeason, '\d+')
           if not isSeason:
            sSeason='1'
        
           sSeason=str(sSeason).replace("['","").replace("']","")
           oGuiElement = cGuiElement('Season'+' ' +sSeason, SITE_IDENTIFIER, 'showEpisodes')
           oGuiElement.setTVShowTitle(sName)
           oGuiElement.setSeason(sSeason)
           oGuiElement.setMediaType('season')
           params.setParam('sThumbnail', sThumbnail)
           params.setParam('sUrl', sUrl)
           if sYear:
            params.setParam('sYear', sYear)
           cGui().addFolder(oGuiElement, params, True, total)
        else:
           Handler = cRequestHandler(sUrl)
           Handler.addParameters('View', '1')
           sHtmlContent =Handler.request()
           
           sPattern ='<meta property="og:title" content="([^<]+)">.*?<meta property="og:url" content="([^<]+)"'  # start element
           isMatch, aResult = cParser.parse(sHtmlContent, sPattern)
           if  isMatch:
            total = len(aResult)
    
            for sSeason,sUrl in aResult:
             sSeason = sSeason.replace(sName,'').replace('الجزء','الموسم').split('الحلقة')[0].replace('مترجمة','').replace('كامل','').replace('مترجم','').replace('فيلم','').replace('مشاهدة','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').replace("الموسم العاشر","10").replace("الموسم الحادي عشر","11").replace("الموسم الثاني عشر","12").replace("الموسم الثالث عشر","13").replace("الموسم الرابع عشر","14").replace("الموسم الخامس عشر","15").replace("الموسم السادس عشر","16").replace("الموسم السابع عشر","17").replace("الموسم الثامن عشر","18").replace("الموسم التاسع عشر","19").replace("الموسم العشرون","20").replace("الموسم الحادي و العشرون","21").replace("الموسم الثاني و العشرون","22").replace("الموسم الثالث و العشرون","23").replace("الموسم الرابع والعشرون","24").replace("الموسم الخامس و العشرون","25").replace("الموسم السادس والعشرون","26").replace("الموسم السابع و العشرون","27").replace("الموسم الثامن والعشرون","28").replace("الموسم التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الموسم الحادي و الثلاثون","31").replace("الموسم الثاني والثلاثون","32").replace("الموسم الثالث و الثلاثون","33").replace("الموسم الأول","1").replace("الموسم الاول","1").replace("الموسم الثاني","2").replace("الموسم الثالث","3").replace("الموسم الثالث","3").replace("الموسم الرابع","4").replace("الموسم الخامس","5").replace("الموسم السادس","6").replace("الموسم السابع","7").replace("الموسم الثامن","8").replace("الموسم التاسع","9").replace('موسم','').strip()
             sYear=''
             m = re.search('([0-9]{4})',sSeason)
             if m:
               sYear = str(m.group(0))
             sSeason = sSeason.replace(sYear,'')
             isSeason,sSeason = cParser.parse(sSeason, '\d+')
             if not isSeason:
              sSeason='1'
        
             sSeason=str(sSeason).replace("['","").replace("']","")
             oGuiElement = cGuiElement('Season'+' ' +sSeason, SITE_IDENTIFIER, 'showEpisodes')
             oGuiElement.setTVShowTitle(sName)
             oGuiElement.setSeason(sSeason)
             oGuiElement.setMediaType('season')
             params.setParam('sThumbnail', sThumbnail)
             params.setParam('sUrl', sUrl)
             if sYear:
              params.setParam('sYear', sYear)
             cGui().addFolder(oGuiElement, params, True, total)
           
    cGui().setView('seasons')
    cGui().setEndOfDirectory()

def showEpisodes():
    params = ParameterHandler()
    sUrl = params.getValue('sUrl')
    
    sThumbnail = params.getValue('sThumbnail')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sSeason = params.getValue('season')
    sShowName = params.getValue('sName')
    
    sStart = '<div class="EpsList">'
    sEnd = '<div class="clr">'
    sHtmlContent1 = cParser.abParse(sHtmlContent, sStart, sEnd)
    if '<div class="EpsList">'  in sHtmlContent1:
     sPattern = '<a href="([^<]+)" title=".*?">\s*(.*?)\s*</a>'  # start element
     isMatch, aResult = cParser.parse(sHtmlContent1, sPattern)
     if isMatch:
       total = len(aResult)
       for sUrl, sEpisode in aResult:
        sEpisode = sEpisode.replace('الحلقة','').replace('حلقة','').replace('الحلقه','').replace('حلقه','').strip()
        oGuiElement = cGuiElement('Episode ' + sEpisode, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setTVShowTitle(sShowName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(sEpisode)
        oGuiElement.setMediaType('episode')
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sUrl', sUrl)
        cGui().addFolder(oGuiElement, params, False, total)
    else:
        Handler = cRequestHandler(sUrl)
        Handler.addParameters('View', '1')
        sHtmlContent =Handler.request()
        
        sPattern = '<meta property="og:title" content="(.*?)">.*?<meta property="og:url" content="(.*?)" />'
        isMatch, aResult = cParser.parse(sHtmlContent, sPattern)
        if  isMatch:
          total = len(aResult)
          for sEpisode,sUrl in aResult:
            
            sEpisode,sEpisode = cParser.parseSingleResult(sEpisode,'الحلقة \d+')
            sEpisode = str(sEpisode).replace('الحلقة','').replace('حلقة','').replace('الحلقه','').replace('حلقه','').strip()
            
            oGuiElement = cGuiElement('Episode ' + sEpisode, SITE_IDENTIFIER, 'showHosters')
            oGuiElement.setTVShowTitle(sShowName)
            oGuiElement.setSeason(sSeason)
            oGuiElement.setEpisode(sEpisode)
            oGuiElement.setMediaType('episode')
            params.setParam('sThumbnail', sThumbnail)
            params.setParam('sUrl', sUrl)
            cGui().addFolder(oGuiElement, params, False, total)
        
        sStart = '<div class="EpsList">'
        sEnd = '<div class="clr">'
        sHtmlContent1 = cParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = '<a href="([^<]+)" title=".*?">\s*(.*?)\s*</a>'  # start element
        isMatch, aResult = cParser.parse(sHtmlContent1, sPattern)
        if isMatch:
          total = len(aResult)
          for sUrl, sEpisode in aResult:
            sEpisode = sEpisode.replace('الحلقة','').replace('حلقة','').replace('الحلقه','').replace('حلقه','').strip()
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
    
    Handler = cRequestHandler(sUrl)
    Handler.addParameters('View', '1')
    sHtmlContent =Handler.request()
    
    sPattern = '<li data-link="(.+?)">'
    isMatch,aResult = cParser.parse(sHtmlContent, sPattern)
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
    
    
    sPattern = 'class="ser-link" href="(.+?)">'
    isMatch,aResult = cParser.parse(sHtmlContent, sPattern)
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


