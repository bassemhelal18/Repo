# -*- coding: utf-8 -*-


from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, VSlog
import resolveurl
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

class cHosterGui:
    SITE_NAME = 'cHosterGui'
    ADDON = addon()

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl=False, oInputParameterHandler=False):
        oHoster.setUrl(sMediaUrl)
        oOutputParameterHandler = cOutputParameterHandler()
        if not oInputParameterHandler:
            oInputParameterHandler = cInputParameterHandler()

        # Gestion NextUp
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        site = oInputParameterHandler.getValue('site')
        saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        sSeason = oInputParameterHandler.getValue('sSeason')
        sEpisode = oInputParameterHandler.getValue('sEpisode')
        nextSaisonFunc = oInputParameterHandler.getValue('nextSaisonFunc')
        movieUrl = oInputParameterHandler.getValue('movieUrl')
        movieFunc = oInputParameterHandler.getValue('movieFunc')
        sLang = oInputParameterHandler.getValue('sLang')
        sRes = oInputParameterHandler.getValue('sRes')
        sTmdbId = oInputParameterHandler.getValue('sTmdbId')
        sFav = oInputParameterHandler.getValue('sFav')
        if not sFav:
            sFav = oInputParameterHandler.getValue('function')
        searchSiteId = oInputParameterHandler.getValue('searchSiteId')
        if searchSiteId:
            oOutputParameterHandler.addParameter('searchSiteId', searchSiteId)
        oOutputParameterHandler.addParameter('searchSiteName', oInputParameterHandler.getValue('searchSiteName'))
        oOutputParameterHandler.addParameter('sQual', oInputParameterHandler.getValue('sQual'))
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')

        # Catégorie de lecture
        if oInputParameterHandler.exist('sCat'):
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat == '4':  # Si on vient de passer par un menu "Saison" ...
                sCat = '8'   # ...  On est maintenant au niveau "Episode"
        else:
            sCat = '5'     # Divers
        
        oGuiElement.setCat(sCat)
        oOutputParameterHandler.addParameter('sCat', sCat)

        if (oInputParameterHandler.exist('sMeta')):
            sMeta = oInputParameterHandler.getValue('sMeta')
            oGuiElement.setMeta(int(sMeta))

        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        oGuiElement.setIcon(icons+'/Sources.png')
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setPoster(sThumbnail)
        
        sMediaFile = oHoster.getMediaFile()
        if sMediaFile:  # Afficher le nom du fichier plutot que le titre
            oGuiElement.setMediaUrl(sMediaFile)
            if self.ADDON.getSetting('display_info_file') == 'true':
                oHoster.setDisplayName(sMediaFile)
                oGuiElement.setTitle(oHoster.getFileName())  # permet de calculer le cleanTitle
                oGuiElement.setRawTitle(oHoster.getDisplayName())   # remplace le titre par le lien
            else:
                oGuiElement.setTitle(oHoster.getDisplayName())
        else:
            oGuiElement.setTitle(oHoster.getDisplayName())   
        
        
        title = oGuiElement.getCleanTitle()
        tvShowTitle = oGuiElement.getItemValue('tvshowtitle')
        
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        oOutputParameterHandler.addParameter('tvShowTitle', tvShowTitle)
        oOutputParameterHandler.addParameter('sTitle', title)
        oOutputParameterHandler.addParameter('sSeason', sSeason)
        oOutputParameterHandler.addParameter('sEpisode', sEpisode)
        oOutputParameterHandler.addParameter('sLang', sLang)
        oOutputParameterHandler.addParameter('sRes', sRes)
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)


        # gestion NextUp
        oOutputParameterHandler.addParameter('sourceName', site)    # source d'origine
        oOutputParameterHandler.addParameter('sourceFav', sFav)    # source d'origine
        oOutputParameterHandler.addParameter('nextSaisonFunc', nextSaisonFunc)
        oOutputParameterHandler.addParameter('saisonUrl', saisonUrl)
        oOutputParameterHandler.addParameter('realHoster', oHoster.getRealHost())

        # gestion Lecture en cours
        oOutputParameterHandler.addParameter('movieUrl', movieUrl)
        oOutputParameterHandler.addParameter('movieFunc', movieFunc)

        # Download menu
        if oHoster.isDownloadable():
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadList')
            oContext.setTitle(self.ADDON.VSlang(30202))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

            # Beta context download and view menu
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadListandview')
            oContext.setTitle(self.ADDON.VSlang(30326))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

        # Liste de lecture
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(self.ADDON.VSlang(30201))
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

        # Dossier Media
        oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cLibrary', 'cLibrary', 'setLibrary', self.ADDON.VSlang(30324))
        # Upload menu uptobox
        if cInputParameterHandler().getValue('site') != 'siteuptobox' and self.ADDON.getSetting('hoster_uptobox_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = ['uptobox', 'uptostream', '1fichier', 'uploaded', 'uplea']
            for i in accept:
                if host == i:
                    oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteuptobox', 'siteuptobox', 'upToMyAccount', self.ADDON.VSlang(30325))

        # onefichier
        if cInputParameterHandler().getValue('site') != 'siteonefichier' and self.ADDON.getSetting('hoster_onefichier_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = '1fichier'  # les autres ne fonctionnent pas
            if host == accept:
                oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteonefichier', 'siteonefichier', 'upToMyAccount', '1fichier')

        oGui.addFolder(oGuiElement, oOutputParameterHandler, False)

    def checkHoster(self, sHosterUrl, debrid=True):
        # securite
        if not sHosterUrl:
            return False

        # Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]
        sHosterUrl = sHosterUrl.split('?')[0]
        sHosterUrl = sHosterUrl.lower()

        # lien direct ?
        if any(sHosterUrl.endswith(x) for x in ['.avi', '.flv', '.m3u8', '.webm', '.mpd']):
            return self.getHoster('lien_direct')
        # Recuperation du host
        try:
            sHostName = sHosterUrl.split('/')[2]
        except:
            sHostName = sHosterUrl

        if debrid:
            # L'user a active l'url resolver ?
            if self.ADDON.getSetting('Userresolveurl') == 'true':
                import resolveurl
                hmf = resolveurl.HostedMediaFile(url=sHosterUrl)
                if hmf.valid_url():
                    tmp = self.getHoster('resolver')
                    RH = sHosterUrl.split('/')[2]
                    RH = RH.replace('www.', '')
                    tmp.setRealHost('['+RH.split('.')[-2].upper()+']')
                    return tmp



            # L'user a activé alldebrid ?
            if self.ADDON.getSetting('hoster_alldebrid_premium') == 'true':
                f = self.getHoster('alldebrid')
                #mise a jour du nom
                sRealHost = self.checkHoster(sHosterUrl, False)
                if sRealHost:
                    sHostName = sRealHost.getPluginIdentifier()
                f.setRealHost(sHostName)
                return f
					
            # L'user a activé realbrid ?
            if self.ADDON.getSetting('hoster_realdebrid_premium') == 'true':
                f = self.getHoster('realdebrid')
                #mise a jour du nom
                sRealHost = self.checkHoster(sHosterUrl, False)
                if sRealHost:
                    sHostName = sRealHost.getPluginIdentifier()
                f.setRealHost(sHostName)
                return f
					
            # L'user a activé debrid_link ?
            if self.ADDON.getSetting('hoster_debridlink_premium') == 'true':
                if "debrid.link" not in sHosterUrl:
                    return self.getHoster('debrid_link')
                else:
                    return self.getHoster("lien_direct")

                
        supported_player = ['hdup', 'streamable', 'stardima', 'filescdn', 'vidgot', 'videott', 'vidlo', 'sendit', 'thevid', 'vidmoly', 'fastplay', 'cloudy', 'hibridvod', 'arabveturk', 'extremenow', 'yourupload', 'vidspeeds', 'moshahda', 'voe', 'faselhd', 'streamz', 'streamax', 'gounlimited', 'xdrive', 'mixloads', 'vidoza',
                            'rutube', 'megawatch', 'vidzi', 'filetrip', 'speedvid', 'netu', 
                            'onevideo', 'playreplay', 'prostream', 'vidfast', 'uptostream', 'uqload', 'letwatch',
                            'filepup', 'vimple', 'wstream', 'watchvideo', 'vidwatch', 'up2stream', 'tune', 'playtube',
                            'vidup', 'vidbull', 'vidlox', '33player' 'easyload', 'ninjastream', 'cloudhost',
                            'videobin', 'stagevu', 'gorillavid', 'daclips', 'hdvid', 'vshare', 'streamlare', 'vidload',
                            'giga', 'megadrive', 'downace', 'clickopen', 'supervideo',
                            'jawcloud', 'soundcloud', 'mixcloud', 'ddlfr', 'vupload', 'dwfull', 'vidzstore',
                            'pdj', 'rapidstream', 'jetload', 'dustreaming', 'viki', 'flix555', 'onlystream', 'vudeo', 'vidia', 'uptobox', 'uplea',
                            'sibnet', 'vidplayer', 'userload', 'aparat', 'evoload', 'abcvideo', 'plynow', '33player', 'filerio', 'videoraj', 'brightcove', 'detectiveconanar']

        val = next((x for x in supported_player if x in sHostName), None)
        if val:
            return self.getHoster(val.replace('.', ''))

        # Gestion classique
        if ('vadshar' in sHostName) or ('vidshar' in sHostName) or ('vedshaar' in sHostName) or ('viidshar' in sHostName) or  ('vedsharr' in sHostName) or ('vedshar' in sHostName) or ('vidshare' in sHostName) or ('vid1shar' in sHostName):
            return self.getHoster('vidshare')
        if ('streamtape' in sHostName) or ('streamnoads' in sHostName):
            return self.getHoster('streamtape')
        if ('mixdrop' in sHostName)or ('mdy48tn97' in sHostName)or ('mixdroop'in sHostName):
            return self.getHoster('mixdrop')
        if ('sbfull' in sHostName):
            return self.getHoster('resolver')
        if ('sbbrisk' in sHostName):
            return self.getHoster('resolver')
        if ('luluvdo' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost('[LULUVDO]')
            return f
        if ('streamhub' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost('[STREAMHUB]')
            return f
        if ('upstream' in sHostName):
            return self.getHoster('upstream')
        
        if ('highload' in sHostName):
            return self.getHoster('resolver')
        if ('videa' in sHostName):
            return self.getHoster('resolver')
        if ('letsupload' in sHostName):
            return self.getHoster('resolver')
        if ('vanfem' in sHostName):
            return self.getHoster('fembed')
        if ('streamhide' in sHostName):
            return self.getHoster('resolver')
        if ('vidpro' in sHostName):
            return self.getHoster('samashare')
        if ('streamvid' in sHostName):
            return self.getHoster('resolver')
        if ('vidspeed' in sHostName):
            return self.getHoster('vidspeeds')
        if ('allviid' in sHostName):
            return self.getHoster('allvid')
        if ('gofile' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost('[GOFILE]')
            return f
        if ('drop.download' in sHostName):
            return self.getHoster('resolver')

        if ('sblanh' in sHostName):
            return self.getHoster('resolver')
        if ('sbchill' in sHostName):
            return self.getHoster('resolver')
        if ('sbthe' in sHostName):
            return self.getHoster('resolver')
        if ('sbbrisk' in sHostName):
            return self.getHoster('resolver')
        if ('sbanh' in sHostName):
            return self.getHoster('resolver')
        if ('viewsb' in sHostName):
            return self.getHoster('resolver')
        if ('tubeload' in sHostName):
            return self.getHoster('resolver')
        if ('vimeo' in sHostName):
            return self.getHoster('resolver')
        if ('embed.scdn.' in sHostName):
            return self.getHoster('faselhd')
        if ('/run/' in sHosterUrl):
            return self.getHoster('mycima')
        if ('weecima' in sHostName):
            return self.getHoster('megavideo')            
        if ('megaupload.' in sHostName) or ('fansubs' in sHostName) or ('us.archive.' in sHostName) or ('ddsdd' in sHostName) or ('ffsff' in sHostName) or ('rrsrr.' in sHostName)or ('fbcdn.net' in sHostName) or ('blogspot.com' in sHostName) or ('videodelivery' in sHostName) or ('bittube' in sHostName) or ('amazonaws.com' in sHostName):
            return self.getHoster('lien_direct')
        
        if ('film77' in sHostName):
            return self.getHoster('film77')
        
        if ('file-upload' in sHostName):
            return self.getHoster('fileupload')
        
        if ('lanesh' in sHosterUrl):
            return self.getHoster('lanesh')
        
        if ('liiivideo' in sHostName):
            return self.getHoster('qfilm')
        
        if ('rumble' in sHostName):
            return self.getHoster('rumble')

        if ('streamwish' in sHostName)or ('ankrzkz' in sHostName) or ('cilootv' in sHostName)or ('sfastwish' in sHostName)or ('egtpgrvh' in sHostName) or ('volvovideo' in sHostName):
           return self.getHoster('streamwish')
        
        if ('rabbitstream' in sHostName) or ('dokicloud' in sHostName):
            return self.getHoster('streamrapid')
        
        if ('motvy55' in sHostName) or ('filelions' in sHostName) or ('fviplions' in sHostName)or ('lylxan' in sHostName)or ('lumiawatch' in sHostName):
            return self.getHoster('filelions')
        
        if ('workupload' in sHostName):
            return self.getHoster('workupload')
        
        if ('vkplay' in sHostName):
            return self.getHoster('vkplay')

        if ('sharecast' in sHostName):
            return self.getHoster('sharecast')

        if ('live7' in sHostName):
            return self.getHoster('live7')

        if ('voodc' in sHostName):
            return self.getHoster('voodc')
        
        if ('hadara.ps' in sHostName):
            return self.getHoster('lien_direct')
        
        if ('vidtube' in sHostName)or ('vtbe' in sHostName):
            return self.getHoster('vidtube')

        if ('updown' in sHostName):
            return self.getHoster('updown')
        
        if ('.googleusercontent.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('archive.org/download' in sHostName):
            return self.getHoster('lien_direct')

        if ('ak-download' in sHostName):
            return self.getHoster('lien_direct')
        
        if ('newcima' in sHostName):
            return self.getHoster('lien_direct')
        
        if ('rrsrrs' in sHostName):
            return self.getHoster('cimanow')
        
        if ('app.box' in sHostName):
            return self.getHoster('lien_direct')

        if ('nextcdn' in sHostName):
            return self.getHoster('lien_direct')

        if ('akwam' in sHostName):
            return self.getHoster('lien_direct')

        if ('.vimeocdn.' in sHostName):
            return self.getHoster('lien_direct')

        if ('bokracdn' in sHostName):
            return self.getHoster('lien_direct')

        if ('akoams.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('gcdn' in sHostName):
            return self.getHoster('lien_direct')

        

        if ('alarabiya' in sHostName):
            return self.getHoster('lien_direct')

        if ('kingfoot' in sHostName):
            return self.getHoster('lien_direct')
            
        if (('vidbm' in sHostName) or ('vadbam' in sHostName) or ('vedbom' in sHostName) or ('vadbom' in sHostName) or ('vidbam' in sHostName) or
            ('viidshar' in sHostName) or ('allviid' in sHostName) or ('vidspeed' in sHostName)or ('vedbam' in sHostName) or ('viboom' in sHostName)):
            return self.getHoster('vidbom')
				
        if ('mail.ru' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost('[MAIL.RU]')
            return f
				
        if ('streamcherry' in sHostName):
            return self.getHoster('resolver')
			
        if ('twitch' in sHostName):
            return self.getHoster('resolver')
			
        if ('clicknupload' in sHostName):
            return self.getHoster('resolver')
        
        if ('vidguard' in sHostName) or ('vembed' in sHostName) or ('vgfplay' in sHostName)or ('vgembed' in sHostName)or ('vid-guard' in sHostName)or ('v6embed' in sHostName):
            return self.getHoster('vidguard')

        if ('linkbox' in sHostName) or ('sharezweb' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost('[LINKBOX]')
            return f
        
        if ('vidoba' in sHostName):
             return self.getHoster('vidoba')
            
        if ('mediafire' in sHostName):
            return self.getHoster('mediafire')

        if ('workupload' in sHostName):
            return self.getHoster('workupload')

        if ('upbaam' in sHostName) or ('upbam' in sHostName) or ('uppom' in sHostName) or ('uppboom' in sHostName) or ('upgobom' in sHostName)or ('uupbom' in sHostName):
            return self.getHoster('uppom')
        
        if ('eeggyy' in sHosterUrl):
            return self.getHoster('egybest')

        if ('shoffree' in sHostName) or ('egy-best' in sHostName) or ('egy.best' in sHostName):
            return self.getHoster('shoffree')    
        
        if ('filemoon' in sHostName):
            return self.getHoster('resolver')
            
        if ('veehd.' in sHostName):
            return self.getHoster('veehd')
				
        if ('streamsforu' in sHostName or 'ylass' in sHostName or 'rsc.cdn' in sHostName or 'btolat' in sHostName):
            return self.getHoster('streamz')
				
        if ('archive.org/embed/"' in sHostName):
            return self.getHoster('archive')
				
        if (('anavids' in sHostName) or ('anavidz' in sHostName)):
            return self.getHoster('anavids')
				
        if (('anonfile' in sHostName) or ('govid.xyz' in sHostName) or ('file.bz' in sHostName) or ('myfile.is' in sHostName) or ('upload.st' in sHostName)):
            return self.getHoster('anonfile')

        if (('cloudvideo' in sHostName) or ('streamcloud' in sHostName) or ('userscloud' in sHostName)):
            return self.getHoster('cloudvid')
            
        if ('myviid' in sHostName) or ('myvid' in sHostName):
            return self.getHoster('myvid')
       
        if ('.aflam' in sHosterUrl):
            return self.getHoster('mixloads')			
        
        if ('mixloads' in sHosterUrl):
            return self.getHoster('mixloads')

        if ('streamwire' in sHostName) or ('vup' in sHostName):
            return self.getHoster('resolver')
            
        if ('vidhd' in sHostName) or ('oktube' in sHostName):
            return self.getHoster('vidhd')
            
        if ('skyvid' in sHostName)or ('gvadz' in sHostName):
            return self.getHoster('skyvid')
            
        if ('seeeed' in sHostName):
            return self.getHoster('arabseed')
            
        if ('reviewtech' in sHostName):
            return self.getHoster('arabseed')
            
        if ('4shared' in sHostName):
            return self.getHoster('shared')
				
        if ('fajer.live' in sHostName):
            return self.getHoster('fajerlive')
            
        if ('goved' in sHostName) or ('govad' in sHostName) or ('govid.me' in sHostName)or ('goveed' in sHosterUrl):
            return self.getHoster('govidme')
            
        if ('nowvid' in sHostName) or ('vegaasvid' in sHostName)or('govid' in sHostName) or ('drkvid' in sHosterUrl) or ('gvid.' in sHosterUrl) or ('govid.' in sHostName) or ('kopatube' in sHostName) or ('kobatube' in sHostName) or ('darkveed' in sHostName) or ('downvol' in sHosterUrl) or ('rbrb' in sHosterUrl)or ('telvod' in sHosterUrl) :
            return self.getHoster('govid')
        

        if ('vid4up' in sHostName):
            return self.getHoster('vidforup')
            
        if ('send.cm' in sHosterUrl):
            return self.getHoster('sendme')

        if ('avideo.host' in sHosterUrl):
            return self.getHoster('avideo')
        
        if ('vidhls' in sHosterUrl):
            return self.getHoster('vidhls')
        
        if ('vidguard' in sHostName) or ('fertoto' in sHostName) or ('vgembed' in sHostName) or ('vgfplay' in sHostName) or ('vid-guard' in sHostName):
            return self.getHoster('vidguard')
        
        if ('torrent' in sHosterUrl) or ('magnet:' in sHosterUrl):
            return self.getHoster('torrent')

        if ('play.imovietime' in sHosterUrl):
            return self.getHoster('moviztime')

        if ('mp4upload' in sHostName):
            return self.getHoster('mpupload')
            
        if ('fajer.video' in sHostName):
            return self.getHoster('fajer')
            
        if ('youtube' in sHostName) or ('youtu.be' in sHostName):
            return self.getHoster('youtube')

        if ('sama-share' in sHostName):
            return self.getHoster('samashare')

        if ('anafast' in sHostName) or ('anamov' in sHostName):
            return self.getHoster('anafasts')
        
        if ('akoam' in sHostName):
            return self.getHoster('lien_direct')

        if ('myvi.' in sHostName):
            return self.getHoster('myvi')

        if ('yodbox' in sHostName) or ('youdbox' in sHostName) or ('youdboox' in sHostName):
            return self.getHoster('youdbox')

        if ('yandex' in sHostName) or ('yadi.sk' in sHostName):
            return self.getHoster('yadisk')

        if ('vidbom' in sHostName):
            return self.getHoster('vidbom')

        if ('vedpom' in sHostName) or ('vidbem' in sHostName):
            return self.getHoster('vidbem')

        if ('vk.com' in sHostName) or ('vkontakte' in sHostName) or ('vkcom' in sHostName):
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost('[VK]')
            return f

        if ('playvidto' in sHostName):
            return self.getHoster('vidto')

        if ('hd-stream' in sHostName):
            return self.getHoster('hd_stream')
        
        if ('dooood.com' in sHostName) or('dood' in sHostName)or('ds2play' in sHostName) :
            return self.getHoster('dood')
        
        if ('livestream' in sHostName):
            return self.getHoster('lien_direct')

        if ('embedo' in sHostName):
            return self.getHoster('resolver')
        
        if ('reviewtech' in sHosterUrl) or ('reviewrate' in sHosterUrl):
            return self.getHoster('arabseed')
        
        

        # vidtodo et clone
        val = next((x for x in ['vidtodo', 'vixtodo', 'viddoto', 'vidstodo'] if x in sHostName), None)
        if val:
            return self.getHoster('vidtodo')

        if ('dailymotion' in sHostName) or ('dai.ly' in sHostName):
            try:
                if 'stream' in sHosterUrl:
                    return self.getHoster('lien_direct')
            except:
                pass
            else:
                return self.getHoster('dailymotion')
        if ('flashx' in sHostName) or ('filez' in sHostName):
            return self.getHoster('flashx')

        if ('mystream' in sHostName) or ('mstream' in sHostName):
            return self.getHoster('mystream')

        if ('streamingentiercom/videophp?type=speed' in sHosterUrl) or ('speedvideo' in sHostName):
            return self.getHoster('speedvideo')

        if ('googlevideo' in sHostName) or ('picasaweb' in sHostName) or ('googleusercontent' in sHostName):
            return self.getHoster('googlevideo')

        if ('ok.ru' in sHostName) or ('odnoklassniki' in sHostName):
            return self.getHoster('ok_ru')

        if ('iframe-secured' in sHostName):
            return self.getHoster('iframe_secured')

        if ('iframe-secure' in sHostName):
            return self.getHoster('iframe_secure')

        if ('thevideo' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName):
            return self.getHoster('thevideo_me')

        if ('drive.google.com' in sHostName) or ('docs.google.com' in sHostName):
            return self.getHoster('resolver')

        if ('stream.moe' in sHostName):
            return self.getHoster('streammoe')

        if ('movshare' in sHostName) or ('wholecloud' in sHostName):
            return self.getHoster('wholecloud')

        if ('upvid.' in sHostName):
            return self.getHoster('upvid')

        if ('upvideo' in sHostName) or ('streamon' in sHostName):
            return self.getHoster('upvideo')

        if ('estream' in sHostName) and not ('widestream' in sHostName):
            return self.getHoster('estream')

        if ('clipwatching' in sHostName) or ('highstream' in sHostName):
            return self.getHoster('clipwatching')

        if ('goo.gl' in sHostName) or ('bit.ly' in sHostName) or ('streamcrypt' in sHostName) or ('opsktp' in sHosterUrl):
            return self.getHoster('allow_redirects')

        # frenchvid et clone
        val = next((x for x in ['french-vid', 'diasfem', 'yggseries', 'fembed', 'fem.tohds', 'feurl', 'fsimg', 'core1player',
                                'vfsplayer', 'gotochus', 'suzihaza', 'sendvid', "femax"] if x in sHostName), None)
        if val:
            return self.getHoster("fembed")

        if ('directmoviedl' in sHostName) or ('moviesroot' in sHostName):
            return self.getHoster('directmoviedl')

        # Lien telechargeable a convertir en stream
        if ('1fichier' in sHostName):
            return self.getHoster('1fichier')

        if ('uploaded' in sHostName) or ('ul.to' in sHostName):
            if ('/file/forbidden' in sHosterUrl):
                return False
            return self.getHoster('uploaded')

        if ('myfiles.alldebrid.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('.m3u8' in sHosterUrl):
            return self.getHoster('lien_direct')
        if ('akwam' in sHostName) or ('.akw.' in sHostName) or ('اكوام' in sHostName)  or ('AKWAM.' in sHostName) or ('ak4ar' in sHostName)or ('onesav' in sHostName)or ('akdl.link' in sHostName):
            return self.getHoster('lien_direct')
        
				
        if ('nitroflare' in sHostName or 'tubeload.' in sHostName or 'Facebook' in sHostName  or 'fastdrive' in sHostName or 'megaup.net' in sHostName  or 'openload' in sHostName or 'doodrive' in sHostName or 'fikper' in sHostName or 'turbobit' in sHostName
            or 'rapidgator' in sHostName or 'katfile' in sHostName or 'mega4upload.com' in sHostName or 'megamax' in sHostName):
            return False

        
        # lien direct ?
        
        if any(sHosterUrl.endswith(x) for x in ['.mp4', '.avi', '.flv', '.m3u8', '.webm', '.mkv', '.mpd']):
            return self.getHoster('lien_direct')

        else:
            f = self.getHoster('resolver')
            #mise a jour du nom
            f.setRealHost(sHostName)
            return f            
        
            
    
    def getHoster(self, sHosterFileName):
        mod = __import__('resources.hosters.' + sHosterFileName, fromlist=['cHoster'])
        klass = getattr(mod, 'cHoster')
        return klass()

    def play(self, oInputParameterHandler = False, autoPlay = False):
        oGui = cGui()
        oDialog = dialog()

        if not oInputParameterHandler:
            oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sTitle = oInputParameterHandler.getValue('sTitle')
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sCat = oInputParameterHandler.getValue('sCat')
        sMeta = oInputParameterHandler.getValue('sMeta')

        if not sTitle:
            sTitle = sFileName

        if bGetRedirectUrl == 'True':
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        try:
            mediaDisplay = sMediaUrl.split('/')
            VSlog('Hoster %s - play : %s/ ... /%s' % (sHosterIdentifier,'/'.join(mediaDisplay[0:3]), mediaDisplay[-1]))
        except:
            VSlog('Hoster %s - play : ' % (sHosterIdentifier, sMediaUrl))

        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        sHosterName1=sMediaUrl.split('/')[2]
                                  
        sHosterName1 = sHosterName1.replace('www.', '')
        sHosterName1 = sHosterName1.split('.')[-2].upper()
        sHosterIdentifier1 = sHosterIdentifier.replace('lien_direct','Direct Link')
        if not autoPlay:
            oDialog.VSinfo(sHosterName1, sHosterIdentifier1.upper())
        

        try:
            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink(autoPlay)

            if aLink and (aLink[0] or aLink[1]):  # Le hoster ne sait pas résoudre mais a retourné une autre url
                if not aLink[0]:  # Voir exemple avec allDebrid qui : return False, URL
                    oHoster = self.checkHoster(aLink[1], debrid=False)
                    if oHoster:
                        oHoster.setFileName(sFileName)
                        sHosterName = oHoster.getDisplayName()
                        if not autoPlay:
                            oDialog.VSinfo(sHosterName, 'Resolve')

                        oHoster.setUrl(aLink[1])
                        aLink = oHoster.getMediaLink(autoPlay)

                if aLink[0]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(self.SITE_NAME)
                    oGuiElement.setSiteUrl(siteUrl)
                    oGuiElement.setMediaUrl(aLink[1])
                    oGuiElement.setFileName(sFileName)
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.setCat(sCat)
                    oGuiElement.setMeta(int(sMeta))
                    oGuiElement.getInfoLabel()

                    from resources.lib.player import cPlayer
                    oPlayer = cPlayer(oInputParameterHandler)

                    # sous titres ?
                    if len(aLink) > 2:
                        oPlayer.AddSubtitles(aLink[2])

                    return oPlayer.run(oGuiElement, aLink[1])

            if not autoPlay:
                oDialog.VSerror(self.ADDON.VSlang(30020))
            return False

        except Exception as e:
            oDialog.VSerror(self.ADDON.VSlang(30020))
            import traceback
            traceback.print_exc()
            return False

        if not autoPlay:
            oGui.setEndOfDirectory()
        return False

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if bGetRedirectUrl == 'True':
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        VSlog('Hoster - playlist ' + sMediaUrl)
        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if aLink[0]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            from resources.lib.player import cPlayer
            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            dialog().VSinfo(str(oHoster.getFileName()), 'Playlist')
            return

        oGui.setEndOfDirectory()

    def __getRedirectUrl(self, sUrl):
        from resources.lib.handler.requestHandler import cRequestHandler
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
