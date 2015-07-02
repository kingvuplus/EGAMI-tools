#Coded By SODO
from . import _, AutoCamSetupInfoBarKeys
import Camsetup
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigText, ConfigSelection
from Plugins.Plugin import PluginDescriptor
from keyids import KEYIDS
from enigma import eActionMap
oldInfoBar__init__ = None

def newInfoBar__init__(self, session):
    global oldInfoBar__init__
    oldInfoBar__init__(self, session)
    self.autocaminfobar = AutoCamSetupInfoBar(session, self)


class AutoCamSetupInfoBar:

    def __init__(self, session, infobar):
        self.session = session
        self.infobar = infobar
        self.lastKey = None
        self.hotkeys = {}
        for x in AutoCamSetupInfoBarKeys:
            self.hotkeys[x[0]] = [ KEYIDS[key] for key in x[2] ]

        eActionMap.getInstance().bindAction('', -10, self.keyPressed)

    def keyPressed(self, key, flag):
        for k in self.hotkeys[config.plugins.autoCamSetup.hotkey.value]:
            if key == k and self.session.current_dialog == self.infobar:
                if flag == 0:
                    self.lastKey = key
                elif self.lastKey != key or flag == 4:
                    self.lastKey = None
                    continue
                elif flag == 3:
                    self.lastKey = None
                    if config.plugins.autoCamSetup.long_hotkey.value == 'no':
                        return 0
                    self.RestartCam()
                elif flag == 1:
                    self.lastKey = None
                    self.openCamsetup()
                return 1

        return 0

    def RestartCam(self):
        if not hasattr(self.session, 'camsetup'):
            self.session.camsetup = self.session.instantiateDialog(Camsetup.CamsetupSelection)
        if hasattr(self.session, 'camsetup'):
            self.session.camsetup.restartCam()

    def openCamsetup(self):
        self.session.open(Camsetup.CamsetupSelection)


def autostart(reason, **kwargs):
    global oldInfoBar__init__
    if reason == 0:
        from Screens.InfoBar import InfoBar
        if oldInfoBar__init__ is None:
            oldInfoBar__init__ = InfoBar.__init__
        InfoBar.__init__ = newInfoBar__init__
        if 'session' in kwargs:
            from autocam import StartMainSession
            session = kwargs['session']
            if session is not None:
                StartMainSession(session)


def main(session, **kwargs):
    session.open(Camsetup.CamsetupSelection)


def menu(menuid, **kwargs):
    if menuid == 'cam':
        return [(_('Egami Cam Manager'),
          main,
          'softcam_setup',
          -1)]
    return []


def Plugins(**kwargs):
    try:
        return [PluginDescriptor(name='Egami Cam Manager', description='Active Your Emu Softcam', where=PluginDescriptor.WHERE_PLUGINMENU, icon='egami.png', fnc=main), PluginDescriptor(name='Egami Cam Manager', description='Emu Softcam', where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon='egami.png', fnc=main)]
    except:
        return [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc=autostart), PluginDescriptor(name='Egami Cam Manager', description='Active Your Emu Softcam', where=PluginDescriptor.WHERE_PLUGINMENU, icon='egami.png', fnc=main)]
