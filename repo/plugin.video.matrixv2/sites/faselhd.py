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

SITE_IDENTIFIER = 'faselhd'
SITE_NAME = 'FaselHD'
SITE_ICON = 'faselhd.png'
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_'+ SITE_IDENTIFIER +'.domain', 'faselhd.cafe')
URL_MAIN = 'https://' + DOMAIN + '/'


URL_MOVIES_English = URL_MAIN + 'movies'
URL_SERIES_English = URL_MAIN + 'recent_series'
URL_MOVIES_Kids = URL_MAIN + 'dubbed-movies'
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
    
    
    sStart = 'id="postList"'
    sEnd = "<ul class='pagination justify-content-center'>"
    sHtmlContent2 = cParser.abParse(sHtmlContent, sStart, sEnd)
    pattern = '<div\s*class="postDiv\s*">\s*<a\s*href="(.*?)">.*?data-src="(.*?)".*?alt="(.*?)"'
    isMatch, aResult = cParser.parse(sHtmlContent2, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    itemList =[]
    total = len(aResult)
    for sUrl,sThumbnail, sName  in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        sName = sName.replace('مترجمة','').replace('مترجم','').replace('فيلم','').replace('مسلسل','').split('الموسم')[0].split('الحلقة')[0].replace('سلسل','')
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
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
            params.setParam('sUrl', sUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)
            params.setParam('sYear', sYear)

            oGui.addFolder(oGuiElement, params, isTvshow, total)
        
    if not sGui and not sSearchText:
        isMatchNextPage, sNextUrl = cParser.parseSingleResult(sHtmlContent,'''<a class="page-link" href='([^<]+)'>&rsaquo;</a>''')
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
    
    
    pattern = '''window.location.href = '(.*?)'.*?data-src="(.*?)".*?class="title">(.*?)</div>'''  # start element
    
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if  isMatch:
     total = len(aResult)
    
     for sUrl,sThumbnail,sSeason in aResult:
        sSeason = sSeason.replace('الموسم','').replace('موسم','')
        oGuiElement = cGuiElement('Season'+' ' +sSeason, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setMediaType('season')
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sUrl', URL_MAIN+sUrl)
        cGui().addFolder(oGuiElement, params, True, total)
    else:
     pattern = '''<link rel="canonical"\s*href="(.*?)".*?<div class="posterImg">.*?<img src="(.*?)".*?<div class="h1 title">\s*(.*?)\s*</div>'''  # start element
     isMatch, aResult = cParser.parse(sHtmlContent, pattern)
     if  isMatch:
      total = len(aResult)
    
      for sUrl,sThumbnail,sSeason in aResult:
        sSeason = sSeason.replace(sName,'').replace('مسلسل','').replace('سلسل','').replace("الموسم العاشر","10").replace("الموسم الحادي عشر","11").replace("الموسم الثاني عشر","12").replace("الموسم الثالث عشر","13").replace("الموسم الرابع عشر","14").replace("الموسم الخامس عشر","15").replace("الموسم السادس عشر","16").replace("الموسم السابع عشر","17").replace("الموسم الثامن عشر","18").replace("الموسم التاسع عشر","19").replace("الموسم العشرون","20").replace("الموسم الحادي و العشرون","21").replace("الموسم الثاني و العشرون","22").replace("الموسم الثالث و العشرون","23").replace("الموسم الرابع والعشرون","24").replace("الموسم الخامس و العشرون","25").replace("الموسم الخامس والعشرون","25").replace("الموسم السادس والعشرون","26").replace("الموسم السابع و العشرون","27").replace("الموسم الثامن والعشرون","28").replace("الموسم التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الموسم الحادي و الثلاثون","31").replace("الموسم الثاني والثلاثون","32").replace("الموسم الثالث و الثلاثون","33").replace("الموسم الرابع و الثلاثون","34").replace("الموسم الرابع والثلاثون","34").replace("الموسم الخامس والثلاثون","35").replace("الموسم الأول","1").replace("الموسم الاول","1").replace("الموسم الثاني","2").replace("الموسم الثالث","3").replace("الموسم الثالث","3").replace("الموسم الرابع","4").replace("الموسم الخامس","5").replace("الموسم السادس","6").replace("الموسم السابع","7").replace("الموسم الثامن","8").replace("الموسم التاسع","9")
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
    sThumbnail = params.getValue('sThumbnail')
    sHtmlContent = cRequestHandler(sUrl).request()
    sSeason = params.getValue('season')
    sShowName = params.getValue('sName')
    
    sStart = '<div class="epAll" id="epAll">'
    sEnd = '<div class="postShare">'
    sHtmlContent = cParser.abParse(sHtmlContent, sStart, sEnd)
    
    pattern = '<a href="(.+?)".*?>\s*(.*?)\s*</a>'  # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
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
    sHtmlContent = cRequestHandler(sUrl).request()
    
    
    pattern = "player_iframe.location.href = '([^<]+)&img.*?'" # start element
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch: return
    for slink in aResult:
        slink=slink.replace(' ','')
        oRequest = cRequestHandler(slink)
        oRequest.addHeaderEntry('referer',URL_MAIN)
        sHtmlContent = oRequest.request()
    page = prase_function(sHtmlContent)
    page =str(page.encode('latin-1'),'utf-8')

    Pattern =  'button class="hd_btn " data-url="([^<]+)">([^<]+)</button>'  # start element
    isMatch, aResult = cParser().parse(page, Pattern)
    if isMatch:
        for sUrl ,sQuality in aResult:
            sName = cParser.urlparse(sUrl)
            
             # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
            if 'youtube' in sUrl:
                continue
            elif sUrl.startswith('//'):
                 sUrl = 'https:' + sUrl
            elif 'fasel' in sUrl:
                sName = 'FaselHD'
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

def prase_function(data):
    if 'adilbo' in data:
     t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
     t_int = re.findall('/g.....(.*?)\)', data, re.S)
     if t_script and t_int:
         script = t_script[3].replace("'",'')
         script = script.replace("+",'')
         script = script.replace("\n",'')
         sc = script.split('.')
         page = ''
         for elm in sc:
             c_elm = base64.b64decode(elm+'==').decode()
             t_ch = re.findall('\d+', c_elm, re.S)
             if t_ch:
                nb = int(t_ch[0])+int(t_int[2])
                page = page + chr(nb)
    return page
