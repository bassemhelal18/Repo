

import xbmcaddon
import xbmcvfs
import xbmcgui
import os
from resolveurl import common

from resources.lib.comaddon import VSlog


class cInputWindow(xbmcgui.WindowDialog):

    chkbutton = []

    def __init__(self, *args, **kwargs):
        

        DimTab = kwargs.get('dimtab')
        self.DimTabTotal = DimTab[0] * DimTab[1]

        bg_image = os.path.join(common.addon_path, 'resources', 'images', 'DialogBack2.png')
        check_image = os.path.join(common.addon_path, 'resources', 'images', 'checked.png')
        button_fo = os.path.join(common.kodi.get_path(), 'resources', 'skins', 'Default', 'media', 'button-fo.png')
        button_nofo = os.path.join(common.kodi.get_path(), 'resources', 'skins', 'Default', 'media', 'button-nofo.png')
        
        
        
        

        self.ctrlBackground = xbmcgui.ControlImage(250, 110, 780, 499, bg_image)
        self.cancelled = False
        self.addControl(self.ctrlBackground)
        
        self.msg = '[COLOR red]%s[/COLOR]' % (kwargs.get('msg'))

        self.strActionInfo = xbmcgui.ControlLabel(250, 20, 724, 400, self.msg, 'font13')
        self.addControl(self.strActionInfo)

        self.img = xbmcgui.ControlImage(250, 110, 780, 499,  kwargs.get('captcha'))
        self.addControl(self.img)

        self.chk = [0] * self.DimTabTotal
        self.chkbutton = [0] * self.DimTabTotal
        self.chkstate = [False] * self.DimTabTotal

        c = 0
        cx = int((780) / DimTab[0])  # 260
        cy = int((499) / DimTab[1])  # 166

        ox = 250  # 250
        oy = 110  # 110

        for y in range(DimTab[1]):
            for x in range(DimTab[0]):

                self.chk[c] = xbmcgui.ControlImage(ox + cx * x, oy + cy * y, cx, cy, check_image)
                self.chkbutton[c] = xbmcgui.ControlButton(ox + cx * x, oy + cy * y, cx, cy, str(c + 1), font='font1', focusTexture=button_fo, noFocusTexture=button_nofo)
                c += 1

        for obj in self.chk:
            self.addControl(obj)
            obj.setVisible(False)
        for obj in self.chkbutton:
            self.addControl(obj)

        self.cancelbutton = xbmcgui.ControlButton(250 + 260 - 70, 620, 140, 50, common.i18n('cancel'), focusTexture=button_fo, noFocusTexture=button_nofo, alignment=2)
        self.okbutton = xbmcgui.ControlButton(250 + 520 - 50, 620, 100, 50, common.i18n('ok'), focusTexture=button_fo, noFocusTexture=button_nofo, alignment=2)
        self.addControl(self.okbutton)
        self.addControl(self.cancelbutton)

        for c in range(self.DimTabTotal):
            self.chkbutton[c].controlDown(self.getbutton(c, "down", DimTab[0], DimTab[1]))
            self.chkbutton[c].controlUp(self.getbutton(c, "up", DimTab[0], DimTab[1]))
            self.chkbutton[c].controlLeft(self.getbutton(c, "left", DimTab[0], DimTab[1]))
            self.chkbutton[c].controlRight(self.getbutton(c, "right", DimTab[0], DimTab[1]))

        self.cancelled = False
        self.setFocus(self.okbutton)
        self.okbutton.controlLeft(self.cancelbutton)
        self.okbutton.controlRight(self.cancelbutton)
        self.cancelbutton.controlLeft(self.okbutton)
        self.cancelbutton.controlRight(self.okbutton)
        self.okbutton.controlDown(self.chkbutton[2])
        self.okbutton.controlUp(self.chkbutton[8])
        self.cancelbutton.controlDown(self.chkbutton[0])
        self.cancelbutton.controlUp(self.chkbutton[6])

    def getbutton(self, actuel, sens, dx, dy):

        if sens == "up":
            if actuel < dx:
                return self.okbutton
            else:
                return self.chkbutton[actuel - dx]

        if sens == "down":
            if actuel >= dx * (dy - 1):
                return self.okbutton
            else:
                return self.chkbutton[actuel + dx]

        if sens == "right":
            if actuel >= dx * dy - 1:
                return self.okbutton
            else:
                return self.chkbutton[actuel + 1]

        if sens == "left":
            if actuel == 0:
                return self.okbutton
            else:
                return self.chkbutton[actuel - 1]

    def get(self):
        self.doModal()
        self.close()
        if not self.cancelled:
            retval = []
            for objn in range(self.DimTabTotal):
                if self.chkstate[objn]:
                    retval.append(int(objn))
            return retval

        else:
            return False

    def anythingChecked(self):
        for obj in self.chkstate:
            if obj:
                return True
        return False

    def onControl(self, control):
        if str(control.getLabel()) == "OK":
            if self.anythingChecked():
                self.close()
        elif str(control.getLabel()) == "Cancel":
            self.cancelled = True
            self.close()
        try:
            if 'xbmcgui.ControlButton' in repr(type(control)):
                index = control.getLabel()
                if index.isnumeric():
                    self.chkstate[int(index)-1] = not self.chkstate[int(index)-1]
                    self.chk[int(index)-1].setVisible(self.chkstate[int(index)-1])

        except:
            pass

    def onAction(self, action):
        if action == 10:
            self.cancelled = True
            self.close()


