#Coded By SODO
from . import _
from Components.config import config
from Screens.Screen import Screen
import Screens.InfoBar
from Screens.MessageBox import MessageBox
from Screens.ChannelSelection import service_types_radio, service_types_tv, ChannelSelection, ChannelSelectionBase
from Tools.BoundFunction import boundFunction
import Components.ParentalControl
from enigma import eServiceReference, eServiceCenter, eTimer, iServiceInformation
from camcontrol import CamControl
OFF = 0
EDIT_BOUQUET = 1
EDIT_ALTERNATIVES = 2

def getProviderName(ref):
    typestr = ref.getData(0) in (2, 10) and service_types_radio or service_types_tv
    pos = typestr.rfind(':')
    rootstr = '%s (channelID == %08x%04x%04x) && %s FROM PROVIDERS ORDER BY name' % (typestr[:pos + 1],
     ref.getUnsignedData(4),
     ref.getUnsignedData(2),
     ref.getUnsignedData(3),
     typestr[pos + 1:])
    provider_root = eServiceReference(rootstr)
    serviceHandler = eServiceCenter.getInstance()
    providerlist = serviceHandler.list(provider_root)
    if providerlist is not None:
        while True:
            provider = providerlist.getNext()
            if not provider.valid():
                break
            if provider.flags & eServiceReference.isDirectory:
                servicelist = serviceHandler.list(provider)
                if servicelist is not None:
                    while True:
                        service = servicelist.getNext()
                        if not service.valid():
                            break
                        if service == ref:
                            info = serviceHandler.info(provider)
                            return info and info.getName(provider) or 'Unknown'

    return ''


def getAutoCamForService(service, provname = None):
    refstring = service.toString()
    if not provname:
        provname = getProviderName(service)
    for cam, list in autoCamList.items():
        if refstring in list or provname and provname in list:
            return cam


class AutoCamList(dict):

    def __init__(self):
        dict.__init__(self)
        self.camCtrl = CamControl('softcam')
        self.load()

    def loadFrom(self, filename):
        try:
            cfg = open(filename, 'r')
        except:
            return {}

        camname = 'default'
        from re import compile
        re_section = compile('\\[(?P<camname>[^]]+)\\]')
        while True:
            line = cfg.readline()
            if not line:
                break
            if line[0] in '#;\n':
                continue
            mo = re_section.match(line)
            if mo:
                camname = mo.group('camname')
                if camname not in self:
                    self[camname] = []
            else:
                self[camname].append(line.strip())

        cfg.close()
        return self

    def saveTo(self, filename):
        try:
            cfg = open(filename, 'w')
        except:
            return {}

        first = True
        for cam, val in self.items():
            if first:
                first = False
            else:
                cfg.write('\n')
            cfg.write('[%s]\n' % cam)
            for v in val:
                cfg.write('%s\n' % v)

        cfg.close()
        return self

    def load(self):
        self.loadFrom('/etc/autocam.conf')

    def save(self):
        self.saveTo('/etc/autocam.conf')

    def dict(self):
        return self

    def addCam(self, cam):
        if not self.has_key(cam):
            self[cam] = []

    def delCam(self, cam):
        if self.has_key(cam):
            del self[cam]

    def addService(self, cam, service):
        self.addCam(cam)
        if isinstance(service, str):
            service = [service]
        for s in service:
            if s not in self[cam]:
                self[cam].append(s)

    def delService(self, cam, service):
        if self.has_key(cam):
            if isinstance(service, str):
                service = [service]
            for s in service:
                if s in self[cam]:
                    self[cam].remove(s)

            if len(self[cam]) < 1:
                del self[cam]


autoCamList = AutoCamList()

