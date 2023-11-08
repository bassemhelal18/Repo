# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from bs4 import BeautifulSoup

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
 
SITE_IDENTIFIER = 'tuktukcinema'
SITE_NAME = 'Tuktukcinema'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


MOVIE_EN = (URL_MAIN + 'category/movies-33/افلام-اجنبي/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/movies-33/افلام-هندى/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/movies-33/افلام-اسيوي/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/movies-33/افلام-تركي/', 'showMovies')
MOVIE_PACK = (URL_MAIN , 'showPack')
KID_MOVIES = (URL_MAIN + 'category/anime-6/افلام-انمي/', 'showMovies')
SERIE_EN = (URL_MAIN + 'category/series-9/مسلسلات-اجنبي/', 'showSeries')
SERIE_HEND = (URL_MAIN + 'category/series-9/مسلسلات-هندي/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/series-9/مسلسلات-أسيوي/', 'showSeries')
SERIE_TR = (URL_MAIN + 'category/series-9/مسلسلات-تركي/', 'showSeries')
ANIM_NEWS = (URL_MAIN + 'category/anime-6/انمي-مترجم/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN +'?s=فيلم+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN +'?s=مسلسل+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
   
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
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', icons + '/Icon.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '?s=فيلم+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '?s=مسلسل+'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showPack(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
# ([^<]+) .+? 

    sPattern = '<a href="([^<]+)">([^<]+)</a>'


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","") 
            if 'مدبلج' in sTitle:
              continue
            sThumb = aEntry[1]
            siteUrl = aEntry[0]
            sDesc = ''
			

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'sercat' in siteUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, sThumb, oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, sThumb, oOutputParameterHandler)
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
    
        oGui.setEndOfDirectory()
			
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:   
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
      sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()

    # (.+?) .+? ([^<]+)   
    sPattern = '<div class="Block--Item"><a href="([^<]+)" title="([^<]+)"><div class="Poster--Block"><img src=".+?" data-src="([^<]+)" alt=".+?">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if 'مسلسل' in aEntry[1]:
                continue
            if 'الحلقة' in aEntry[1]:
                continue
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")
            if 'مدبلج' in sTitle:
              continue
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
        progress_.VSclose(progress_)

    sPattern = '<div class="Block--Item"> <a href="([^<]+)" title="([^<]+)"> <div class="Poster--Block"> <img src="([^<]+)" alt=".+?">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if 'مسلسل' in aEntry[1]:
                continue
            if 'الحلقة' in aEntry[1]:
                continue
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")
            if 'مدبلج' in sTitle:
              continue
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)        

        progress_.VSclose(progress_)
    
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
    
        oGui.setEndOfDirectory()



		
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
 # ([^<]+) .+? (.+?)
    sPattern = '<div class="Block--Item"><a href="([^<]+)" title="([^<]+)"><div class="Poster--Block"><img src=".+?" data-src="([^<]+)" alt=".+?">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemList = []
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'فيلم' in aEntry[1]:
                continue
            if 'والاخيرة' in aEntry[1]:
                continue
            sTitle = aEntry[1].replace("مشاهدة","").replace("والاخيرة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace(" والأخيرة","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","").replace("الموسم الحادي عشر","").replace("الموسم الثاني عشر","").replace("الموسم الثالث عشر","").replace("الموسم الرابع عشر","").replace("الموسم الخامس عشر","").replace("الموسم السادس عشر","").replace("الموسم السابع عشر","").replace("الموسم الثامن عشر","").replace("الموسم التاسع عشر","").replace("الموسم العشرون","").replace("الموسم الحادي و العشرون","").replace("الموسم الثاني و العشرون","").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","").replace("الموسم الخامس و العشرون","").replace("الموسم السادس والعشرون","").replace("الموسم السابع والعشرون","").replace("الموسم الثامن والعشرون","").replace("الموسم التاسع والعشرون","").replace("الموسم الثلاثون","").replace("الموسم الحادي و الثلاثون","").replace("الموسم الثاني والثلاثون","").replace("الموسم الاول","").replace("الموسم الثاني","").replace("الموسم الثالث","").replace("الموسم الثالث","").replace("الموسم الرابع","").replace("الموسم الخامس","").replace("الموسم السادس","").replace("الموسم السابع","").replace("الموسم الثامن","").replace("الموسم التاسع","").replace("الموسم","").replace("S ","").replace("الحلقة","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("10","").replace("11","").replace("12","").replace("13","").replace("14","").replace("15","").replace("16","").replace("17","").replace("18","").replace("19","").replace("20","").replace("21","").replace("22","").replace("23","").replace("24","").replace("25","").replace("26","").replace("27","").replace("28","").replace("29","").replace("30","").replace("0","").replace("season","")
            sTitle = sTitle.strip()
            
            if sTitle not in itemList:
                itemList.append(sTitle)
                


                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
            
    sPattern = '<div class="Block--Item"> <a href="([^<]+)" title="([^<]+)"> <div class="Poster--Block"> <img src="([^<]+)" alt=".+?">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemList = []
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if 'فيلم' in aEntry[1]:
                continue
            if 'والاخيرة' in aEntry[1]:
                continue
            sTitle = aEntry[1].replace("مشاهدة","").replace("والاخيرة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace(" والأخيرة","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","").replace("الموسم الحادي عشر","").replace("الموسم الثاني عشر","").replace("الموسم الثالث عشر","").replace("الموسم الرابع عشر","").replace("الموسم الخامس عشر","").replace("الموسم السادس عشر","").replace("الموسم السابع عشر","").replace("الموسم الثامن عشر","").replace("الموسم التاسع عشر","").replace("الموسم العشرون","").replace("الموسم الحادي و العشرون","").replace("الموسم الثاني و العشرون","").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","").replace("الموسم الخامس و العشرون","").replace("الموسم السادس والعشرون","").replace("الموسم السابع والعشرون","").replace("الموسم الثامن والعشرون","").replace("الموسم التاسع والعشرون","").replace("الموسم الثلاثون","").replace("الموسم الحادي و الثلاثون","").replace("الموسم الثاني والثلاثون","").replace("الموسم الاول","").replace("الموسم الثاني","").replace("الموسم الثالث","").replace("الموسم الثالث","").replace("الموسم الرابع","").replace("الموسم الخامس","").replace("الموسم السادس","").replace("الموسم السابع","").replace("الموسم الثامن","").replace("الموسم التاسع","").replace("الموسم","").replace("S ","").replace("الحلقة","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("10","").replace("11","").replace("12","").replace("13","").replace("14","").replace("15","").replace("16","").replace("17","").replace("18","").replace("19","").replace("20","").replace("21","").replace("22","").replace("23","").replace("24","").replace("25","").replace("26","").replace("27","").replace("28","").replace("29","").replace("30","").replace("0","").replace("season","")
            if sTitle not in itemList:
                itemList.append(sTitle)


                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
    if not sSearch:   
        sNextPage = __checkForNextPage(sHtmlContent)
        
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
     
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
    
    sStart = '<section class="allseasonss"'
    sEnd = '<section class="allepcont getMoreByScroll">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = 'href="(.+?)".+?<img src=".+?" alt="([^<]+)" data-srccs="([^<]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = sMovieTitle +' '+aEntry[1].replace("الموسم","S").replace("S ","S")
            
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
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
    
    sStart = '<section class="allepcont getMoreByScroll">'
    sEnd = '<section class="otherser"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = '<a href="(.+?)" title=.+?<div class="epnum"><span>الحلقة</span>(.+?)</div></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = " E"+aEntry[1].replace("E ","E")
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0]
            sThumb = ''
            sDesc = ''
            
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
  
     # (.+?)

def __checkForNextPage(sHtmlContent):

    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    sHtmlContent = str(soup.find("ul",{"class":"page-numbers"}))
    
    sPattern = '<a class="next page-numbers" href="(.+?)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        return URL_MAIN+aResult[1][0]

    return False

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    if not oInputParameterHandler:
        oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<a class="watchAndDownlaod" href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sUrl = aResult[1][0]
        VSlog(sUrl)
    
    sReferer=sUrl.split('watch/')[0]
    
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Accept-Encoding','gzip, deflate, br')
    oRequestHandler.addHeaderEntry('Referer',sReferer)
    sHtmlContent = oRequestHandler.request()
    sTitle = sMovieTitle

              
    
    sPattern = 'data-link="(.+?)" class='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:           
            url = aEntry.replace('https://http://','https://')
            
            if url.startswith('//'):
               url = 'http:' + url
			
            sTitle = sMovieTitle					
            sHosterUrl = url 
            
            
            if '?download_' in sHosterUrl:
               sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    # (.+?) ([^<]+) .+?

    sPattern = '<a target="_blank" href="(.+?)" class="download--direct"><i class="fa fa-download"></i><span>(.+?)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:           
            url = aEntry[0].replace('https://http://','https://')
            
            if url.startswith('//'):
               url = 'http:' + url
			
            sTitle = sMovieTitle					
            sHosterUrl = url 
            
            if '?download_' in sHosterUrl:
               sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'userload' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    # (.+?) ([^<]+) .+?

    sPattern = '<a target="_NEW" href="(.+?)" class="download--item">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:           
            url = aEntry.replace('https://http://','https://')
            
            if url.startswith('//'):
               url = 'http:' + url
			
            sTitle = sMovieTitle					
            sHosterUrl = url 
            
            if '?download_' in sHosterUrl:
              sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'userload' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
				                     
				               
    oGui.setEndOfDirectory()