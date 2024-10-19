# -*- coding: utf-8 -*-
# Python 3

import xbmc
import xbmcgui
import xbmcaddon
import hashlib
import re
import platform
import os
import sys

from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib import common
from resources.lib import pyaes
from resources.lib.config import cConfig
from xbmcaddon import Addon
from xbmcgui import Dialog
from xbmcvfs import translatePath
from urllib.parse import quote, unquote, quote_plus, unquote_plus, urlparse
from html.entities import name2codepoint


# Aufgeführte Plattformen zum Anzeigen der Systemplattform
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'Android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'Linux'
    elif xbmc.getCondVisibility('system.platform.linux.Raspberrypi'):
        return 'Linux/RPi'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'Windows'
    elif xbmc.getCondVisibility('system.platform.uwp'):
        return 'Windows UWP'      
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'OSX'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'ATV2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'iOS'
    elif xbmc.getCondVisibility('system.platform.darwin'):
        return 'iOS'
    elif xbmc.getCondVisibility('system.platform.xbox'):
        return 'XBOX'
    elif xbmc.getCondVisibility('System.HasAddon(service.coreelec.settings)'):
        return "CoreElec"
    elif xbmc.getCondVisibility('System.HasAddon(service.libreelec.settings)'):
        return "LibreElec"
    elif xbmc.getCondVisibility('System.HasAddon(service.osmc.settings)'):
        return "OSMC"        


class cPluginInfo:

    def __init__(self):
        self.addon = common.addon
        self.rootFolder = common.addonPath
        self.settingsFile = os.path.join(self.rootFolder, 'resources', 'settings.xml')
        self.profilePath = common.profilePath
        self.pluginDBFile = os.path.join(self.profilePath, 'pluginDB')
        self.defaultFolder = os.path.join(self.rootFolder, 'sites')


    def __getFileNamesFromFolder(self, sFolder):  # Hole Namen vom Dateiname.py
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
            return False
        try:
            pluginData['identifier'] = plugin.SITE_IDENTIFIER
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


# Plugin Support Informationen
    def pluginInfo(self):
        BUILD = (xbmc.getInfoLabel('System.BuildVersion')[:4])
        BUILDCODE = xbmc.getInfoLabel('System.BuildVersionCode')
        SYS_FORM = cConfig().getLocalizedString(30266)
        PLUGIN_NAME = Addon().getAddonInfo('name')
        PLUGIN_ID = Addon().getAddonInfo('id')
        PLUGIN_VERSION = Addon().getAddonInfo('version')
        RESOLVER_NAME = Addon('script.module.resolveurl').getAddonInfo('name')
        RESOLVER_ID = Addon('script.module.resolveurl').getAddonInfo('id')
        RESOLVER_VERSION = Addon('script.module.resolveurl').getAddonInfo('version')
        PLATFORM = '   {0}'.format(platform().title())

        # Support Informationen anzeigen
        Dialog().textviewer(cConfig().getLocalizedString(30265),
                            '[B]Geräte - Informationen:[/B]\n'
                            + 'Kodi Version:  ' + BUILD + ' (Code Version: ' + BUILDCODE + ') ' + '\n'
                            + SYS_FORM + PLATFORM + '\n'
                            + '\n'
                            + '[B]Plugin - Informationen:[/B]\n'
                            + PLUGIN_NAME + ' Version:  ' + PLUGIN_ID + ' - ' + PLUGIN_VERSION + '\n'
                            + RESOLVER_NAME + ' Version:  ' + RESOLVER_ID + ' - ' + RESOLVER_VERSION + '\n'
                            
                            )


# zeigt nach Update den Changelog als Popup an
def changelog():
    CHANGELOG_PATH = translatePath(os.path.join('special://home/addons/plugin.video.matrixv2/', 'changelog.txt'))
    version = xbmcaddon.Addon().getAddonInfo('version')
    if xbmcaddon.Addon().getSetting('changelog_version') == version or not os.path.isfile(CHANGELOG_PATH):
        return
    xbmcaddon.Addon().setSetting('changelog_version', version)
    heading = cConfig().getLocalizedString(30275)
    with open(CHANGELOG_PATH, mode="r", encoding="utf-8") as f:
        cl_lines = f.readlines()
    announce = ''
    for line in cl_lines:
        announce += line
    textBox(heading, announce)


