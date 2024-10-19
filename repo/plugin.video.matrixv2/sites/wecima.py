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

SITE_IDENTIFIER = 'wecima'
SITE_NAME = 'Wecima'
SITE_ICON = 'wecima.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'wecima.movie')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'category/أفلام/10-movies-english-افلام-اجنبي/'
URL_MOVIES_Arabic = URL_MAIN + 'category/افلام/افلام-عربي-arabic-movies/'
URL_SERIES_English = URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/5-series-english-%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a/'
URL_SERIES_Arabic = URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/13-%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a%d9%87-arabic-series/'
URL_MOVIES_Kids = URL_MAIN + 'category/افلام-كرتون/'
URL_SEARCH = URL_MAIN + 'search/%s'

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
    sHtmlContent = oRequest.request()
    sStart = '<div class="Grid--WecimaPosts">'
    sEnd = '</wecima>'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    pattern = '<a href="([^<]+)" title="(.+?)">.+?image:url(.+?);"><div.+?class="year">(.+?)</span>'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    for sUrl, sName,sThumbnail,sYear  in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        sName = sName.replace('مترجمة','').replace('مترجم','').replace('فيلم','').replace('مشاهدة','').replace('مسلسل','').replace('اون','').replace('أون','').replace('كامل','').replace('لاين','').split('الموسم')[0].split('موسم')[0].split('الحلقة')[0].split('حلقة')[0].split('حلقه')[0].replace('سلسل','').strip()
        m = re.search('([0-9]{4})', sName)
        if m:
            sYear = str(m.group(0))
            sName = sName.replace(sYear,'').replace('()','')
        if sName not in itemList:
            itemList.append(sName)
            sThumbnail=sThumbnail.replace("(","").replace(")","")
            isTvshow, aResult = cParser.parse(unquote(sUrl), 'مسلسل')
            if not isTvshow:
              isTvshow, aResult = cParser.parse(unquote(sUrl),'حلقة')
              if not isTvshow:
               isTvshow, aResult = cParser.parse(unquote(sUrl),'series')
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
            params.setParam('sUrl', sNextUrl)
            params.setParam('trumb', os.path.join(ART, 'Next.png'))
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        
            oGui.setView('tvshows' if isTvshow else 'movies')
            oGui.setEndOfDirectory()



