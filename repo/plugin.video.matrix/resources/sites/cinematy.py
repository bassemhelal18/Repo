# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager,addon
from resources.lib.parser import cParser
from resources.lib.util import Quote
from bs4 import BeautifulSoup
import os
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
SITE_IDENTIFIER = 'cinematy'
SITE_NAME = 'cinematy'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


MOVIE_EN = (URL_MAIN + '/category/افلام-اجنبي/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/افلام-عربي/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/افلام-هندي/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/category/افلام-اسيوية/', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/category/الأفلام-التركية/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/افلام-كرتون/', 'showMovies')
SERIE_TR = (URL_MAIN + '/category/مسلسلات-تركية-مترجمة/', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/category/مسلسلات-تركية-مدبلجة/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/category/مسلسلات-اسيوية/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/category/مسلسلات-هندى/', 'showSeries')
SERIE_EN = (URL_MAIN + '/category/مسلسلات-اجنبي/', 'showSeries')
SERIE_AR = (URL_MAIN + '/category/مسلسلات-عربي/', 'showSeries')
RAMADAN_SERIES = (URL_MAIN + '/category/مسلسلات-رمضان-2024/', 'showSeries')
KID_CARTOON = (URL_MAIN+'/category/مسلسلات-كرتون/', 'showSeries')
SPORT_WWE = (URL_MAIN + '/category/عروض-مصارعة/', 'showMovies')
ANIM_NEWS = (URL_MAIN + '/category/مسلسلات-انمي-مترجمة/', 'showSeries')
REPLAYTV_PLAY = (URL_MAIN + '/category/مسرحيات/', 'showMovies')
REPLAYTV_NEWS = (URL_MAIN + '/category/برامج-تلفزيونية/', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=فيلم+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=مسلسل+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)
 
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
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)  
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'برامج تلفزيونية',icons + '/Programs.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', icons + '/Theater.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مصارعة', icons + '/WWE.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
        sUrl = URL_MAIN + '/?s=فيلم+'+sSearchText+'&search=البحث'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
        sUrl = URL_MAIN + '/?s=مسلسل+'+sSearchText+'&search=البحث'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'&search=البحث'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    

 # ([^<]+) .+?
    sPattern = '<div class="block-post">.*?<a.*?href="([^<]+)" title="([^<]+)">.*?data-img="(.*?)"'

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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            if 'مدبلج' in sTitle:
              continue
            siteUrl = aEntry[0]+'watch/'
            sThumb = aEntry[2].replace("(","").replace(")","")
            sDesc = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
        progress_.VSclose(progress_)
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    
        oGui.setEndOfDirectory()

 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'&search=البحث'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    
    sPattern = '<div class="block-post">.*?<a.*?href="([^<]+)" title="([^<]+)">.*?data-img="(.*?)"'
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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("الجزء","الموسم").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            sTitle = sTitle.split("الموسم")[0].split("الحلقة")[0].split("موسم")[0].split("حلقة")[0]
            siteUrl = aEntry[0]+'watch/'
            
            sThumb = aEntry[2].replace("(","").replace(")","")
            sDesc=''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')
            
            sTitle = sTitle.strip()
            
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
			
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent2 = oRequestHandler.request()
    # (.+?) .+? ([^<]+)
    oParser = cParser()
    sStart = '<div class="tabCon" id="seasons">'
    sEnd = '<div class="tabCon" id="otherseries">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'div class="block-post">.*?<a href="([^<]+)" title="([^<]+)">.*?data-img="([^<]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("الجزء","الموسم").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("مترجم","").replace("الموسم","S").replace("مترجمة","").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'S1')
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:

        sStart = '<div class="tabCon episodes" id="episodes">'
        sEnd = '</div>'
        sHtmlContent = oParser.abParse(sHtmlContent2, sStart, sEnd)
    # (.+?) .+? ([^<]+)
        sPattern = 'href="(.+?)" title="(.+?)"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
    
        if aResult[0] is True:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:

 
                
                sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
                sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع و العشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9")
                sTitle = sTitle.replace("الحلقة","E")
                
                m = re.search('([0-9]{4})', sTitle)
                if m:
                   sYear = str(m.group(0))
                   sTitle = sTitle.replace(sYear,'S1')
                siteUrl = aEntry[0]+'watch/'
                
                sThumb = ''
                sDesc = ''
                sHost = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
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
    sStart = '<div class="tabCon episodes" id="episodes">'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="(.+?)" title="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0] is True:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:

 
                
                sTitle = aEntry[1].replace("الحلقة","E").replace("E ","E")
                sTitle = sMovieTitle+sTitle
                sTitle = sTitle.strip()
                m = re.search('([0-9]{4})', sTitle)
                if m:
                   sYear = str(m.group(0))
                   sTitle = sTitle.replace(sYear,'S1')
                siteUrl = aEntry[0]+'watch/'
               
                sThumb = ''
                sDesc = ''
                

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			    
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)


            
 
       
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a class="next page-numbers" href="([^<]+)">'	 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

    return False

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    if not oInputParameterHandler:
        oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()  
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern =  "<link rel='dns-prefetch' href='([^']+)' />" 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        urlre = aResult[1][0] 
        if urlre.startswith('//'):
               urlre = 'https:' + urlre
        
    oParser = cParser()
    sPattern =  'postid-(.*?)"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sID = aResult[1][0] 

    ## Watch Servers
    sPattern = 'id="s_.+?onClick="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            ServerIDs = aEntry.replace('getServer2(this.id,','').replace(');','') 
            sHosterID = ServerIDs.split(',')[0]
            serverId = ServerIDs.split(',')[1]

            url = URL_MAIN + 'wp-content/themes/vo2022/temp/ajax/iframe2.php?id=' + sID + '&video=' + sHosterID + '&serverId=' + serverId
            oRequestHandler = cRequestHandler(url)
            cook = oRequestHandler.GetCookies()
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
            oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
            oRequestHandler.addHeaderEntry('authority', 'cinematy.online'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
            sHtmlContent2 = oRequestHandler.request()

            sPattern = 'iframe.+?src=\"(.+?)\"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0]
                sTitle = sMovieTitle
                if 'mystream' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                if 'ma2d' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + urlre
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    ## Download Servers
    sUrl = sUrl.replace('/watch/','/downloads/')
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()  
    sHtmlContent = oRequestHandler.request()
    
    sStart = '<div class="DownList">'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = '<a href="([^"]+)".+?</span><span>(.+?)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            url = aEntry[0]
            sQual = '['+aEntry[1] +']'
            sTitle = sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
            if 'ma2d' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + urlre
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle+sQual)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()