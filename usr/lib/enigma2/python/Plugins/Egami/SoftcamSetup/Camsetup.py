#Coded By SODO
from . import _
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.config import config, ConfigElement, ConfigSubsection, ConfigSelection, ConfigSubList, getConfigListEntry, ConfigYesNo, ConfigEnableDisable, KEY_LEFT, KEY_RIGHT, KEY_OK
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.Pixmap import Pixmap
from Tools.Directories import fileExists
from Components.ScrollLabel import ScrollLabel
import os
from Tools.GetEcmInfo import ecm
from camcontrol import CamControl
from enigma import eTimer
try:
    from Plugins.Extensions.PPanel.ppanel import PPanel
    InstallPPanel = True
except:
    InstallPPanel = None

try:
    from Plugins.Extensions.HistoryZapSelector.plugin import UseAutoCamSetup
    HistoryZap = True
except:
    HistoryZap = False

class ConfigAction(ConfigElement):

    def __init__(self, action, *args):
        ConfigElement.__init__(self)
        self.value = '(OK)'
        self.action = action
        self.actionargs = args

    def handleKey(self, key):
        if key == KEY_OK:
            self.action(*self.actionargs)

    def getMulti(self, dummy):
        pass


EcmCamsetupSelection = '\n         <screen position="center,92" size="650,530" title="Autocam Setup" flags="wfBorder">\n           <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/egami-plugin.png" position="4,2" size="640,40" zPosition="1" transparent="1" alphatest="on" />\n               <widget name="cam" zPosition="2" position="14,236" size="310,22" font="Regular; 17" halign="left" foregroundColor="#00bab329" />\n                <widget name="entries" position="12,47" size="630,180" scrollbarMode="showOnDemand" selectionPixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/select002.png" />\n           <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/div-h.png" position="2,230" zPosition="2" size="646,2" />\n         <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/div-h.png" position="2,264" zPosition="2" size="646,2" />\n           <widget name="ecm" position="13,265" size="320,222" font="Regular;17" />\n             <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/image.png" position="368,397" size="225,95" alphatest="on" zPosition="-1" transparent="0" />\n             <ePixmap position="20,522" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/red.png" transparent="1" alphatest="on" />\n           <ePixmap position="474,522" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/green.png" transparent="1" alphatest="on" />\n           <widget name="key_red" position="20,498" zPosition="2" size="150,25" valign="top" halign="center" font="Regular; 18" transparent="1" />\n           <widget name="key_green" position="474,498" zPosition="2" size="150,25" valign="top" halign="center" font="Regular; 18" transparent="1" />\n           <widget name="info_key" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/key_info.png" position="226,497" zPosition="2" size="30,25" alphatest="on" />\n           <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/key_menu.png" position="382,497" zPosition="2" size="30,25" alphatest="on" />\n         </screen>'
NoEcmCamsetupSelection = '\n       <screen position="center,center" size="650,330" title="Autocam Setup" flags="wfBorder">\n           <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/egami-plugin.png" position="5,10" size="640,40" zPosition="1" transparent="1" alphatest="on" />\n           <widget name="cam" zPosition="2" position="4,60" size="310,21" font="Regular; 17" halign="left" foregroundColor="yellow" />\n           <widget name="server" zPosition="2" position="314,60" size="328,21" font="Regular; 17" halign="left" foregroundColor="yellow" />\n           <widget name="entries" position="4,88" size="640,206" scrollbarMode="showOnDemand" selectionPixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/select004.png" />\n           <ePixmap position="80,322" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/red.png" transparent="1" alphatest="on" />\n           <ePixmap position="415,322" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/green.png" transparent="1" alphatest="on" />\n           <widget name="key_red" position="82,299" zPosition="2" size="150,25" valign="center" halign="center" font="Regular; 18" transparent="1" />\n           <widget name="key_green" position="414,299" zPosition="2" size="150,25" valign="center" halign="center" font="Regular; 18" transparent="1" />\n           <widget name="info_key" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/key_info.png" position="268,299" zPosition="2" size="30,25" alphatest="on" />\n           <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/key_menu.png" position="354,300" zPosition="2" size="30,25" alphatest="on" />\n         </screen>'

