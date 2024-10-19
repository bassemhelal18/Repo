# -*- coding: utf-8 -*-
# Python 3

import json
import os
import sys
import xbmcaddon

from resources.lib.config import cConfig
from xbmc import LOGINFO as LOGNOTICE, LOGERROR, LOGWARNING, log
from resources.lib import common
from resources.lib.handler.requestHandler import cRequestHandler
from urllib.parse import urlparse

LOGMESSAGE = cConfig().getLocalizedString(30166)
class cPluginHandler:
    def __init__(self):
        self.addon = common.addon
        self.rootFolder = common.addonPath
        self.settingsFile = os.path.join(self.rootFolder, 'resources', 'settings.xml')
        self.profilePath = common.profilePath
        self.pluginDBFile = os.path.join(self.profilePath, 'pluginDB')

        log(LOGMESSAGE + ' -> [pluginHandler]: profile folder: %s' % self.profilePath, LOGNOTICE)
        log(LOGMESSAGE + ' -> [pluginHandler]: root folder: %s' % self.rootFolder, LOGNOTICE)
        self.defaultFolder = os.path.join(self.rootFolder, 'sites')
        log(LOGMESSAGE + ' -> [pluginHandler]: default sites folder: %s' % self.defaultFolder, LOGNOTICE)

    def getAvailablePlugins(self):
        pluginDB = self.__getPluginDB()
        # default plugins
        update = False
        fileNames = self.__getFileNamesFromFolder(self.defaultFolder)
        for fileName in fileNames:
            plugin = {'name': '', 'identifier': '', 'icon': '', 'domain': '', 'globalsearch': '', 'modified': 0}
            if fileName in pluginDB:
                plugin.update(pluginDB[fileName])
            try:
                modTime = os.path.getmtime(os.path.join(self.defaultFolder, fileName + '.py'))
            except OSError:
                modTime = 0
            try:
                globalSearchStatus = cConfig().getSetting('global_search_' + fileName)
            except Exception:
                pass
            if fileName not in pluginDB or modTime > plugin['modified'] or globalSearchStatus:
                log(LOGMESSAGE + ' -> [pluginHandler]: load plugin Informations for ' + str(fileName), LOGNOTICE)
                # try to import plugin
                pluginData = self.__getPluginData(fileName, self.defaultFolder)
                if pluginData:
                    pluginData['globalsearch'] = globalSearchStatus
                    pluginData['modified'] = modTime # Wenn Datei (Zeitstempel) verändert wurde aktualisiere Daten
                    pluginDB[fileName] = pluginData
                    update = True
        # check pluginDB for obsolete entries
        deletions = []
        for pluginID in pluginDB:
            if pluginID not in fileNames:
                deletions.append(pluginID)
        for id in deletions:
            del pluginDB[id]
        if update or deletions:
            self.__updatePluginDB(pluginDB) # Aktualisiert PluginDB in Addon_data
            log(LOGMESSAGE + ' -> [pluginHandler]: PluginDB informations updated.', LOGNOTICE)
        return self.getAvailablePluginsFromDB()

    def getAvailablePluginsFromDB(self):
        plugins = []
        iconFolder = os.path.join(self.rootFolder, 'resources', 'art', 'sites')
        pluginDB = self.__getPluginDB() # Erstelle PluginDB
        # PluginID = Siteplugin Name
        for pluginID in pluginDB:
            plugin = pluginDB[pluginID] # Aus PluginDB lese PluginID
            pluginSettingsName = 'plugin_%s' % pluginID # Name des Siteplugins
            plugin['id'] = pluginID
            if 'icon' in plugin:
                plugin['icon'] = os.path.join(iconFolder, plugin['icon'])
            else:
                plugin['icon'] = ''
            # existieren zu diesem plugin die an/aus settings
            if cConfig().getSetting(pluginSettingsName) == 'true': # Lese aus settings.xml welche Plugins eingeschaltet sind
                plugins.append(plugin)
        return plugins

    def __updatePluginDB(self, data): # Aktualisiere PluginDB
        if not os.path.exists(self.profilePath):
            os.makedirs(self.profilePath)
        file = open(self.pluginDBFile, 'w')
        json.dump(data, file)
        file.close()

    def __getPluginDB(self): # Erstelle PluginDB
        if not os.path.exists(self.pluginDBFile): # Wenn Datei nicht verfügbar dann erstellen
            return dict()
        file = open(self.pluginDBFile, 'r')
        try:
            data = json.load(file)
        except ValueError:
            log(LOGMESSAGE + ' -> [pluginHandler]: pluginDB seems corrupt, creating new one', LOGERROR)
            data = dict()
        file.close()
        return data


    def __getFileNamesFromFolder(self, sFolder): # Hole Namen vom Dateiname.py
        aNameList = []
        items = os.listdir(sFolder)
        for sItemName in items:
            if sItemName.endswith('.py'):
                sItemName = os.path.basename(sItemName[:-3])
                aNameList.append(sItemName)
        return aNameList

    def __getPluginData(self, fileName, defaultFolder): # Hole Plugin Daten aus dem Siteplugin
        pluginData = {}
        if not defaultFolder in sys.path: sys.path.append(defaultFolder)
        try:
            plugin = __import__(fileName, globals(), locals())
            pluginData['name'] = plugin.SITE_NAME
        except Exception as e:
            log(LOGMESSAGE + " -> [pluginHandler]: Can't import plugin: %s" % fileName, LOGERROR)
            return False
        try:
            pluginData['identifier'] = plugin.SITE_IDENTIFIER
        except Exception:
            pass
        try:
            pluginData['icon'] = plugin.SITE_ICON
        except Exception:
            pass
        try:
            pluginData['domain'] = plugin.DOMAIN
        except Exception:
            pass
        try:
            pluginData['globalsearch'] = plugin.SITE_GLOBAL_SEARCH
        except Exception:
            pluginData['globalsearch'] = True
            pass
        return pluginData


    def __getPluginDataDomain(self, fileName, defaultFolder): # Hole Plugin Daten für Domains
        pluginDataDomain = {}
        if not defaultFolder in sys.path: sys.path.append(defaultFolder)
        try:
            plugin = __import__(fileName, globals(), locals())
            pluginDataDomain['identifier'] = plugin.SITE_IDENTIFIER
        except Exception as e:
            log(LOGMESSAGE + " -> [pluginHandler]: Can't import plugin: %s" % fileName, LOGERROR)
            return False
        try:
            pluginDataDomain['domain'] = plugin.DOMAIN
        except Exception:
            pass
        return pluginDataDomain

    # Überprüfung des Domain Namens. Leite um und hole neue URL und schreibe in die settings.xml. Bei nicht erreichen der Seite deaktiviere Globale Suche bis zum nächsten Start und überprüfe erneut.
    def checkDomain(self):
        log(LOGMESSAGE + ' -> [checkDomain]: Query status code of the provider', LOGNOTICE)
        fileNames = self.__getFileNamesFromFolder(self.defaultFolder)
        for fileName in fileNames:
            try:
                pluginDataDomain = self.__getPluginDataDomain(fileName, self.defaultFolder)
                provider = pluginDataDomain['identifier']
                _domain = pluginDataDomain['domain']
                domain = cConfig().getSetting('plugin_' + provider + '.domain', _domain)
                base_link = 'http://' + domain + '/'  # URL_MAIN
                if domain == 'site-maps.cc':  # Falsche Umleitung ausschliessen
                    xbmcaddon.Addon().setSetting('plugin_' + provider + '.domain', '')  # Falls doch dann lösche Settings Eintrag
                    continue
                try:
                    if xbmcaddon.Addon().getSetting('plugin_' + provider) == 'false':  # Wenn SitePlugin deaktiviert
                        cConfig().setSetting('global_search_' + provider, 'false')  # setzte Globale Suche auf aus
                        cConfig().setSetting('plugin_' + provider + '_checkdomain', 'false')  # setzte Domain Check auf aus
                        xbmcaddon.Addon().setSetting('plugin_' + provider + '.domain', '')  # lösche Settings Eintrag

                    if xbmcaddon.Addon().getSetting('plugin_' + provider + '_checkdomain') == 'true':  # aut. Domainüberprüfung an ist überprüfe Status der Sitplugins
                        oRequest = cRequestHandler(base_link, caching=False, ignoreErrors=True)
                        oRequest.request()
                        status_code = int(oRequest.getStatus())
                        log(LOGMESSAGE + ' -> [checkDomain]: Status Code ' + str(status_code) + '  ' + provider + ': - ' + base_link, LOGNOTICE)
                        if 403 <= status_code <= 503:  # Domain Interner Server Error und nicht erreichbar
                            cConfig().setSetting('global_search_' + provider, 'false')  # deaktiviere Globale Suche
                            log(LOGMESSAGE + ' -> [checkDomain]: Internal Server Error (DDOS Guard, HTTP Error, Cloudflare or BlazingFast active)', LOGNOTICE)
                        elif 300 <= status_code <= 400:  # Domain erreichbar mit Umleitung
                            url = oRequest.getRealUrl()
                            # cConfig().setSetting('plugin_'+ provider +'.base_link', url)
                            cConfig().setSetting('plugin_' + provider + '.domain', urlparse(url).hostname)  # setze Domain in die settings.xml
                            cConfig().setSetting('global_search_' + provider, 'true')  # aktiviere Globale Suche
                            log(LOGMESSAGE + ' -> [checkDomain]: globalSearch for ' + provider + ' is activated.', LOGNOTICE)

                        elif status_code == 200:  # Domain erreichbar
                            # cConfig().setSetting('plugin_' + provider + '.base_link', base_link)
                            cConfig().setSetting('plugin_' + provider + '.domain', urlparse(base_link).hostname)  # setze URL_MAIN in die settings.xml
                            cConfig().setSetting('global_search_' + provider, 'true')  # aktiviere Globale Suche
                            log(LOGMESSAGE + ' -> [checkDomain]: globalSearch for ' + provider + ' is activated.', LOGNOTICE)

                        else:
                            log(LOGMESSAGE + ' -> [checkDomain]: Error ' + provider + ' not available.', LOGNOTICE)
                            cConfig().setSetting('global_search_' + provider, 'false')  # deaktiviere Globale Suche
                            xbmcaddon.Addon().setSetting('plugin_' + provider + '.domain', '')  # lösche Settings Eintrag
                            log(LOGMESSAGE + ' -> [checkDomain]: globalSearch for ' + provider + ' is deactivated.', LOGNOTICE)
                except:
                    cConfig().setSetting('global_search_' + provider, 'false')  # deaktiviere Globale Suche
                    xbmcaddon.Addon().setSetting('plugin_' + provider + '.domain', '')  # lösche Settings Eintrag
                    log(LOGMESSAGE + ' -> [checkDomain]: Error ' + provider + ' not available.', LOGNOTICE)
                    pass
            except Exception:
                pass
        log(LOGMESSAGE + ' -> [checkDomain]: Domains for all available Plugins updated', LOGNOTICE)