# Erstellt eine Textbox
def textBox(heading, announce):
    class TextBox():

        def __init__(self, *args, **kwargs):
            self.WINDOW = 10147
            self.CONTROL_LABEL = 1
            self.CONTROL_TEXTBOX = 5
            xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, ))
            self.win = xbmcgui.Window(self.WINDOW)
            xbmc.sleep(500)
            self.setControls()

        def setControls(self):
            self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
            try:
                f = open(announce)
                text = f.read()
            except:
                text = announce
            self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
            return

    TextBox()
    while xbmc.getCondVisibility('Window.IsVisible(10147)'):
        xbmc.sleep(500)


class cParser:
    @staticmethod
    def parseSingleResult(sHtmlContent, pattern):
        aMatches = None
        if sHtmlContent:
            aMatches = re.compile(pattern).findall(sHtmlContent)
            if len(aMatches) == 1:
                aMatches[0] = cParser.replaceSpecialCharacters(aMatches[0])
                return True, aMatches[0]
        return False, aMatches

    @staticmethod
    def replaceSpecialCharacters(s):
        # Umlaute Unicode konvertieren
        for t in (('\\/', '/'), ('&amp;', '&'), ('\\u00c4', 'Ä'), ('\\u00e4', 'ä'),
            ('\\u00d6', 'Ö'), ('\\u00f6', 'ö'), ('\\u00dc', 'Ü'), ('\\u00fc', 'ü'),
            ('\\u00df', 'ß'), ('\\u2013', '-'), ('\\u00b2', '²'), ('\\u00b3', '³'),
            ('\\u00e9', 'é'), ('\\u2018', '‘'), ('\\u201e', '„'), ('\\u201c', '“'),
            ('\\u00c9', 'É'), ('\\u2026', '...'), ('\\u202fh', 'h'), ('\\u2019', '’'),
            ('\\u0308', '̈'), ('\\u00e8', 'è'), ('#038;', ''), ('\\u00f8', 'ø'),
            ('／', '/'), ('\\u00e1', 'á'), ('&#8211;', '-'), ('&#8220;', '“'), ('&#8222;', '„'),
            ('&#8217;', '’'), ('&#8230;', '…'), ('\\u00bc', '¼'), ('\\u00bd', '½'), ('\\u00be', '¾'),
            ('\\u2153', '⅓'), ('\\u002A', '*')):
            try:
                s = s.replace(*t)
            except:
                pass
        # Umlaute HTML konvertieren
        for h in (('\\/', '/'), ('&#x26;', '&'), ('&#039;', "'"), ("&#39;", "'"),
            ('&#xC4;', 'Ä'), ('&#xE4;', 'ä'), ('&#xD6;', 'Ö'), ('&#xF6;', 'ö'),
            ('&#xDC;', 'Ü'), ('&#xFC;', 'ü'), ('&#xDF;', 'ß') , ('&#xB2;', '²'),
            ('&#xDC;', '³'), ('&#xBC;', '¼'), ('&#xBD;', '½'), ('&#xBE;', '¾'),
            ('&#8531;', '⅓'), ('&#8727;', '*')):
            try:
                s = s.replace(*h)
            except:
                pass
        try:
            re.sub(u'é', 'é', s)
            re.sub(u'É', 'É', s)
            # kill all other unicode chars
            r = re.compile(r'[^\W\d_]', re.U)
            r.sub('', s)
        except:
            pass
        return s

    @staticmethod
    def parse(sHtmlContent, pattern, iMinFoundValue=1, ignoreCase=False):
        aMatches = None
        if sHtmlContent:
            sHtmlContent = cParser.replaceSpecialCharacters(sHtmlContent)
            if ignoreCase:
                aMatches = re.compile(pattern, re.DOTALL | re.I).findall(sHtmlContent)
            else:
                aMatches = re.compile(pattern, re.DOTALL).findall(sHtmlContent)
            if len(aMatches) >= iMinFoundValue:
                return True, aMatches
        return False, aMatches

    @staticmethod
    def replace(pattern, sReplaceString, sValue):
        return re.sub(pattern, sReplaceString, sValue)

    @staticmethod
    def search(sSearch, sValue):
        return re.search(sSearch, sValue, re.IGNORECASE)

    @staticmethod
    def escape(sValue):
        return re.escape(sValue)

    @staticmethod
    def getNumberFromString(sValue):
        pattern = '\\d+'
        aMatches = re.findall(pattern, sValue)
        if len(aMatches) > 0:
            return int(aMatches[0])
        return 0

    @staticmethod
    def urlparse(sUrl):
        return urlparse(sUrl.replace('www.', '')).netloc.title()

    @staticmethod
    def urlDecode(sUrl):
        return unquote(sUrl)

    @staticmethod
    def urlEncode(sUrl, safe=''):
        return quote(sUrl, safe)

    @staticmethod
    def quote(sUrl):
        return quote(sUrl)

    @staticmethod
    def unquotePlus(sUrl):
        return unquote_plus(sUrl)

    @staticmethod
    def quotePlus(sUrl):
        return quote_plus(sUrl)

    @staticmethod
    def B64decode(text):
        import base64
        b = base64.b64decode(text).decode('utf-8')
        return b
    
    @staticmethod
    def abParse(sHtmlContent, start, end=None, startoffset=0):
        # usage oParser.abParse(sHtmlContent, 'start', 'end')
        # startoffset (int) décale le début pour ne pas prendre en compte start dans le résultat final si besoin
        # la fin est recherchée forcement après le début
        # la recherche de fin n'est pas obligatoire
        # usage2 oParser.abParse(sHtmlContent, 'start', 'end', 6)
        # ex youtube.py

        startIdx = sHtmlContent.find(start)
        if startIdx == -1:  # rien trouvé, on prend depuis le début
            startIdx = 0

        if end:
            endIdx = sHtmlContent[startoffset + startIdx + len(start):].find(end)
            if endIdx > 0:
                return sHtmlContent[startoffset + startIdx: startoffset + startIdx + endIdx + len(start)]
        return sHtmlContent[startoffset + startIdx:]
    