class CamsetupSelection(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        if config.plugins.autoCamSetup.show_ecm.value:
            self.skin = EcmCamsetupSelection
        else:
            self.skin = NoEcmCamsetupSelection
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'EPGSelectActions',
         'CiSelectionActions'], {'left': self.keyLeft,
         'right': self.keyRight,
         'cancel': self.cancel,
         'ok': self.ok,
         'green': self.save,
         'red': self.cancel,
         'menu': self.keyMenu,
         'info': self.ppanelShortcut}, -1)
        self.setTitle(_('Egami Softcam Setup'))
        self.prev_mtime = 0
        self.prev_mtime1 = 0
        if config.plugins.autoCamSetup.show_ecm.value:
            self['ecm'] = ScrollLabel()
            self['ecm1'] = ScrollLabel()
            self.EcmTimer = eTimer()
            self.EcmTimer1 = eTimer()
            self.EcmTimer.callback.append(self.showEcmInfo)
            self.EcmTimer1.callback.append(self.showEcmInfo1)
            self.EcmTimer.start(50, True)
            self.EcmTimer1.start(50, True)
        self.softcam = CamControl('softcam')
        self.cardserver = CamControl('cardserver')
        self['entries'] = ConfigList([])
        self.initConfig()
        self.createConfig()
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('OK'))
        self['cam'] = Label()
        self['server'] = Label()
        self['info_key'] = Pixmap()
        self['info_key'].hide()
        if InstallPPanel:
            ppanelFileName = '/etc/ppanels/' + self.softcams.value + '.xml'
            if os.path.isfile(ppanelFileName):
                self['info_key'].show()
        self.nameSoftcam()
        self.nameCardserver()
        self.onClose.append(self.__onClose)

    def __onClose(self):
        config.plugins.autoCamSetup.autocam.enabled.save()
        if config.plugins.autoCamSetup.autocam.enabled.value:
            config.plugins.autoCamSetup.autocam.defcam.value = self.softcams.value
            config.plugins.autoCamSetup.autocam.defcam.save()
        else:
            config.plugins.autoCamSetup.autocam.defcam.cancel()

    def initConfig(self):
        self.softcams = ConfigSelection(choices=self.softcam.getList())
        self.cfg_autocam = getConfigListEntry(_('Switch auto-camd'), config.plugins.autoCamSetup.autocam.enabled)
        self.cfg_autocam_setup = getConfigListEntry(_('Additional Settings Auto-Camd'), ConfigAction(self.AdditionalsetupAutoCam, None))
        self.cfg_aclsetup = getConfigListEntry(_('Setup Auto-Camd List'), ConfigAction(self.setupAutoCamList, None))

    def createConfig(self):
        cardservers = self.cardserver.getList()
        list = []
        if config.plugins.autoCamSetup.restart_choice.value == '1':
            list.append(getConfigListEntry(_('Restart Egami Softcam'), ConfigAction(self.restart, 's')))
            if cardservers:
                list.append(getConfigListEntry(_('Restart Egami Cardserver'), ConfigAction(self.restart, 'c')))
                list.append(getConfigListEntry(_('Restart Both'), ConfigAction(self.restart, 'sc')))
        elif config.plugins.autoCamSetup.restart_choice.value == '2':
            if cardservers:
                list.append(getConfigListEntry(_('Restart Egami Cardserver'), ConfigAction(self.restart, 'c')))
            list.append(getConfigListEntry(_('Restart Egami Softcam'), ConfigAction(self.restart, 's')))
            if cardservers:
                list.append(getConfigListEntry(_('Restart Both'), ConfigAction(self.restart, 'sc')))
        elif config.plugins.autoCamSetup.restart_choice.value == '3':
            if cardservers:
                list.append(getConfigListEntry(_('Restart Both'), ConfigAction(self.restart, 'sc')))
            list.append(getConfigListEntry(_('Restart Egami Softcam'), ConfigAction(self.restart, 's')))
            if cardservers:
                list.append(getConfigListEntry(_('Select Egami Cardserver'), ConfigAction(self.restart, 'c')))
        list.append(self.cfg_autocam)
        if not config.plugins.autoCamSetup.autocam.enabled.value:
            self.softcams.value = self.softcam.current()
            list.append(getConfigListEntry(_('Select Egami Softcam'), self.softcams))
        else:
            self.softcams.value = config.plugins.autoCamSetup.autocam.defcam.value
            list.append(getConfigListEntry(_('Default Egami Camd'), self.softcams))
            list.append(self.cfg_aclsetup)
            list.append(self.cfg_autocam_setup)
        if cardservers:
            self.cardservers = ConfigSelection(choices=cardservers)
            self.cardservers.value = self.cardserver.current()
            list.append(getConfigListEntry(_('Select Egami Cardserver'), self.cardservers))
        self['entries'].list = list
        self['entries'].l.setList(list)

    def newConfig(self):
        cur = self['entries'].getCurrent()
        if cur == self.cfg_autocam:
            self.createConfig()
        elif cur == self.cfg_aclsetup:
            self.setupAutoCamList()
        elif cur == self.cfg_autocam_setup:
            self.AdditionalsetupAutoCam()

    def keyLeft(self):
        self['entries'].handleKey(KEY_LEFT)
        self.newConfig()

    def keyRight(self):
        self['entries'].handleKey(KEY_RIGHT)
        self.newConfig()

    def ok(self):
        self['entries'].handleKey(KEY_OK)

    def restart(self, what):
        self.what = what
        if 's' in what:
            if 'c' in what:
                msg = _('Please wait, restarting Egami softcam and cardserver.')
            else:
                msg = _('Please wait, restarting Egami softcam.')
        elif 'c' in what:
            msg = _('Please wait, restarting Egami cardserver.')
        else:
            return
        try:
            self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
        except:
            self.mbox = None

        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.doStop)
        self.activityTimer.start(100, False)

    def doStop(self):
        self.activityTimer.stop()
        if 'c' in self.what:
            self.cardserver.command('stop')
        if 's' in self.what:
            self.softcam.command('stop')
        self.oldref = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.doStart)
        self.activityTimer.start(1000, False)

    def doStart(self):
        self.activityTimer.stop()
        del self.activityTimer
        if 'c' in self.what:
            self.cardserver.select(self.cardservers.value)
            self.cardserver.command('start')
        if 's' in self.what:
            self.softcam.select(self.softcams.value)
            self.softcam.command('start')
        if self.mbox:
            self.mbox.close()
        if config.plugins.autoCamSetup.close_on_restart.value:
            self.close()
        else:
            self.nameSoftcam()
            self.nameCardserver()
        self.session.nav.playService(self.oldref)
        del self.oldref

    def restartCardServer(self):
        if hasattr(self, 'cardservers'):
            self.restart('c')

    def restartSoftcam(self):
        self.restart('s')

    def restartCam(self):
        val = config.plugins.autoCamSetup.long_hotkey.value
        if val == 'c' or val == 'sc':
            cardservers = self.cardserver.getList()
            if cardservers:
                self.restart(val)
        elif val == 's':
            self.restart(val)

    def save(self):
        what = ''
        if hasattr(self, 'cardservers') and self.cardservers.value != self.cardserver.current():
            what = 'sc'
        elif self.softcams.value != self.softcam.current():
            what = 's'
        if what:
            self.restart(what)
        else:
            self.close()

    def ppanelShortcut(self):
        if InstallPPanel:
            ppanelFileName = '/etc/ppanels/' + self.softcams.value + '.xml'
            if os.path.isfile(ppanelFileName) and os.path.isdir('/usr/lib/enigma2/python/Plugins/Extensions/PPanel'):
                self.session.open(PPanel, name=self.softcams.value + ' PPanel', node=None, filename=ppanelFileName, deletenode=None)
            else:
                return 0
        else:
            return 0

    def keyMenu(self):
        self.session.openWithCallback(self.createConfig, CamSetupScreen)

    def nameSoftcam(self):
        name = ''
        if fileExists('/etc/init.d/softcam'):
            try:
                f = os.popen('/etc/init.d/softcam info')
                for i in f.readlines():
                    text = _('Current softcam: ')
                    name = text + i

            except:
                pass

        self['cam'].setText(name)

    def nameCardserver(self):
        name = ''
        if fileExists('/etc/init.d/cardserver'):
            try:
                f = os.popen('/etc/init.d/cardserver info')
                for i in f.readlines():
                    text = _('Current cardserver: ')
                    name = text + i

            except:
                pass

        self['server'].setText(name)

    def showEcmInfo(self):
        text = ''
        snow_text = False
        if fileExists('/tmp/ecm.info'):
            try:
                st = os.stat('/tmp/ecm.info')
                if st.st_size > 0 and self.prev_mtime < st.st_mtime:
                    self.prev_mtime = st.st_mtime
                    f = open('/tmp/ecm.info', 'r')
                    for line in f:
                        text += line

                    f.close()
                    snow_text = True
            except:
                snow_text = True

        else:
            self.prev_mtime = 0
            snow_text = True
        if snow_text:
            self['ecm'].setText(text)
        self.EcmTimer.start(1500, True)

    def showEcmInfo1(self):
        text = ''
        snow_text = False
        if fileExists('/tmp/ecm1.info'):
            try:
                st = os.stat('/tmp/ecm1.info')
                if st.st_size > 0 and self.prev_mtime1 < st.st_mtime:
                    self.prev_mtime1 = st.st_mtime
                    f = open('/tmp/ecm1.info', 'r')
                    for line in f:
                        text += line

                    f.close()
                    snow_text = True
            except:
                snow_text = True

        else:
            self.prev_mtime1 = 0
            snow_text = True
        if snow_text:
            self['ecm1'].setText(text)
        self.EcmTimer1.start(1500, True)

    def cancel(self):
        self.close()

    def AdditionalsetupAutoCam(self, *args):
        self.session.open(AdditionalAutoCamSetup, None)

    def setupAutoCamList(self, *args):
        from autocam import AutoCamListSetup
        self.session.open(AutoCamListSetup, self.softcam)


