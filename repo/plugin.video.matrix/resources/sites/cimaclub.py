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
import requests


ADDON = addon()
icons = ADDON.getSetting('defaultIcons')


SITE_IDENTIFIER = 'cimaclub'
SITE_NAME = 'Cimaclub'
SITE_DESC = 'arabic vod'
 

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

    




MOVIE_FAM = (URL_MAIN + 'getposts?genre=%D8%B9%D8%A7%D8%A6%D9%84%D9%8A&category=1', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'getposts?type=one&data=rating', 'showMovies')
MOVIE_EN = (URL_MAIN + 'category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%89-aflam-onilne15', 'showMovies')
MOVIE_AR = (URL_MAIN + 'category/aflam-arabia-arabic-movies', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%AA%D8%B1%D9%83%D9%8A%D8%A9', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%B3%D9%8A%D9%88%D9%8A%D8%A9', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%86%D9%8A%D9%85%D9%8A%D8%B4%D9%86', 'showMovies')
MOVIE_MOVIE = (True, 'load')
RAMADAN_SERIES = (URL_MAIN + 'category/مسلسلات-رمضان-2023', 'showSerie')
SERIE_LATIN = (URL_MAIN + 'category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A8%D8%B1%D8%A7%D8%B2%D9%8A%D9%84%D9%8A%D8%A9', 'showSerie')
SERIE_DUBBED = (URL_MAIN + 'category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D9%87', 'showSerie')
SERIE_ASIA = (URL_MAIN + 'category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%83%D9%88%D8%B1%D9%8A', 'showSerie')
SERIE_TR = (URL_MAIN + 'category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A%D9%87', 'showSerie')
SERIE_EN = (URL_MAIN + 'category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showSerie')
SERIE_AR = (URL_MAIN + 'category/arabic-series-moslslat', 'showSerie')
SERIE_GENRES = (True, 'showGenres')
ANIM_NEWS = (URL_MAIN + 'category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%86%D9%8A%D9%85%D9%8A', 'showSerie')
DOC_NEWS = (URL_MAIN + 'category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9', 'showMovies')
DOC_SERIES = (URL_MAIN + 'category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9', 'showSerie')
SPORT_NEWS = (URL_MAIN + 'category/%D8%A7%D9%84%D9%85%D8%B5%D8%A7%D8%B1%D8%B9%D9%87-wwe', 'showMovies')
REPLAYTV_NEWS = (URL_MAIN + 'category/%D9%85%D8%B3%D8%B1%D8%AD%D9%8A%D8%A7%D8%AA-%D9%88%D8%B9%D8%B1%D9%88%D8%B6-%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D9%87', 'showSeries')
URL_SEARCH = (URL_MAIN + 'search?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'search?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?s=مسلسل+', 'showSerie')
URL_SEARCH_MISC = (URL_MAIN + 'search?s=', 'showSerie')
FUNCTION_SEARCH = 'showMovies'


UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

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
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات أسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', icons + '/Documentary.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات وثائقية', icons + '/Documentary.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', icons + '/WWE.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'عروض تلفزيونية',icons + '/Programs.png', oOutputParameterHandler) 
    
    oGui.setEndOfDirectory()
 


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return 
def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search?s=مسلسل+'+ sSearchText
        showSerie(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["korean series","http://cimaclub.com/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%83%D9%88%D8%B1%D9%8A%D8%A9/"] )
    liste.append( ["مسلسلات-رمضان-2016","http://cimaclub.com/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86-2016/"] )
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSerie',sTitle, icons + '/Genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()   

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?

    sPattern = '<div class="content-box">.+?<a href="([^<]+)" data-src="([^<]+)" class="image"></a>.+?<h3>([^<]+)</h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("اونلاين","").replace("برنامج","").replace("بجودة","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","مدبلج").replace("انيمي","")
            if 'مدبلج' in sTitle:
              continue
            siteUrl = aEntry[0].replace('/film/','/watch/').replace('/post/','/watch/')
            sThumb = aEntry[1].replace('(','').replace(')','')
            sDesc = ''
            sYear = ''
            m = re.search('([1-2][0-9]{3})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
       oGui.setEndOfDirectory()



def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    
    
 
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="content-box">.+?<a href="(.+?)".+?data-src="(.+?)".+?<h3>([^<]+)</h3></a>'

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
            if'/series/'in aEntry[0]:
                continue
            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مشاهده","").replace("مسلسل","").replace("انيمي","").replace("انمي","").replace("انمى","").replace("مترجمة","").replace("برنامج","").replace("مترجم","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مدبلج للعربية","مدبلج").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("انيمي","").replace("كامل","")  
            sTitle = sTitle.split("الموسم")[0].split("الحلقة")[0].split("موسم")[0].split("حلقة")[0]
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sTitle = sTitle.strip()
            
            if sTitle not in itemList:
                itemList.append(sTitle)
                
            
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
    
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
    soup = BeautifulSoup(sHtmlContent,"html.parser") 
    
    
    
    
    sPattern = 'data-season=".+?" data-series=".+?"><a href="([^<]+)" title="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("كامل","").replace("برنامج","").replace("فيلم","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            siteUrl = aEntry[0]
            sThumb = ''
            sDesc = ""
            sTitle = sTitle.strip()
            
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)	
    else:
     sStart = '<h2 class="title ti-list-numbered f13"> باقى المواسم</h2>'
     sEnd = '<h2 class="title ti-list-numbered f13"> جميع الحلقات </h2>'
     sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
  
     # (.+?) ([^<]+) .+?
     sPattern = '<a href="([^<]+)" class=".+?"><h3>.+?<span>([^<]+)</span></h3></a>'
     aResult = oParser.parse(sHtmlContent, sPattern)

     if aResult[0] :
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
            
                
            
             siteUrl = aEntry[0].replace("/episode/","/watch/").replace("/post/","/watch/")
             sSeason = ' S'+aEntry[1]
             sTitle = sMovieTitle + sSeason
             sThumb =  ''
             sDesc = ""
             sTitle = sTitle.strip()
             
             oOutputParameterHandler.addParameter('siteUrl',siteUrl)
             oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
             oOutputParameterHandler.addParameter('sMovieUrl', sUrl)
             oOutputParameterHandler.addParameter('sThumb', sThumb)
             oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
     else:
         sPattern = '</div><a href="(.+?)".+?class="poster-image" data-src="(.+?)".+?<h1>(.+?)</h1>'

         oParser = cParser()
         aResult = oParser.parse(sHtmlContent, sPattern)
	
	
         if aResult[0] :
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
            
             if'/season/'in aEntry[0]:
                continue   
            
            siteUrl = aEntry[0].replace("/episode/","/watch/").replace("/post/","/watch/")
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("كامل","").replace("برنامج","").replace("فيلم","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            sTitle = sTitle.split("الحلقة")[0].split("حلقة")[0]
            if'موسم' not in aEntry[0]:
                sTitle =sTitle+' S1'
            sThumb =  aEntry[1]
            sDesc = ""
            sTitle = sTitle.strip()
            


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
 # ([^<]+) .+?
    oParser = cParser()

    sStart = '<div class="row gutter-small">'
    sEnd = '<div class="carousel-slider glide glide-rtl glide-carousel glide-swipeable">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = '<a href="(.+?)" class="col-6 col-s-4 col-m-3 col-l-1 button-block"><h3>([^<]+)<span>([^<]+)</span></h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            if'/season/'in aEntry[0]:
                continue
            siteUrl = aEntry[0].replace("/episode/","/watch/").replace("/post/","/watch/")
            
            sTitle = sMovieTitle+" E"+aEntry[2]
            sThumb = ''
            sDesc = ""
            


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc , oOutputParameterHandler)
    else:
     sPattern = '<a class="Hoverable" href="(.+?)".+?<em>(.+?)</em>'

     oParser = cParser()
     aResult = oParser.parse(sHtmlContent, sPattern)
	
	
     if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            if'/season/'in aEntry[0]:
                continue
            siteUrl = aEntry[0].replace("/episode/","/watch/").replace("/post/","/watch/")
            
            sTitle = sMovieTitle+" E"+aEntry[1]
            sThumb = ''
            sDesc = ""
            


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc , oOutputParameterHandler)        
   
    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="active"><a href="javascript:;">.+?</a></li><li><a href="(.+?)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] :
        
        return aResult[1][0]

    return False
  
