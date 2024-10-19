# -*- coding: utf-8 -*-
# Python 3

import os
import json
import re
import xbmc
import xbmcaddon
import xbmcgui
import time

from xbmcaddon import Addon
from xbmcgui import Dialog
from resources.lib.config import cConfig
from resources.lib import tools
from xbmc import LOGINFO as LOGNOTICE, LOGERROR, LOGWARNING, LOGDEBUG, log, getInfoLabel
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib import updateManager
from xbmcvfs import translatePath

HEADERMESSAGE = cConfig().getLocalizedString(30151)
LOGMESSAGE = cConfig().getLocalizedString(30166)


AddonName = xbmcaddon.Addon().getAddonInfo('name')

# Pfad der update.sha
NIGHTLY_UPDATE = os.path.join(translatePath(Addon().getAddonInfo('profile')), "update_sha")


ADDON_PATH = translatePath(os.path.join('special://home/addons/', '%s'))


# Update Info beim Kodi Start
def infoDialog(message, heading=AddonName, icon='', time=5000, sound=False):
    if icon == '': icon = xbmcaddon.Addon().getAddonInfo('icon')
    elif icon == 'INFO': icon = xbmcgui.NOTIFICATION_INFO
    elif icon == 'WARNING': icon = xbmcgui.NOTIFICATION_WARNING
    elif icon == 'ERROR': icon = xbmcgui.NOTIFICATION_ERROR
    xbmcgui.Dialog().notification(heading, message, icon, time, sound=sound)



def enableAddon(ADDONID):
    struktur = json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","id":1,"params": {"addonid":"%s", "properties": ["enabled"]}}' % ADDONID))
    if 'error' in struktur or struktur["result"]["addon"]["enabled"] != True:
        count = 0
        while True:
            if count == 5: break
            count += 1
            xbmc.executebuiltin('EnableAddon(%s)' % (ADDONID))
            xbmc.executebuiltin('SendClick(11)')
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s", "enabled":true}}' % ADDONID)
            xbmc.sleep(500)
            try:
                struktur = json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","id":1,"params": {"addonid":"%s", "properties": ["enabled"]}}' % ADDONID))
                if struktur["result"]["addon"]["enabled"] == True: break
            except:
                pass



def checkDependence(ADDONID):
    isdebug = True
    if isdebug:
        log(__name__ + ' - %s - checkDependence ' % ADDONID, LOGDEBUG)
    try:
        addon_xml = os.path.join(ADDON_PATH % ADDONID, 'addon.xml')
        with open(addon_xml, 'rb') as f:
            xml = f.read()
        pattern = '(import.*?addon[^/]+)'
        allDependence = re.findall(pattern, str(xml))
        for i in allDependence:
            try:
                if 'optional' in i or 'xbmc.python' in i: continue
                pattern = 'import.*?"([^"]+)'
                IDdoADDON = re.search(pattern, i).group(1)
                if os.path.exists(ADDON_PATH % IDdoADDON) == True and xbmcaddon.Addon().getSetting('enforceUpdate') != 'true':
                    enableAddon(IDdoADDON)
                else:
                    xbmc.executebuiltin('InstallAddon(%s)' % (IDdoADDON))
                    xbmc.executebuiltin('SendClick(11)')
                    enableAddon(IDdoADDON)
            except:
                pass
    except Exception as e:
        log(__name__ + ' %s - Exception ' % e, LOGERROR)


# Auslesen der installierten Kodi Version und setze danach den Release Branch in den settings

xbmcaddon.Addon().setSetting('matrixv2.branch.release', 'main')




if os.path.isfile(NIGHTLY_UPDATE) == False or Addon().getSetting('githubUpdateMatrixv2') == 'true'  or Addon().getSetting('enforceUpdate') == 'true':
    status1 = updateManager.Matrixv2Update(True)
    cRequestHandler('').clearCache()  # Cache löschen
    if Addon().getSetting('update.notification') == 'full': 
        infoDialog(cConfig().getLocalizedString(30112), sound=False, icon='INFO', time=10000)   
        if status1 == True: infoDialog(cConfig().getLocalizedString(30113), sound=False, icon='INFO', time=6000)
        if status1 == False: infoDialog(cConfig().getLocalizedString(30114), sound=True, icon='ERROR')
        if status1 == None: infoDialog(cConfig().getLocalizedString(30115), sound=False, icon='INFO', time=6000)
        if xbmcaddon.Addon().getSetting('enforceUpdate') == 'true': xbmcaddon.Addon().setSetting('enforceUpdate', 'false')
    else:
        if status1 == True: infoDialog(cConfig().getLocalizedString(30113), sound=False, icon='INFO', time=6000)
        if status1 == False: infoDialog(cConfig().getLocalizedString(30114), sound=True, icon='ERROR')
        if xbmcaddon.Addon().getSetting('enforceUpdate') == 'true': xbmcaddon.Addon().setSetting('enforceUpdate', 'false')


# Starte Resolver Update wenn auf Github verfügbar    
if os.path.isfile(NIGHTLY_UPDATE) == False or Addon().getSetting('githubUpdateResolver') == 'true'  or Addon().getSetting('enforceUpdate') == 'true':
    status2 = updateManager.resolverUpdate(True)
    if Addon().getSetting('update.notification') == 'full': # Benachrichtung Resolver vollständig
        infoDialog(cConfig().getLocalizedString(30112), sound=False, icon='INFO', time=10000)   # Suche Updates
        if status2 == True: infoDialog('Resolver ' + xbmcaddon.Addon().getSetting('resolver.branch') + cConfig().getLocalizedString(30116), sound=False, icon='INFO', time=6000)
        if status2 == False: infoDialog(cConfig().getLocalizedString(30117), sound=True, icon='ERROR')
        if status2 == None: infoDialog(cConfig().getLocalizedString(30118), sound=False, icon='INFO', time=6000)
        if xbmcaddon.Addon().getSetting('enforceUpdate') == 'true': xbmcaddon.Addon().setSetting('enforceUpdate', 'false')
    else:
        if status2 == True: infoDialog('Resolver ' + xbmcaddon.Addon().getSetting('resolver.branch') + cConfig().getLocalizedString(30116), sound=False, icon='INFO', time=6000)
        if status2 == False: infoDialog(cConfig().getLocalizedString(30117), sound=True, icon='ERROR')
        if xbmcaddon.Addon().getSetting('enforceUpdate') == 'true': xbmcaddon.Addon().setSetting('enforceUpdate', 'false')


# Startet Überprüfung der Abhängigkeiten
checkDependence('plugin.video.matrixv2')


# Startet Domain Überprüfung und schreibt diese in die settings.xml
cPluginHandler().checkDomain()


# Wenn neue settings vorhanden oder geändert in addon_data dann starte Pluginhandler und aktualisiere die PluginDB um Daten von checkDomain mit aufzunehmen
try:
    if xbmcaddon.Addon().getSetting('newSetting') == 'true':
        cPluginHandler().getAvailablePlugins()
except Exception:
    pass


# Changelog Popup in den "settings.xml" ein bzw. aus schaltbar
if xbmcaddon.Addon().getSetting('popup.update.notification') == 'true': 
    tools.changelog()


# Html Cache beim KodiStart nach (X) Tage löschen
deltaDay = int(cConfig().getSetting('cacheDeltaDay', 2))
deltaTime = 60*60*24*deltaDay # Tage 
currentTime = int(time.time())
# alle x Tage
if currentTime >= int(cConfig().getSetting('lastdelhtml', 0)) + deltaTime:
    cRequestHandler('').clearCache() # Cache löschen
    cConfig().setSetting('lastdelhtml', str(currentTime))