class CamSetupScreen(Screen, ConfigListScreen):
    skin = '\n\t\t<screen position="center,center" size="650,330" title="Additional settings" flags="wfBorder">\n                        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/egami-plugin.png" position="5,10" size="640,40" zPosition="1" transparent="1" alphatest="on" />\n             <ePixmap position="80,322" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/red.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap position="415,322" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/green.png" transparent="1" alphatest="on" />\n\t\t\t<widget name="red" position="82,299" zPosition="2" size="150,25" valign="center" halign="center" font="Regular; 18" transparent="1" />\n\t\t\t<widget name="green" position="414,299" zPosition="2" size="150,25" valign="center" halign="center" font="Regular; 18" transparent="1" />\n\t\t\t<widget name="config" position="8,58" size="640,206" font="Regular;22" scrollbarMode="showOnDemand" selectionPixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/select004.png" />\n\t\t</screen>\n\t\t'

    def __init__(self, session, args = None):
        self.skin = CamSetupScreen.skin
        self.setup_title = _('Egami Additional Settings')
        Screen.__init__(self, session)
        self['red'] = Button(_('Cancel'))
        self['green'] = Button(_('OK'))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.keyOk,
         'save': self.keyGreen,
         'cancel': self.keyRed}, -2)
        ConfigListScreen.__init__(self, [])
        self.initConfig()
        self.createSetup()
        self.onClose.append(self.__closed)
        self.onLayoutFinish.append(self.__layoutFinished)

    def __closed(self):
        pass

    def __layoutFinished(self):
        self.setTitle(self.setup_title)

    def initConfig(self):

        def getPrevValues(section):
            res = {}
            for key, val in section.content.items.items():
                if isinstance(val, ConfigSubsection):
                    res[key] = getPrevValues(val)
                else:
                    res[key] = val.value

            return res

        self.SC = config.plugins.autoCamSetup
        self.prev_values = getPrevValues(self.SC)
        self.cfg_MenuExt = getConfigListEntry(_('Show Egami plugin In extensions menu'), self.SC.ext_menu)
        self.cfg_quickButton = getConfigListEntry(_('Quick button'), self.SC.hotkey)
        self.cfg_longKey = getConfigListEntry(_('Action when long-keys'), self.SC.long_hotkey)
        self.cfg_RestartChoice = getConfigListEntry(_('Open plugin - cursor to restart:'), self.SC.restart_choice)
        self.cfg_showEcm = getConfigListEntry(_('Show Egami ecm.info'), self.SC.show_ecm)
        self.cfg_CloseOnRestart = getConfigListEntry(_('Close plugin on restart emu'), self.SC.close_on_restart)

    def createSetup(self):
        list = [self.cfg_MenuExt]
        list.append(self.cfg_RestartChoice)
        list.append(self.cfg_quickButton)
        if self.SC.hotkey.value != 'none':
            list.append(self.cfg_longKey)
        list.append(self.cfg_showEcm)
        if self.SC.show_ecm.value:
            list.append(self.cfg_CloseOnRestart)
        self['config'].list = list
        self['config'].l.setList(list)

    def newConfig(self):
        cur = self['config'].getCurrent()
        if cur in (self.cfg_MenuExt,
         self.cfg_quickButton,
         self.cfg_longKey,
         self.cfg_RestartChoice,
         self.cfg_showEcm,
         self.cfg_CloseOnRestart):
            self.createSetup()

    def keyOk(self):
        self.keyGreen()

    def keyRed(self):

        def setPrevValues(section, values):
            for key, val in section.content.items.items():
                value = values.get(key, None)
                if value is not None:
                    if isinstance(val, ConfigSubsection):
                        setPrevValues(val, value)
                    else:
                        val.value = value

        setPrevValues(self.SC, self.prev_values)
        self.keyGreen()

    def keyGreen(self):
        if not self.SC.show_ecm.value:
            self.SC.close_on_restart.value = True
        self.SC.save()
        self.close()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.newConfig()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.newConfig()