def showSeasons():
    params = ParameterHandler()
    sUrl = params.getValue('sUrl')
    sUrl = sUrl.split('/')[-2]
    sUrl = URL_MAIN+sUrl
    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    seasonList =[]
    pattern = 'href="([^<]+)">موسم(.+?)</a>'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if  isMatch:
     total = len(aResult)
    
     for sUrl,sSeason in aResult:
        sSeason = sSeason.replace(sName,'').replace('مترجمة','').replace('كامل','').replace('مترجم','').replace('فيلم','').replace('مشاهدة','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').replace("الموسم العاشر","10").replace("الموسم الحادي عشر","11").replace("الموسم الثاني عشر","12").replace("الموسم الثالث عشر","13").replace("الموسم الرابع عشر","14").replace("الموسم الخامس عشر","15").replace("الموسم السادس عشر","16").replace("الموسم السابع عشر","17").replace("الموسم الثامن عشر","18").replace("الموسم التاسع عشر","19").replace("الموسم العشرون","20").replace("الموسم الحادي و العشرون","21").replace("الموسم الثاني و العشرون","22").replace("الموسم الثالث و العشرون","23").replace("الموسم الرابع والعشرون","24").replace("الموسم الخامس و العشرون","25").replace("الموسم السادس والعشرون","26").replace("الموسم السابع و العشرون","27").replace("الموسم الثامن والعشرون","28").replace("الموسم التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الموسم الحادي و الثلاثون","31").replace("الموسم الثاني والثلاثون","32").replace("الموسم الثالث و الثلاثون","33").replace("الموسم الأول","1").replace("الموسم الاول","1").replace("الموسم الثاني","2").replace("الموسم الثالث","3").replace("الموسم الثالث","3").replace("الموسم الرابع","4").replace("الموسم الخامس","5").replace("الموسم السادس","6").replace("الموسم السابع","7").replace("الموسم الثامن","8").replace("الموسم التاسع","9").replace('موسم','').strip()
        isSeason,sSeason = cParser.parse(sSeason, '\d+')
        if not isSeason:
         sSeason='1'
        sSeason=str(sSeason).replace("['","").replace("']","").strip()
        if sSeason not in seasonList:
            seasonList.append(sSeason)
            oGuiElement = cGuiElement('Season'+' ' +sSeason, SITE_IDENTIFIER, 'showEpisodes')
            oGuiElement.setTVShowTitle(sName)
            oGuiElement.setSeason(sSeason)
            oGuiElement.setMediaType('season')
            params.setParam('sThumbnail', sThumbnail)
            params.setParam('sUrl', sUrl)
            cGui().addFolder(oGuiElement, params, True, total)
    
    pattern = '<a class="unline" itemprop="item" href="([^<]+)"><span itemprop="name">موسم(.+?)</span></a>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if  isMatch:
        total = len(aResult)
    
        for sUrl,sSeason in aResult:
           sSeason = sSeason.replace(sName,'').replace('مترجمة','').replace('كامل','').replace('مترجم','').replace('فيلم','').replace('مشاهدة','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').replace("الموسم العاشر","10").replace("الموسم الحادي عشر","11").replace("الموسم الثاني عشر","12").replace("الموسم الثالث عشر","13").replace("الموسم الرابع عشر","14").replace("الموسم الخامس عشر","15").replace("الموسم السادس عشر","16").replace("الموسم السابع عشر","17").replace("الموسم الثامن عشر","18").replace("الموسم التاسع عشر","19").replace("الموسم العشرون","20").replace("الموسم الحادي و العشرون","21").replace("الموسم الثاني و العشرون","22").replace("الموسم الثالث و العشرون","23").replace("الموسم الرابع والعشرون","24").replace("الموسم الخامس و العشرون","25").replace("الموسم السادس والعشرون","26").replace("الموسم السابع و العشرون","27").replace("الموسم الثامن والعشرون","28").replace("الموسم التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الموسم الحادي و الثلاثون","31").replace("الموسم الثاني والثلاثون","32").replace("الموسم الثالث و الثلاثون","33").replace("الموسم الأول","1").replace("الموسم الاول","1").replace("الموسم الثاني","2").replace("الموسم الثالث","3").replace("الموسم الثالث","3").replace("الموسم الرابع","4").replace("الموسم الخامس","5").replace("الموسم السادس","6").replace("الموسم السابع","7").replace("الموسم الثامن","8").replace("الموسم التاسع","9").replace('موسم','').strip()
           isSeason,sSeason = cParser.parse(sSeason, '\d+')
           if not isSeason:
             sSeason='1'
           sSeason=str(sSeason).replace("['","").replace("']","").strip()
           if sSeason not in seasonList:
            seasonList.append(sSeason)
            oGuiElement = cGuiElement('Season'+' ' +sSeason, SITE_IDENTIFIER, 'showEpisodes')
            oGuiElement.setTVShowTitle(sName)
            oGuiElement.setSeason(sSeason)
            oGuiElement.setMediaType('season')
            params.setParam('sThumbnail', sThumbnail)
            params.setParam('sUrl', sUrl)
            cGui().addFolder(oGuiElement, params, True, total)
    else:
          pattern = '<a class="unline" itemprop="item" href="([^<]+)"><span itemprop="name">(.+?)</span>'  # start element
          isMatch, aResult = cParser.parse(sHtmlContent, pattern)
          if  isMatch:
           total = len(aResult)
    
           for sUrl,sSeason in aResult:
             sSeason = sSeason.replace(sName,'').replace('مترجمة','').replace('كامل','').replace('مترجم','').replace('فيلم','').replace('مشاهدة','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').replace("الموسم العاشر","10").replace("الموسم الحادي عشر","11").replace("الموسم الثاني عشر","12").replace("الموسم الثالث عشر","13").replace("الموسم الرابع عشر","14").replace("الموسم الخامس عشر","15").replace("الموسم السادس عشر","16").replace("الموسم السابع عشر","17").replace("الموسم الثامن عشر","18").replace("الموسم التاسع عشر","19").replace("الموسم العشرون","20").replace("الموسم الحادي و العشرون","21").replace("الموسم الثاني و العشرون","22").replace("الموسم الثالث و العشرون","23").replace("الموسم الرابع والعشرون","24").replace("الموسم الخامس و العشرون","25").replace("الموسم السادس والعشرون","26").replace("الموسم السابع و العشرون","27").replace("الموسم الثامن والعشرون","28").replace("الموسم التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الموسم الحادي و الثلاثون","31").replace("الموسم الثاني والثلاثون","32").replace("الموسم الثالث و الثلاثون","33").replace("الموسم الأول","1").replace("الموسم الاول","1").replace("الموسم الثاني","2").replace("الموسم الثالث","3").replace("الموسم الثالث","3").replace("الموسم الرابع","4").replace("الموسم الخامس","5").replace("الموسم السادس","6").replace("الموسم السابع","7").replace("الموسم الثامن","8").replace("الموسم التاسع","9").replace('موسم','').strip()
             isSeason,sSeason = cParser.parse(sSeason, '\d+')
             if not isSeason:
               sSeason='1'
             sSeason=str(sSeason).replace("['","").replace("']","")
             if sSeason not in seasonList:
               seasonList.append(sSeason)
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
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sSeason = params.getValue('season')
    sShowName = params.getValue('sName')
    
    
    pattern = '<a class="hoverable activable.+?href="([^<]+)"><div class="Thumb"><span><i class="fa fa-play"></i></span></div><episodeArea><episodeTitle>([^<]+)</episodeTitle></episodeArea></a>'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if isMatch:
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
    
    pattern = '<div class="MoreEpisodes.+?" data-term="([^<]+)">'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if isMatch:
     total = len(aResult)
     for data in aResult:
        import requests
        s = requests.Session()            
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
        r1 = s.get(URL_MAIN+'/AjaxCenter/MoreEpisodes/'+data+'/30/', headers=headers)
        sHtmlContent1 = r1.content.decode('utf8').replace("\\","")
        r2 = s.get(URL_MAIN+'/AjaxCenter/MoreEpisodes/'+data+'/70/', headers=headers)
        sHtmlContent2 = r2.content.decode('utf8').replace("\\","")
        r3 = s.get(URL_MAIN+'/AjaxCenter/MoreEpisodes/'+data+'/110/', headers=headers)
        sHtmlContent3 = r3.content.decode('utf8').replace("\\","")
        sHtmlContent = sHtmlContent1+sHtmlContent2+sHtmlContent3
        sPattern = 'href=([^<]+)"><div.+?<episodeTitle>([^<]+)<'
        isMatch, aResult = cParser.parse(sHtmlContent, sPattern)
        if isMatch:
         total = len(aResult)
         for sUrl,sEpisode in aResult:
          sEpisode = sEpisode.replace('الحلقة','').replace('حلقة','').replace('الحلقه','').replace('حلقه','').replace("u0627u0644u062du0644u0642u0629","")
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
    sR,sUrl = sUrl.split('watch')
    sUrl = URL_MAIN+'watch'+sUrl
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    
    sPattern = '<btn data-url="([^<]+)" class="hoverable activable">'
    isMatch,aResult = cParser.parse(sHtmlContent, sPattern)
    if isMatch:
       for shost in aResult :
        sName = cParser.urlparse(shost)
        sName =  sName.split('.')[-2]
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
        if 'youtube' in shost:
            continue
        if 'goveed' or '/run/' in shost:
            shost = shost+'$$'+URL_MAIN
        elif shost.startswith('//'):
               shost = 'https:' + shost
        hoster = {'link': shost, 'name': sName, 'displayedName':sName} # Qualität Anzeige aus Release Eintrag
        hosters.append(hoster)
    
    
    
    sPattern = 'class="hoverable activable" target="_blank" href="([^<]+)"><quality>.*?</quality><resolution><i class=".+?"></i>([^<]+)</resolution>'
    isMatch,aResult = cParser.parse(sHtmlContent, sPattern)
    if isMatch:
       for shost,sQuality  in aResult :
        
        sName = cParser.urlparse(shost)
        sName =  sName.split('.')[-2]
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
        if 'top15top'in shost:
           sName='Wecima'
           shost = shost +'|Referer='+URL_MAIN
        if 'youtube' in shost:
            continue
        elif shost.startswith('//'):
               shost = 'https:' + shost
        hoster = {'link': shost, 'name': sName, 'displayedName':sName+' '+sQuality, 'quality': sQuality} # Qualität Anzeige aus Release Eintrag
        hosters.append(hoster)
    
    
    if hosters:
        hosters.append('getHosterUrl')
    return hosters

def getHosterUrl(sUrl=False):
    if '|Referer'in sUrl:
        sUrl = sUrl.replace(' ','%20')
        return [{'streamUrl': sUrl, 'resolved': True}]
    return [{'streamUrl': sUrl, 'resolved': False}]
    

def showSearch():
    sSearchText = cGui().showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    cGui().setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_SEARCH % cParser.quotePlus(sSearchText), oGui, sSearchText)

