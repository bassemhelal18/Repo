﻿# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, isMatrix, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'spacepowerfan'
SITE_NAME = 'Spacepowerfan'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_MOVIES = (URL_MAIN + '/%d8%a3%d9%81%d9%84%d8%a7%d9%85/', 'showMovies')
ANIM_NEWS = (URL_MAIN + '/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام إنمي', icons + '/Anime.png', oOutputParameterHandler)  
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
   
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<article.+?href="([^<]+)">.+?data-lazy-src="([^<]+)" />.+?class="Title">([^<]+)</h3>.+?class="Year">(.+?)</span>.+?class="Description"><p>([^<]+)</p>'
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
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace('"',"").replace("&quot;","").replace("amp;","")
            sDesc = aEntry[4]
            sYear = aEntry[3]
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
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
    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<div class="Top">'
    sEnd = '<div class="WebDescription">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'class="TPost C"> <a href="([^<]+)">.+?data-lazy-src="(.+?)".+?class="Title">(.+?)</'

    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("أنمي","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        
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
    import requests
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    St=requests.Session()
    
    if not isMatrix(): 
       sHtmlContent = St.get(sUrl).content
    
    if isMatrix(): 
       sHtmlContent = St.get(sUrl).content.decode('utf-8')
    

     # (.+?) ([^<]+) .+?
    sPattern = 'data-tab="(.+?)">(.+?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0] :
        for aEntry in aResult[1]:
            sSeason = "S"+aEntry[0]
            if sSeason:
               sHtmlContent1 = aEntry[1]
               sPattern = '<img src="(http[^<]+)" alt.+?href="([^<]+)">(.+?)</a>'
               aResult = oParser.parse(sHtmlContent1, sPattern)
	
               if aResult[0] :
                   oOutputParameterHandler = cOutputParameterHandler()   
                   for aEntry in aResult[1]:
 
                       sTitle = aEntry[2].replace("الحلقة "," E").replace("حلقة "," E")
                       sTitle = sTitle.replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","").replace("الاخيرة","")
                       sTitle = sMovieTitle+' '+sSeason+sTitle
                       siteUrl = aEntry[1]
                       sThumb = aEntry[0]
                       sDesc = ""
			


                       oOutputParameterHandler = cOutputParameterHandler()
                       oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                       oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                       oOutputParameterHandler.addParameter('sThumb', sThumb)
                       oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        

       
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers" href="([^<]+)">'
	
    # (.+?) .+? ([^<]+)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] :
        return aResult[1][0]

    return False
	 
def showServers():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    #Recuperation infos
    sId = ''
     # (.+?) ([^<]+) .+?
    sPattern = '<iframe.+?src=(.+?) frameborder'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        for aEntry in aResult[1]:
            import requests
            sId = aEntry.replace('"',"").replace("&quot;","").replace("amp;","")
            sgn = requests.Session()
            data = sgn.get(sId).content
            sHtmlContent2 = data    
            sPattern = 'src="([^<]+)" frameborder'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0] :
                for aEntry in aResult[1]:
                    url = aEntry
                    sTitle = sMovieTitle
                    if url.startswith('//'):
                       url = 'http:' + url
                       
                    sHosterUrl = url 
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
				       
    oGui.setEndOfDirectory()