class AutoCamListSetup(Screen):
    skin = '\n     <screen name="AutoCamListSetup" position="center,center" size="670,440" title="Auto-Camd List Setup" flags="wfBorder">\n          <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/egami-plugin.png" position="16,10" size="640,40" zPosition="1" transparent="1" alphatest="on" />\n          <ePixmap position="4,434" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/red.png" transparent="1" alphatest="on" />\n          <ePixmap position="176,434" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/green.png" transparent="1" alphatest="on" />\n          <ePixmap position="346,434" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/yellow.png" transparent="1" alphatest="on" />\n          <ePixmap position="514,434" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/blue.png" transparent="1" alphatest="on" />\n          <widget name="key_red" position="4,412" zPosition="1" size="150,25" font="Regular;18" halign="center" valign="top" transparent="1" />\n          <widget name="key_green" position="176,412" zPosition="1" size="150,25" font="Regular;18" halign="center" valign="top" transparent="1" />\n          <widget name="key_yellow" position="346,412" zPosition="1" size="150,25" font="Regular;18" halign="center" valign="top" transparent="1" />\n         <widget name="key_blue" position="510,412" zPosition="1" size="150,25" font="Regular;18" halign="center" valign="top" transparent="1" />          \n         <widget source="list" render="Listbox" position="4,54" size="660,340" scrollbarMode="showOnDemand" selectionPixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/select000.png">\n             <convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\t\tMultiContentEntryText(pos = (10, 5), size = (420, 25), font = 0, flags = RT_HALIGN_LEFT, text = 0),\n\t\t\t\t\t\tMultiContentEntryText(pos = (50, 30), size = (380, 20), font = 1, flags = RT_HALIGN_LEFT, text = 1),\n\t\t\t\t\t\tMultiContentEntryText(pos = (430, 13), size = (140, 24), font = 0, flags = RT_HALIGN_LEFT, text = 2),\n\t\t\t\t\t],\n\t\t\t\t "fonts": [gFont("Regular", 21), gFont("Regular", 16)],\n\t\t\t\t "itemHeight": 50\n\t\t\t\t}\n                      </convert>\n             </widget>\n       </screen>\n     '

    def __init__(self, session, camcontrol):
        Screen.__init__(self, session)
        self.camctrl = camcontrol
        self.ACL = autoCamList
        from Components.Sources.List import List
        self['list'] = List([])
        self.updateList()
        from Components.Label import Label
        self['key_red'] = Label(' ')
        self['key_green'] = Label(_('Add Provider'))
        self['key_yellow'] = Label(_('Add Channel'))
        self['key_blue'] = Label(' ')
        self.updateButtons()
        from Components.ActionMap import ActionMap
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': self.exit,
         'ok': self.keyOk,
         'red': self.keyRed,
         'green': self.keyGreen,
         'yellow': self.keyYellow,
         'blue': self.keyBlue}, -1)
        self.setTitle(_('Auto-Camd Setup'))
        self.onClose.append(self.__onClose)

    def __onClose(self):
        self.ACL.save()

    def keyRed(self):
        cur = self['list'].getCurrent()
        if cur:
            self.ACL.delService(cur[1], cur[3])
            self.updateList()
            self.updateButtons()

    def keyGreen(self):
        self.session.openWithCallback(self.addServiceCallback, AutoCamServiceSetup, True)

    def keyYellow(self):
        self.session.openWithCallback(self.addServiceCallback, AutoCamServiceSetup)

    def addServiceCallback(self, *ref):
        if ref:
            ref = ref[0]
            if ref.flags & 7 == 7:
                from ServiceReference import ServiceReference
                provname = ServiceReference(ref).getServiceName()
                self.ACL.addService(config.plugins.autoCamSetup.autocam.defcam.value, provname)
            else:
                self.ACL.addService(config.plugins.autoCamSetup.autocam.defcam.value, ref.toString())
            self.updateList()
            self.updateButtons()

    def keyBlue(self):
        cur = self['list'].getCurrent()
        if cur:
            sel, x = (0, -1)
            camlist = []
            for cam in self.camctrl.getList():
                x += 1
                camlist.append((cam,))
                if not sel and cam == cur[1]:
                    sel = x

            from Screens.ChoiceBox import ChoiceBox
            dlg = self.session.openWithCallback(self.choiceCamCallback, ChoiceBox, list=camlist, selection=sel)
            dlg.setTitle(_('Change Camd to %s') % cur[0])

    def choiceCamCallback(self, choice):
        if choice:
            cur = self['list'].getCurrent()
            if choice[0] != cur[1]:
                self.ACL.delService(cur[1], cur[3])
                self.ACL.addService(choice[0], cur[3])
                self.updateList()

    def keyOk(self):
        self.keyBlue()

    def exit(self):
        self.close()

    def updateList(self):
        from ServiceReference import ServiceReference
        self.list = []
        for cam, list in self.ACL.items():
            for service in list:
                if '1:0:' in service:
                    s = _('Channel')
                    servname = ServiceReference(service).getServiceName()
                else:
                    s = _('Provider')
                    servname = service
                self.list.append((servname,
                 cam,
                 s,
                 service))

        self['list'].setList(self.list)
        self['list'].updateList(self.list)

    def updateButtons(self):
        if len(self.list):
            self['key_red'].setText(_('Delete'))
            self['key_blue'].setText(_('Change Camd'))
        else:
            self['key_red'].setText(' ')
            self['key_blue'].setText(' ')