def showServers(oInputParameterHandler = False):
    oGui = cGui()
   
    if not oInputParameterHandler:
        oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    sReferer = sUrl.split('/watch')[0]
   
    oParser = cParser()
    
    #Recuperation infos

    sPattern = '&_post_id=([^<]+)",'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        spost = aResult[1][0]
    # (.+?) ([^<]+) .+?

    sPattern = 'data-embedd="(.+?)">(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0]:
        for aEntry in aResult[1]:


            sId = URL_MAIN + '/ajaxCenter?_action=getserver&_post_id='+spost
            siteUrl = sId+'&serverid='+aEntry[0]
			
            oRequestHandler = cRequestHandler(siteUrl)
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sData = oRequestHandler.request()
   
            sPattern = '([^<]+)'
            oParser = cParser()
            aResult = oParser.parse(sData, sPattern)
	
            if aResult[0]:
               for aEntry in aResult[1]:
        
                   url = str(aEntry)
                   
                   sTitle = " "
                   sThumb = sThumb
                   if 'govid' in url:
                      url = url.replace("play","down").replace("embed-","")
                   if 'telvod.site/play/' in url:
                       url = url.replace("telvod.site","rbrb.site")
                   if url.startswith('//'):
                      url = 'http:' + url
								            
                   sHosterUrl = url
                   if 'nowvid' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'kvid' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'moshahda' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                   if 'darkveed' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   
                   if 'rbrb' in sHosterUrl or 'downvol' in sHosterUrl:
                      sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                    
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                      sDisplayTitle = sMovieTitle
                      oHoster.setDisplayName(sDisplayTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
       	
    sPattern = 'rel="nofollow" href="(.+?)" class'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = str(aEntry)
            sTitle = sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
				
					
            
            sHosterUrl = url 
            if 'nowvid' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'darkveed' in sHosterUrl:
                     sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'telvod' in sHosterUrl or 'downvol' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sDisplayTitle = sTitle
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

     
    oGui.setEndOfDirectory()	
 
