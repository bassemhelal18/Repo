﻿# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re	
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'arabsciences'
SITE_NAME = 'Arabsciences'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

DOC_NEWS = (URL_MAIN +'category/tv-channels/', 'showMovies')
DOC_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN +'?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN +'?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN +'?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', icons + '/Documentary.png', oOutputParameterHandler)
    

            
    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["natgeoad","https://arabsciences.com/category/tv-channels/natgeoad/"] )
    liste.append( ["quest-arabiya","https://arabsciences.com/category/tv-channels/quest-arabiya/"] )
    liste.append( ["jazeeradoc-tv-channels","https://arabsciences.com/category/tv-channels/jazeeradoc-tv-channels/"] )
    liste.append( ["alarabyatv","https://arabsciences.com/category/tv-channels/alarabyatv/"] )
    liste.append( ["bbc-arabic","https://arabsciences.com/category/tv-channels/bbc-arabic/"] )
    liste.append( ["natgeowild","https://arabsciences.com/category/tv-channels/natgeowild/"] )
    liste.append( ["dw-arabic","https://arabsciences.com/category/tv-channels/dw-arabic/"] )
    liste.append( ["arabi-tv","https://arabsciences.com/category/tv-channels/arabi-tv-channels/"] )
    liste.append( ["russia-today","https://arabsciences.com/category/tv-channels/russia-today/"] )
    liste.append( ["قناة صانعوا القرار","https://arabsciences.com/category/tv-channels/%D9%82%D9%86%D8%A7%D8%A9-%D8%B5%D8%A7%D9%86%D8%B9%D9%88%D8%A7-%D8%A7%D9%84%D9%82%D8%B1%D8%A7%D8%B1/"] )
    liste.append( ["othertv","https://arabsciences.com/category/tv-channels/othertv/"] )

    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies',sTitle, icons + '/Genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
	
	
	
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = 'https://arabsciences.com/?s='+sSearchText
        showMovies(sUrl)
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
 
# ([^<]+) .+?
    sPattern = '<a aria-label="(.+?)" href="(.+?)" class="post-thumb">.+?data-orig-file="(.+?)" data.+?class="post-excerpt">([^<]+)</p>'

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
 
            sTitle = aEntry[0]
            
            sThumb = aEntry[2]
            siteUrl = aEntry[1]
            sDesc = aEntry[3]
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^<]+)"><span class="pagination-icon" aria-hidden="true">'
	 #.+? ([^<]+)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] :
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    # ([^<]+)          

    sPattern = 'src=(.+?) frameborder'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0] :
        for aEntry in aResult[1]:
            
            url = aEntry.replace('?rel=0','').replace('"','')
            if url.startswith('//'):
                url = 'http:' + url
				
					
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'https://www.youtube.com/embed/(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0] :
        for aEntry in aResult[1]:
            
            url = 'https://www.youtube.com/embed/'+aEntry
				
					
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				          
           

    sPattern = '<iframe src=([^<]+) width='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0] :
        for aEntry in aResult[1]:
            
            url = aEntry.replace('?rel=0','').replace('"','')
            if url.startswith('//'):
               url = 'http:' + url
				
					
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()