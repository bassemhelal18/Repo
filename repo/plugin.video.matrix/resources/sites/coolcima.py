# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'coolcima'
SITE_NAME = 'CoolCima'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'category/افلام-اجنبي/', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + 'category/افلام-اجنبي-مدبلجة/', 'showMovies')
MOVIE_AR = (URL_MAIN + 'category/افلام-عربي/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/افلام-هندي/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/افلام-اسيوية/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/افلام-تركي/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/افلام-كرتون/', 'showMovies')

SERIE_TR = (URL_MAIN + 'category/مسلسلات-تركي-مترجمة/', 'showSeries')
SERIE_TR_AR = (URL_MAIN + 'category/مسلسلات-تركي-مدبلجة/', 'showSeries')
SERIE_DUBBED = (URL_MAIN + 'category/مسلسلات-اجنبية-مدبلجة/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/مسلسلات-اسيوي-مترجمة/', 'showSeries')
SERIE_HEND = (URL_MAIN + 'category/مسلسلات-هندي-مترجمة/', 'showSeries')
SERIE_HEND_AR = (URL_MAIN + 'category/مسلسلات-هندي-مدبلجة/', 'showSeries')
SERIE_LATIN = (URL_MAIN + 'category/مسلسلات-لاتينية/', 'showSeries')
SERIE_EN = (URL_MAIN + 'category/مسلسلات-اجنبي/', 'showSeries')
SERIE_AR = (URL_MAIN + 'category/مسلسلات-عربي/', 'showSeries')
RAMADAN_SERIES = (URL_MAIN + 'category/مسلسلات-رمضان-2024/', 'showSeries')
KID_CARTOON = (URL_MAIN + 'category/مسلسلات-كرتون-مترجمة/', 'showSeries')

DOC_SERIES = (URL_MAIN + 'genre/وثائقي', 'showSeries')
SPORT_WWE = (URL_MAIN + 'category/عروض-مصارعة-مترجمة/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'category/مسلسلات-انمي-مترجمة/', 'showSeries')
ANIM_MOVIES = (URL_MAIN + 'category/افلام-انمي/', 'showMovies')
REPLAYTV_PLAY = (URL_MAIN + 'category/مسرحيات/', 'showMovies')
REPLAYTV_NEWS = (URL_MAIN + 'category/برامج-تلفزيونية/', 'showSeries')

URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), icons + '/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية مدبلجة', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HEND_AR[1], 'مسلسلات هندية مدبلج', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات لاتنية', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', icons + '/Anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/مسلسلات-انمي-مدبلجة/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/مسلسلات-انمي-مدبلجة/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', icons + '/Documentary.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', icons + '/Programs.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', icons + '/Theater.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', icons + '/WWE.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
        sUrl = URL_MAIN + '/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
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

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="block-post">\s*<a href="([^"]+)" title="([^"]+)".+?data-img="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if '/episode' in aEntry[0] or '/serie' in aEntry[0]:
                continue

            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","Kamla").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("كول سيما","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2].replace("(","").replace(")","")
            sDesc = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                if 'عرض' in sTitle:
                    sTitle = sTitle.replace('عرض','')
                else:
                    sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            			
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
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

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
        
    sPattern = '<div class="block-post">\s*<a href="([^"]+)" title="([^"]+)".+?data-img="([^"]+)'
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
            if '/movie' in aEntry[0]:
                continue

            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("كول سيما","")
            sTitle = sTitle.split("الموسم")[0].split("الحلقة")[0].split("موسم")[0].split("حلقة")[0]
            siteUrl = aEntry[0]          
            sThumb = aEntry[2]
            sDesc=''
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
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons +'/next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
			
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()     
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="tabCon" id="seasons">'
    sEnd = '<div class="tabCon"'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = '<div class="block-post">\s*<a href="([^"]+)".+?data-img="([^"]+)".+?</li>\s*<li>(.+?)</li>'
    aResult = oParser.parse(sHtmlContent1, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

            sSeason = aEntry[2].replace("الموسم ","S")
            sTitle = f'{sMovieTitle} {sSeason}'
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:

        sStart = '<div class="tabCon episodes" id="episodes">'
        sEnd = '</ul>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'href="([^"]+)".+?<span>الحلقة</span>(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)   
        if aResult[0] is True:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
                sEp = aEntry[1]
                sTitle = f'{sMovieTitle} E{sEp}'
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ''
                sHost = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sHost', sHost)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
             
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="tabCon" id="episodes">'
    sEnd = '</ul>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?<span>الحلقة</span>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sEp = aEntry[1]
            sTitle = f'{sMovieTitle} E{sEp}'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sHost = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			    
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
      
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a class="next page-numbers" href="([^<]+)">'	 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    
    return False

def showLinks(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    Referer = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = 'link rel="shortlink" href="(.*?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0]):
        sMain = aResult[1][0].split('?p')[0]
        
    sPattern =  '<a rel="nofollow" href="(.*?)" class="btn watch">'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sID = aResult[1][0] 
        oRequestHandler = cRequestHandler(sID)
        oRequestHandler.addHeaderEntry('Referer',sMain)
        sHtmlContent = oRequestHandler.request()
        
        sPattern = '<a href=javascript.*?data-src\s*=(.*?)>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
           for aEntry in aResult[1]:

               url = aEntry
               if url.startswith('//'):
                 url = 'http:' + url
               sHosterUrl = url 
               oHoster = cHosterGui().checkHoster(sHosterUrl)
               if oHoster:
                  oHoster.setDisplayName(sMovieTitle)
                  oHoster.setFileName(sMovieTitle)
                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)             
        else:
            sUrl2 = sUrl+'watch/'
            oRequestHandler = cRequestHandler(sUrl2)
            sHtmlContent = oRequestHandler.request()
            sPattern =  'vo_postID = "([^"]+)' 
            aResult = oParser.parse(sHtmlContent,sPattern)
            if aResult[0]:
                sID = aResult[1][0] 

            sPattern = 'id="s_.+?onClick="([^"]+)".+?class="server">(.+?)</i>'
            aResult = oParser.parse(sHtmlContent,sPattern)
            if aResult[0]:
            
                for aEntry in aResult[1]:
                    ServerIDs = aEntry[0].replace('getServer2(this.id,','').replace(');','') 
                    sHosterID = ServerIDs.split(',')[0]
                    serverId = ServerIDs.split(',')[1]
      
                    url = f'{URL_MAIN}wp-content/themes/coolcima/temp/ajax/iframe2.php?id={sID}&video={sHosterID}&serverId={serverId}'
                    oParser = cParser()
                    oRequestHandler = cRequestHandler(url)
                    cook = oRequestHandler.GetCookies()
                    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
                    oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
                    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
                    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
                    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
                    oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
                    sHtmlContent2 = oRequestHandler.request()
    
                    sPattern = 'iframe.+?src="([^"]+)'
                    aResult = oParser.parse(sHtmlContent2, sPattern)
                    if aResult[0]:
                        sHosterUrl = aResult[1][0]

                        if 'mystream' in sHosterUrl:
                            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster != False:
                           oHoster.setDisplayName(sMovieTitle)
                           oHoster.setFileName(sMovieTitle)
                           cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)
    
    
    sUrl = sUrl+'downloads/'
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sStart = '<div class="DownList">'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?</span><span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            url = aEntry[0]
            sQual = aEntry[1]
            if url.startswith('//'):
               url = 'http:' + url

            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sDisplayTitle = ('%s-[%s]') % (sMovieTitle, sQual)
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()