class cInputWindowYesNo(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        

        imgX, imgY, imgw, imgh = 436, 210, 408, 300
        ph, pw = imgh / 3, imgw / 3
        x_gap = 70
        y_gap = 70
        button_gap = 40
        button_h = 40
        button_y = imgY + imgh + button_gap
        middle = imgX + (imgw / 2)
        win_x = imgX - x_gap
        win_y = imgY - y_gap
        win_h = imgh + 2 * y_gap + button_h + button_gap
        win_w = imgw + 2 * x_gap

        bg_image = os.path.join(common.addon_path, 'resources', 'images', 'DialogBack2.png')
        button_fo = os.path.join(common.kodi.get_path(), 'resources', 'skins', 'Default', 'media', 'button-fo.png')
        button_nofo = os.path.join(common.kodi.get_path(), 'resources', 'skins', 'Default', 'media', 'button-nofo.png')

        self.ctrlBackground = xbmcgui.ControlImage(win_x, win_y, win_w, win_h, bg_image)
        self.cancelled = False
        self.addControl(self.ctrlBackground)
        
        self.msg = '[COLOR red]%s[/COLOR]' % (kwargs.get('msg'))
        self.strActionInfo = xbmcgui.ControlLabel(250, 20, 724, 400, self.msg, 'font13')
        self.addControl(self.strActionInfo)

        self.img = xbmcgui.ControlImage(500, 250, 280, 280, kwargs.get('captcha') )
        self.addControl(self.img)

        self.Yesbutton = xbmcgui.ControlButton(250 + 520 - 50, 620, 100, 50, common.i18n('Yes'), focusTexture=button_fo, noFocusTexture=button_nofo, alignment=2)
        self.Nobutton = xbmcgui.ControlButton(250 + 260 - 70, 620, 140, 50,  common.i18n('No'), focusTexture=button_fo, noFocusTexture=button_nofo, alignment=2)
        self.addControl(self.Yesbutton)
        self.addControl(self.Nobutton)
        self.setFocus(self.Yesbutton)
        self.Yesbutton.controlLeft(self.Nobutton)
        self.Nobutton.controlRight(self.Yesbutton)

    def get(self):
        self.doModal()
        self.close()
        retval = self.chkstate
        return retval

    def anythingChecked(self):
        for obj in self.chkstate:
            if obj:
                return True
        return False

    def onControl(self, control):
        try:
            index = control.getLabel()
            if "Yes" in index:
                self.chkstate = "Y"
                self.chk = "Y"
            else:
                self.chkstate = "N"
                self.chk = "N"
        except:
            pass

        if str(control.getLabel()) == "Yes":
            self.close()
        elif str(control.getLabel()) == "No":
            self.close()