class AutoCamServiceSetup(ChannelSelectionBase):
    skin = '\n    <screen position="center,center" size="670,440" title="Channel Selection" flags="wfBorder">\n         <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/egami-plugin.png" position="16,10" size="640,40" zPosition="1" transparent="1" alphatest="on" />\n         <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/red.png" position="4,434" size="150,2" alphatest="on" />\n         <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/green.png" position="176,434" size="150,2" alphatest="on" />\n         <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/yellow.png" position="346,434" size="150,2" alphatest="on" />\n         <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/blue.png" position="514,434" size="150,2" alphatest="on" />\n         <widget name="key_red" position="4,412" zPosition="1" size="150,25" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n         <widget name="key_green" position="176,412" zPosition="1" size="150,25" font="Regular;18" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n         <widget name="key_yellow" position="346,412" zPosition="1" size="150,25" font="Regular;18" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n         <widget name="key_blue" position="512,412" zPosition="1" size="150,25" font="Regular;18" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />\n         <widget name="list" position="5,54" size="660,340" enableWrapAround="1" scrollbarMode="showOnDemand" selectionPixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/select001.png" />\n    </screen>\n    '

    def __init__(self, session, providers = False):
        self.providers = providers
        ChannelSelectionBase.__init__(self, session)
        self.bouquet_mark_edit = OFF
        from Components.ActionMap import ActionMap
        self['actions'] = ActionMap(['OkCancelActions', 'TvRadioActions'], {'cancel': self.close,
         'ok': self.channelSelected,
         'keyRadio': self.setModeRadio,
         'keyTV': self.setModeTv})
        self.onLayoutFinish.append(self.setModeTv)

    def channelSelected(self):
        ref = self.getCurrentSelection()
        if self.providers and ref.flags & 7 == 7:
            if 'provider' in ref.toString():
                self.close(ref)
            else:
                self.enterPath(ref)
        elif ref.flags & 7 == 7:
            self.enterPath(ref)
        elif not ref.flags & 64:
            self.close(ref)

    def setModeTv(self):
        self.setTvMode()
        if self.providers:
            self.showProviders()
        else:
            self.showFavourites()

    def setModeRadio(self):
        self.setRadioMode()
        if self.providers:
            self.showProviders()
        else:
            self.showFavourites()


def restartAutocam(self, cam, pip = False, preview = False):

    def doStop():
        timer.stop()
        self.camCtrl.command('stop')
        timer.callback.remove(doStop)
        timer.callback.append(doStart)
        timer.start(500, True)

    def doStart():
        timer.stop()
        self.camCtrl.select(cam)
        self.camCtrl.command('start')
        if config.plugins.autoCamSetup.autocam.switchinfo.value:
            if msgbox:
                try:
                    msgbox.close()
                except:
                    pass

        if pip:
            try:
                self.session.pip.playService(old_pip_ref)
            except:
                pass

        if old_ref:
            self.session.nav.playService(old_ref)
        if preview:
            self.show()

    if pip:
        try:
            old_pip_ref = self.session.pip.getCurrentServiceReference()
        except:
            pass

    old_ref = self.session.nav.getCurrentlyPlayingServiceReference()
    self.session.nav.stopService()
    self.hide()
    if config.plugins.autoCamSetup.autocam.switchinfo.value:
        msgbox = self.session.open(MessageBox, _("Switch camd :\n '%s' to '%s'") % (self.camCtrl.current(), cam), MessageBox.TYPE_INFO)
        msgbox.setTitle(_('Auto-Camd'))
    else:
        msgbox = False
    timer = eTimer()
    timer.callback.append(doStop)
    timer.start(500, True)


defHistoryPath = None

