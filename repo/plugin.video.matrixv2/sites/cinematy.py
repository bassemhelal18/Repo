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

SITE_IDENTIFIER = 'cinematy'
SITE_NAME = 'Cinematy'
SITE_ICON = 'cinematy.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'cdn-01.cinematy.click')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'category/افلام-اجنبي/'
URL_MOVIES_Arabic = URL_MAIN + 'category/افلام-عربي/'
URL_SERIES_English = URL_MAIN + 'category/مسلسلات-اجنبي/'
URL_SERIES_Arabic = URL_MAIN + 'category/مسلسلات-عربي/'
URL_MOVIES_Kids = URL_MAIN + 'category/افلام-كرتون/'
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
    oRequest = cRequestHandler(sUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<div class="block-post">\s*<a href="([^"]+)" title="([^"]+)".+?data-img="([^"]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    for sUrl, sName,sThumbnail  in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        
        sName = sName.replace('مترجمة','').replace('الجزء','الموسم').replace('مترجم','').replace('فيلم','').replace('مشاهدة','').replace('مسلسل','').replace('اون','').replace('أون','').replace('لاين','').split('الموسم')[0].split('الحلقة')[0].replace('سلسل','').replace("كول سيما","").replace("كامل","").strip()
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

    
    sStart = '<div class="tabCon" id="seasons">'
    sEnd = '<div class="tabCon" id="otherseries">'
    sHtmlContent1 = cParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<div class="block-post">\s*<a href="([^"]+)".+?data-img="([^"]+)"\s*title="(.*?)"'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent1, sPattern)
    if  isMatch:
     total = len(aResult)
    
     for sUrl,sThumbnail,sSeason in aResult:
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
     sPattern = '<meta property="og:title" content="(.*?)"'  # start element
     isMatch, aResult = cParser.parse(sHtmlContent1, sPattern)
     if  isMatch:
      total = len(aResult)
    
      for sSeason in aResult:
        isSeason,sSeason = cParser.parse(sSeason, '\d+ الموسم')
        if not isSeason:
         sSeason='1'
        sSeason=str(sSeason).replace("['","").replace("']","")
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
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('origin', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sSeason = params.getValue('season')
    sShowName = params.getValue('sName')
    
    
    sStart = '<div class="tabCon episodes" id="episodes">'
    sEnd = '</div>'
    sHtmlContent =cParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="(.+?)" title="(.+?)"'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, sPattern)
    if not isMatch: return
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
    sUrl2 = sUrl+'watch/'
    
    
    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent = oRequestHandler.request()
    sPattern =  'postid-(.*?)"' 
    isMatch, aResult = cParser().parse(sHtmlContent, sPattern)
    if isMatch:
        for sID  in aResult:
            sPattern = 'id="s_.+?onClick=".*?this.id,([^"]+),([^"]+)".+?class="server">.+?</i>'
            isMatch, aResult = cParser().parse(sHtmlContent, sPattern)
            if isMatch:
                for sHosterID ,serverId  in aResult:
                 
                 serverId = serverId.replace(');','')
                 
                 url = f'{URL_MAIN}wp-content/themes/vo2022/temp/ajax/iframe2.php?id={sID}&video={sHosterID}&serverId={serverId}'
             
                 oRequestHandler = cRequestHandler(url)
                 oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
                 oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
                 oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
                 oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
                 sHtmlContent2 = oRequestHandler.request()
                 
                 sPattern = 'src="([^"]+)"'
                 isMatch, aResult = cParser().parse(sHtmlContent2, sPattern)
                 if isMatch:
                  for sUrl4  in aResult:
                    megamax = next((x for x in ['megamax', 'm3lomatik', 'ciinematy'] if x in sUrl4), None)
                    if megamax:
                      sHtmlContent2 = cMegamax().GetUrls(sUrl4)
                      for item in sHtmlContent2:
                        sUrl = item.split(',')[0].split('=')[1]
                        sQuality = item.split(',')[1].split('=')[1]
                        
                        
                        sName = cParser.urlparse(sUrl)
                        sName =  sName.split('.')[-2]
                        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
                        if 'ma2d'  in sUrl:
                            sRefer = sUrl.split('/e/')[0]+'/'
                            sUrl = sUrl + "$$" + sRefer
                        if 'vidhidevip'  in sUrl:
                            sUrl = sUrl + "$$" + sRefer
                        if 'youtube' in sUrl:
                           continue
                        elif sUrl.startswith('//'):
                           sUrl = 'https:' + sUrl
                        hoster = {'link': sUrl, 'name': sName, 'displayedName':sName+' '+ sQuality, 'quality': sQuality} # Qualität Anzeige aus Release Eintrag
                        hosters.append(hoster)
                    else: 
                     sName = cParser.urlparse(sUrl4)
                     if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
                     if 'youtube' in sUrl4:
                        continue
                     elif sUrl4.startswith('//'):
                        sUrl4 = 'https:' + sUrl4
                     hoster = {'link': sUrl4, 'name': sName, 'displayedName':sName} # Qualität Anzeige aus Release Eintrag
                     hosters.append(hoster)
    
    sUrl3 = sUrl2.replace('/watch/','/downloads/')
    oRequestHandler = cRequestHandler(sUrl3)
    sHtmlContent = oRequestHandler.request()
    
    sStart = '<div class="DownList">'
    sEnd = '</div>'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<a href="([^"]+)".+?</span><span>(.+?)</span>'   
    isMatch, aResult = cParser().parse(sHtmlContent, sPattern)
    if isMatch:
      for sUrl,sQuality  in aResult:
            
            sName = cParser.urlparse(sUrl)
                
            if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
            if 'youtube' in sUrl:
                continue
            if 'ma2d' in sUrl:
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


