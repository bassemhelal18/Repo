# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, dialog, addon
from resources.lib.util import cUtil, Unquote

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'akwam'
SITE_NAME = 'Akwam'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
oParser = cParser()
 
oRequestHandler = cRequestHandler(URL_MAIN)
sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+)

sPattern = '<meta property="og:url" content="(.+?)"/>'
aResult = oParser.parse(sHtmlContent, sPattern)
    
if (aResult[0]):
    URL_MAIN = aResult[1][0]

MOVIE_FAM = (URL_MAIN + '/movies?section=0&category=33&rating=0&year=0&language=0&formats=0&quality=0', 'showMovies')
MOVIE_AR = (URL_MAIN + '/movies?section=29', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + '/movies?section=0&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showMovies')
MOVIE_EN = (URL_MAIN + '/movies?section=30', 'showMovies')
MOVIE_HI = (URL_MAIN + '/movies?section=31', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/movies?section=33', 'showMovies')
KID_MOVIES = (URL_MAIN + '/movies?category=30', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/movies?section=32', 'showMovies')
MOVIE_TOP = (URL_MAIN + '/movies?section=30&category=0&rating=8&year=0&language=0&formats=0&quality=0', 'showMovies')
RAMADAN_SERIES = (URL_MAIN + '/series?section=0&category=87&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')
SERIE_EN = (URL_MAIN + '/series?section=30', 'showSeries')
SERIE_AR = (URL_MAIN + '/series?section=29', 'showSeries')
SERIE_HEND = (URL_MAIN + '/series?section=31', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/series?section=33', 'showSeries')
SERIE_TR = (URL_MAIN + '/series?section=32', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/series?section=30&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')

SERIE_TR_AR = (URL_MAIN + '/series?section=32&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')
SERIE_HEND_AR = (URL_MAIN + '/series?section=31&category=71&rating=0&year=0&language=0&formats=0&quality=0', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/series?category=30', 'showSeries')

DOC_NEWS = (URL_MAIN + '/movies?category=28', 'showMovies')
DOC_SERIES = (URL_MAIN + '/shows?section=46&category=0&rating=0&year=0&formats=0&quality=0', 'showSeries')

REPLAYTV_NEWS = (URL_MAIN + '/shows?section=42', 'showSeries')
REPLAYTV_PLAY = (URL_MAIN + '/shows?section=45', 'showMovies')

MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '/search?q=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/search?q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search?q=', 'showSeriesSearch')
URL_SEARCH_MISC = (URL_MAIN + '/search?q=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeries'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAll', 'Search All', icons + '/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', icons + '/Ramadan.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', icons + '/Documentary.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', icons + '/TVShowsTurkish-Dubbed.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية مدبلجة', icons + '/TVShowsHindi-Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', icons + '/Documentary.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', icons + '/Programs.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', icons + '/Theater.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1925, 2023)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/movies?section=0&category=0&rating=0&language=0&formats=0&quality=0&year=' + sYear)  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, icons + '/Calendar.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
def showSearchAll():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?q='+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
 
def showSearch():
    oGui = cGui() 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?q='+sSearchText+'&section=movie&year=0&rating=0&formats=0&quality=0'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?q=+'+sSearchText+'&section=series&year=0&rating=0&formats=0&quality=0'
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
		
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'&section=movie&year=0&rating=0&formats=0&quality=0'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    

 # ([^<]+) .+?
    sPattern = '<span class="label quality">([^<]+)</span>.+?<a href="([^<]+)" class="box">.+?data-src="([^<]+)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">([^<]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    idPattern = '<a href=\"https://www.imdb.com/title/([^<]+)/\"'
    idParser = cParser()
    idResult = idParser.parse(sHtmlContent, idPattern)
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[3].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            if 'مدبلج' in sTitle:
              continue
            siteUrl = aEntry[1]
            s1Thumb = aEntry[2]
            sThumb = re.sub(r'thumb\/\d*x\d*\/','',s1Thumb)
            
            sYear = aEntry[4]
            DescPattern = '<div class=\"widget-body\">*[\s]*<h2><div class=\"text-white font-size-18\" style=\"line-height: 1\.7;\">.*<p>([^<]+)<\/p>'
            DescParser = cParser()
            DescResult = DescParser.parse(sHtmlContent, DescPattern)
            if DescResult[0]:
                sDesc = DescResult[1][0]
            else:
                sDesc = ''
            
            if idResult[0]:
                sId = idResult[1][0]
            else:
                sId = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('IMDBNumber', sId)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

 
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'&section=series&year=0&rating=0&formats=0&quality=0'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<span class="label quality">(.+?)</span>.+?<a href="(.+?)" class="box">.+?data-src="(.+?)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">(.+?)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemList =[]
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[3].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            sTitle = sTitle.split("الموسم")[0].split("الحلقة")[0].split("موسم")[0].split("حلقة")[0]
            siteUrl = aEntry[1]
            s1Thumb = aEntry[2]
            sThumb = re.sub(r'thumb\/\d*x\d*\/','',s1Thumb)
            #'https://img.akw.onl/uploads/vzDN3.jpg'
            #'https://img.akw.onl/thumb/178x260/uploads/vzDN3.jpg'
            #'https://img.akw.onl/thumb/520x760/uploads/vzDN3.jpg'
            sYear = aEntry[4]
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم السابع والعشرون","S27").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S")
            
            DescPattern = '<div class=\"widget-body\">*[\s]*<h2><div class=\"text-white font-size-18\" style=\"line-height: 1\.7;\">.*<p>([^<]+)<\/p>'
            DescParser = cParser()
            DescResult = DescParser.parse(sHtmlContent, DescPattern)
            if DescResult[0]:
                sDesc = DescResult[1][0]
            else:
                sDesc = ''
            if sTitle not in itemList:
                itemList.append(sTitle)
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                if '/movie/' in siteUrl:
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler) 
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
			
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    
     # (.+?) .+?  ([^<]+)
    sPattern = 'meta property=".+?title".+?content="([^<]+)".+?/>.+?<meta property=".+?image".+?content="([^<]+)".+?/>.+?<link rel=".+?" href="(.+?)">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

 
            sTitle = aEntry[0].replace(" | اكوام","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع و العشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9")
            if'موسم' not in aEntry[0]:
                sTitle =sTitle+' S1'
            siteUrl = aEntry[2]
            sThumb = aEntry[1]
            
            DescPattern = '<div class=\"widget-body\">*[\s]*<h2><div class=\"text-white font-size-18\" style=\"line-height: 1\.7;\">.*<p>([^<]+)<\/p>'
            DescParser = cParser()
            DescResult = DescParser.parse(sHtmlContent, DescPattern)
            if DescResult[0]:
                sDesc = DescResult[1][0]
            else:
                sDesc = ''
 

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)  
    # (.+?) .+?  ([^<]+)
    sPattern = '<a href="([^<]+)" class="text-white- ml-2 btn btn-light mb-2">(.+?)</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

 
            sTitle = aEntry[1].replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع و العشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9")
            if'موسم' not in aEntry[1]:
                sTitle =sTitle+' S1'
            siteUrl = aEntry[0]
            
            kRequestHandler = cRequestHandler(siteUrl)
            kHtmlContent = kRequestHandler.request()
            ThumbPattern = '<picture><img src=\"([^<]+)\".class=\"img-fluid\" alt=\".*</picture>'
            ThumbParser = cParser()
            ThumbResult = ThumbParser.parse(kHtmlContent, ThumbPattern)
            

            if ThumbResult[0]:
                s1Thumb = ThumbResult[1][0]
                sThumb = re.sub(r'thumb\/\d*x\d*\/','',s1Thumb)
            else:
                s1Thumb = aEntry[1]
                sThumb = re.sub(r'thumb\/\d*x\d*\/','',s1Thumb)

            #sThumb = sThumb
            DescPattern = '<div class=\"widget-body\">*[\s]*<h2><div class=\"text-white font-size-18\" style=\"line-height: 1\.7;\">.*<p>([^<]+)<\/p>'
            DescParser = cParser()
            DescResult = DescParser.parse(sHtmlContent, DescPattern)
            if DescResult[0]:
                sDesc = DescResult[1][0]
            else:
                sDesc = ''
 

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
         
       
    oGui.setEndOfDirectory() 
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<span class="label quality">([^<]+)</span>.+?<a href="([^<]+)" class="box">.+?data-src="([^<]+)" class="img-fluid w-100 lazy" alt="(.+?)".+?<span class="badge badge-pill badge-secondary ml-1">([^<]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemList =[]
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[3].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            sTitle = sTitle.split("الموسم")[0].split("الحلقة")[0].split("موسم")[0].split("حلقة")[0]
            siteUrl = aEntry[1]
            s1Thumb = aEntry[2]
            sThumb = re.sub(r'thumb\/\d*x\d*\/','',s1Thumb)
            sYear = aEntry[4]
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع و العشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9")
            
            DescPattern = '<div class=\"widget-body\">*[\s]*<h2><div class=\"text-white font-size-18\" style=\"line-height: 1\.7;\">.*<p>([^<]+)<\/p>'
            DescParser = cParser()
            DescResult = DescParser.parse(sHtmlContent, DescPattern)
            if DescResult[0]:
                sDesc = DescResult[1][0]
            else:
                sDesc = ''

            if sTitle not in itemList:
                itemList.append(sTitle)
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            


        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
    if not sSearch:
        oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sStart = 'class="header-link text-white">الحلقات</span>'
    sEnd = '<div class="widget-4 widget widget-style-1 more mb-4">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
  
     # (.+?) ([^<]+) .+?
    sPattern = 'class="text-white">(.+?)</a>.+?<a href="([^<]+)">.+?<img src="([^<]+)" class="img-fluid" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sEp = aEntry[0].split(':')[0]
            sEp = sEp.replace("الحلقة "," E").replace("حلقة "," E")
            sTitle = sMovieTitle+''+sEp
            siteUrl = aEntry[1]
            s1Thumb = aEntry[2]
            sThumb = re.sub(r'thumb\/\d*x\d*\/','',s1Thumb)
            
            DescPattern = '<div class=\"widget-body\">*[\s]*<h2><div class=\"text-white font-size-18\" style=\"line-height: 1\.7;\">.*<p>([^<]+)<\/p>'
            DescParser = cParser()
            DescResult = DescParser.parse(sHtmlContent, DescPattern)
            if DescResult[0]:
                sDesc = DescResult[1][0]
            else:
                sDesc = ''
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        

    # .+? ([^<]+)
    sPattern = '<a href="http([^<]+)/watch/(.+?)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    idPattern = '<a href=\"https://www.imdb.com/title/([^<]+)/\"'
    idParser = cParser()
    idResult = idParser.parse(sHtmlContent, idPattern)
    
   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]: 
            sTitle = sMovieTitle
            siteUrl = sUrl
            sThumb = sThumb
            
            DescPattern = '<div class=\"widget-body\">*[\s]*<h2><div class=\"text-white font-size-18\" style=\"line-height: 1\.7;\">.*<p>([^<]+)<\/p>'
            DescParser = cParser()
            DescResult = DescParser.parse(sHtmlContent, DescPattern)
            if DescResult[0]:
                sDesc = DescResult[1][0]
            else:
                sDesc = ''

            if idResult[0]:
                sId = idResult[1][0]
            else:
                sId = ''

 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('IMDBNumber', sId)
            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
       
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^<]+)" rel="next"'	 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oHosterGui = cHosterGui()

    if not oInputParameterHandler:
        oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern =  'href="(http[^<]+/watch/.+?)"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        murl =  aResult[1][0]
        oRequest = cRequestHandler(murl)
        sHtmlContent = oRequest.request()

    sPattern =  'href="(http[^<]+/watch/.+?)"'  
    aResult = oParser.parse(sHtmlContent,sPattern)
    
    if aResult[0]:
        murl =  aResult[1][0]

        oRequest = cRequestHandler(murl)
        sHtmlContent = oRequest.request()

    

    sPattern =  '>Click here</span>.+?<a href="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    
    if aResult[0]:
        murl =  aResult[1][0]
  
        oRequest = cRequestHandler(murl)
        oRequest.disableSSL()
        sHtmlContent = oRequest.request()
    
    import requests
    s = requests.Session() 
    from resources.lib import recaptcha_v2
    from resolveurl import common
    test = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha("6LdMb-QZAAAAAPpUMcYZSn9CpIgBqDVAfTx_SAao", lang='en', Referer=URL_MAIN)
    data = {'g-recaptcha-response':test}
    url = URL_MAIN+'/verify'
    headers = {'User-Agent': common.RAND_UA,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': murl,
                    'Content-Type': 'application/x-www-form-urlencoded'}
    r = s.post(url,data=data,headers=headers)
    rt = s.get(murl)
    sHtmlContent = rt.text
    
    oParser = cParser()           
    sPattern =  '<source.+?src="(.+?)".+?size="(.+?)"' 
	
                                                                 
    aResult = oParser.parse(sHtmlContent,sPattern)

    if aResult[0]:
       for aEntry1 in aResult[1]:
           sHosterUrl = aEntry1[0]
           sHost = aEntry1[1] 
           sTitle = ('%s  -[%sp]') % (sMovieTitle, sHost)  
           oHoster = cHosterGui().checkHoster(sHosterUrl)
           if oHoster:
              oHoster.setDisplayName(sTitle)
              oHoster.setFileName(sMovieTitle)
              cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

                
    oGui.setEndOfDirectory()

    
    