def hew_setHistoryPath(self, doZap = True, ref = None):
    global defHistoryPath
    val = config.plugins.autoCamSetup.autocam.enabled.value
    if not val or val and not doZap:
        defHistoryPath(self, doZap)
    else:
        ref = ref or self.session.nav.getCurrentlyPlayingServiceReference()
        defHistoryPath(self, doZap)
        nref = self.session.nav.getCurrentlyPlayingServiceReference()
        try:
            if self.session.pipshown:
                pip_show = True
            else:
                pip_show = False
        except:
            pip_show = False

        pip = True
        use_pip = config.plugins.autoCamSetup.autocam.pip.value
        if use_pip != '0' and pip_show:
            pip = False
        rec = True
        if config.plugins.autoCamSetup.autocam.checkrec.value and self.session.nav.getRecordings():
            rec = False
        if rec and pip:
            if nref and (ref is None or ref != nref):
                if not hasattr(self, 'camCtrl'):
                    self.camCtrl = CamControl('softcam')
                try:
                    provname = self.session.nav.getCurrentService().info().getInfoString(iServiceInformation.sProvider)
                except:
                    provname = None

                camname = getAutoCamForService(nref, provname)
                camcurrent = self.camCtrl.current()
                if camname and camname != camcurrent:
                    self.restartAutocam(camname)
                elif not camname and camcurrent != config.plugins.autoCamSetup.autocam.defcam.value:
                    self.restartAutocam(config.plugins.autoCamSetup.autocam.defcam.value)


defZap = None

def newZap(self, enable_pipzap = False, preview_zap = False, checkParentalControl = True, ref = None):
    global defZap
    if not config.plugins.autoCamSetup.autocam.enabled.value:
        defZap(self, enable_pipzap, preview_zap, checkParentalControl, ref)
    else:
        self.curRoot = self.startRoot
        nref = ref or self.getCurrentSelection()
        isPip = enable_pipzap and self.dopipzap
        cur_ref = self.session.nav.getCurrentlyPlayingServiceOrGroup()
        check_cam = False
        if isPip:
            cur_ref = self.session.pip.getCurrentService()
            if cur_ref is None or cur_ref != nref:
                nref = self.session.pip.resolveAlternatePipService(nref)
                if nref and (not checkParentalControl or Components.ParentalControl.parentalControl.isServicePlayable(nref, boundFunction(newZap, self, enable_pipzap=True, checkParentalControl=False))):
                    defZap(self, enable_pipzap, preview_zap, checkParentalControl, ref)
                    if self.session.pip.getCurrentService() is not None:
                        check_cam = True
                else:
                    self.setStartRoot(self.curRoot)
                    self.setCurrentSelection(cur_ref)
        elif cur_ref is None or cur_ref != nref:
            try:
                timeshift = config.usage.check_timeshift.value
                if timeshift:
                    config.usage.check_timeshift.value = False
            except:
                pass

            defZap(self, enable_pipzap, preview_zap, checkParentalControl, ref)
            check_cam = True
            try:
                if timeshift:
                    config.usage.check_timeshift.value = True
            except:
                pass

        else:
            defZap(self, enable_pipzap, preview_zap, checkParentalControl, ref)
        if check_cam:
            try:
                if self.session.pipshown:
                    pip_show = True
                else:
                    pip_show = False
            except:
                pip_show = False

            use_preview = True
            if not config.plugins.autoCamSetup.autocam.preview.value and preview_zap:
                use_preview = False
            preview = use_preview and preview_zap
            pip = True
            use_pip = config.plugins.autoCamSetup.autocam.pip.value
            if use_pip == '2':
                if pip_show:
                    pip = False
            elif use_pip == '1':
                if pip_show and not isPip:
                    pip = False
            rec = True
            if config.plugins.autoCamSetup.autocam.checkrec.value and self.session.nav.getRecordings():
                rec = False
            if rec and use_preview and pip:
                if not hasattr(self, 'camCtrl'):
                    self.camCtrl = CamControl('softcam')
                try:
                    if isPip:
                        service = self.session.pip.pipservice
                        provname = service and service.info().getInfoString(iServiceInformation.sProvider)
                    else:
                        service = self.session.nav.getCurrentService()
                        provname = service and service.info().getInfoString(iServiceInformation.sProvider)
                except:
                    provname = None

                camname = getAutoCamForService(nref, provname)
                camcurrent = self.camCtrl.current()
                if camname and camname != camcurrent:
                    self.restartAutocam(camname, pip_show, preview)
                elif not camname and camcurrent != config.plugins.autoCamSetup.autocam.defcam.value:
                    self.restartAutocam(config.plugins.autoCamSetup.autocam.defcam.value, pip_show, preview)


def StartMainSession(session):
    global defHistoryPath
    global defZap
    if defZap is None:
        defZap = ChannelSelection.zap
        ChannelSelection.zap = newZap
        ChannelSelection.restartAutocam = restartAutocam
    if defHistoryPath is None:
        defHistoryPath = ChannelSelection.setHistoryPath
        ChannelSelection.setHistoryPath = hew_setHistoryPath