class logger:
    @staticmethod
    def info(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGINFO)

    @staticmethod
    def debug(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGDEBUG)

    @staticmethod
    def warning(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGWARNING)

    @staticmethod
    def error(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGERROR)

    @staticmethod
    def fatal(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGFATAL)

    @staticmethod
    def __writeLog(sLog, cLogLevel=xbmc.LOGDEBUG):
        params = ParameterHandler()
        try:
            if params.exist('site'):
                site = params.getValue('site')
                sLog = "[%s] -> [%s]: %s" % (common.addonName, site, sLog)
            else:
                sLog = "[%s] %s" % (common.addonName, sLog)
            xbmc.log(sLog, cLogLevel)
        except Exception as e:
            xbmc.log('Logging Failure: %s' % e, cLogLevel)
            pass


class cUtil:
    @staticmethod
    def removeHtmlTags(sValue, sReplace=''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)

    @staticmethod
    def unescape(text): #Todo hier werden Fehler angezeigt
        def fixup(m):
            text = m.group(0)
            if not text.endswith(';'): text += ';'
            if text[:2] == '&#':
                try:
                    if text[:3] == '&#x':
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                try:
                    text = unichr(name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text

        if isinstance(text, str):
            try:
                text = text.decode('utf-8')
            except Exception:
                try:
                    text = text.decode('utf-8', 'ignore')
                except Exception:
                    pass
        return re.sub("&(\\w+;|#x?\\d+;?)", fixup, text.strip())

    @staticmethod
    def cleanse_text(text):
        if text is None: text = ''
        text = cUtil.removeHtmlTags(text)
        return text

    @staticmethod
    def evp_decode(cipher_text, passphrase, salt=None):
        if not salt:
            salt = cipher_text[8:16]
            cipher_text = cipher_text[16:]
        key, iv = cUtil.evpKDF(passphrase, salt)
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
        plain_text = decrypter.feed(cipher_text)
        plain_text += decrypter.feed()
        return plain_text.decode("utf-8")

    @staticmethod
    def evpKDF(pwd, salt, key_size=32, iv_size=16):
        temp = b''
        fd = temp
        while len(fd) < key_size + iv_size:
            h = hashlib.md5()
            h.update(temp + pwd + salt)
            temp = h.digest()
            fd += temp
        key = fd[0:key_size]
        iv = fd[key_size:key_size + iv_size]
        return key, iv

def valid_email(email):
    # Email Muster
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Überprüfen der EMail-Adresse mit dem Muster
    if re.match(pattern, email):
        return True
    else:
        return False

