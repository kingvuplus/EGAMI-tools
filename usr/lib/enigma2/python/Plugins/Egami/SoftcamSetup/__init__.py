#Coded By SODO
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigText, ConfigSelection

def localeInit():
    lang = language.getLanguage()[:2]
    os_environ['LANGUAGE'] = lang
    gettext.bindtextdomain('SoftcamSetup', resolveFilename(SCOPE_PLUGINS, 'Egami/SoftcamSetup/locale'))


def _(txt):
    t = gettext.dgettext('SoftcamSetup', txt)
    if t == txt:
        print '[SoftcamSetup] fallback to default translation for', txt
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
AutoCamSetupInfoBarKeys = [['none', _('NONE'), ['KEY_RESERVED']],
 ['Red', _('RED'), ['KEY_RED']],
 ['Green', _('GREEN'), ['KEY_GREEN']],
 ['Yellow', _('YELLOW'), ['KEY_YELLOW']],
 ['Radio', _('RADIO'), ['KEY_RADIO']],
 ['Text', _('TEXT'), ['KEY_TEXT']],
 ['Tv', _('TV'), ['KEY_TV']],
 ['Help', _('HELP'), ['KEY_HELP']]]
config.plugins.autoCamSetup = ConfigSubsection()
config.plugins.autoCamSetup.ext_menu = ConfigYesNo(True)
config.plugins.autoCamSetup.hotkey = ConfigSelection([ (x[0], x[1]) for x in AutoCamSetupInfoBarKeys ], 'none')
config.plugins.autoCamSetup.long_hotkey = ConfigSelection([('s', _('restart softcam')),
 ('c', _('restart Egami cardserver')),
 ('sc', _('restart both')),
 ('no', _('disabled'))], default='no')
config.plugins.autoCamSetup.restart_choice = ConfigSelection([('1', _('restart Egami softcam')), ('2', _('restart Egami cardserver')), ('3', _('restart both'))], default='1')
config.plugins.autoCamSetup.show_ecm = ConfigYesNo(default=False)
config.plugins.autoCamSetup.close_on_restart = ConfigYesNo(True)
config.plugins.autoCamSetup.autocam = ConfigSubsection()
config.plugins.autoCamSetup.autocam.enabled = ConfigYesNo(False)
config.plugins.autoCamSetup.autocam.checkrec = ConfigYesNo(True)
config.plugins.autoCamSetup.autocam.switchinfo = ConfigYesNo(True)
config.plugins.autoCamSetup.autocam.pip = ConfigSelection([('0', _('always')), ('1', _('only Pip-Zap')), ('2', _('newer'))], default='2')
config.plugins.autoCamSetup.autocam.preview = ConfigYesNo(False)
config.plugins.autoCamSetup.autocam.history_zap = ConfigYesNo(False)
config.plugins.autoCamSetup.autocam.defcam = ConfigText('None')