class AdditionalAutoCamSetup(Screen, ConfigListScreen):
    skin = '\n\t\t<screen position="center,center" size="650,330" title="Additional setup Auto-Camd" flags="wfBorder">\n\t\t           <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/egami-plugin.png" position="5,10" size="640,40" zPosition="1" transparent="1" alphatest="on" />\n                        <ePixmap position="80,322" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/red.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap position="420,322" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/green.png" transparent="1" alphatest="on" />\n\t\t\t<widget name="red" position="82,300" zPosition="2" size="150,25" valign="center" halign="center" font="Regular; 18" transparent="1" />\n\t\t\t<widget name="green" position="420,300" zPosition="2" size="150,25" valign="center" halign="center" font="Regular; 18" transparent="1" />\n\t\t\t<widget name="config" position="4,52" size="640,220" font="Regular;21" scrollbarMode="showOnDemand" selectionPixmap="/usr/lib/enigma2/python/Plugins/Egami/SoftcamSetup/image/select004.png" />\n\t\t</screen>\n\t\t'

    def __init__(self, session, args = None):
        self.skin = AdditionalAutoCamSetup.skin
        self.setup_title = _('Egami Additional Settings Auto-Camd')
        Screen.__init__(self, session)
        self['red'] = Button(_('Cancel'))
        self['green'] = Button(_('OK'))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.keyOk,
         'save': self.keyGreen,
         'cancel': self.keyRed}, -2)
        ConfigListScreen.__init__(self, [])
        self.initConfig()
        self.createSetup()
        self.onClose.append(self.__closed)
        self.onLayoutFinish.append(self.__layoutFinished)

    def __closed(self):
        pass

    def __layoutFinished(self):
        self.setTitle(self.setup_title)

    def initConfig(self):

        def getPrevValues(section):
            res = {}
            for key, val in section.content.items.items():
                if isinstance(val, ConfigSubsection):
                    res[key] = getPrevValues(val)
                else:
                    res[key] = val.value

            return res

        self.AutoCamSetup = config.plugins.autoCamSetup.autocam
        self.prev_values = getPrevValues(self.AutoCamSetup)
        self.cfg_switchinfo = getConfigListEntry(_('Show a message when switching Egami Camd'), self.AutoCamSetup.switchinfo)
        self.cfg_checkrec = getConfigListEntry(_("Don't switch auto-camd while recording"), self.AutoCamSetup.checkrec)
        self.cfg_pip = getConfigListEntry(_('Switch Egami camd when PiP is enabled'), self.AutoCamSetup.pip)
        self.cfg_preview = getConfigListEntry(_('To switch Egami camd in the standard preview'), self.AutoCamSetup.preview)
        self.cfg_preview_historyzap = getConfigListEntry(_('Change Egami Camd when using plug- zaphistory'), self.AutoCamSetup.history_zap)

    def createSetup(self):
        list = [self.cfg_switchinfo]
        list.append(self.cfg_checkrec)
        list.append(self.cfg_pip)
        list.append(self.cfg_preview)
        if HistoryZap:
            list.append(self.cfg_preview_historyzap)
        self['config'].list = list
        self['config'].l.setList(list)

    def newConfig(self):
        pass

    def keyOk(self):
        self.keyGreen()

    def keyRed(self):

        def setPrevValues(section, values):
            for key, val in section.content.items.items():
                value = values.get(key, None)
                if value is not None:
                    if isinstance(val, ConfigSubsection):
                        setPrevValues(val, value)
                    else:
                        val.value = value

        setPrevValues(self.AutoCamSetup, self.prev_values)
        self.keyGreen()

    def keyGreen(self):
        self.AutoCamSetup.switchinfo.save()
        self.AutoCamSetup.checkrec.save()
        self.AutoCamSetup.pip.save()
        self.AutoCamSetup.preview.save()
        self.AutoCamSetup.history_zap.save()
        self.close()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.newConfig()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.newConfig()
