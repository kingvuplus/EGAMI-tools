from enigma import eTimer, getDesktop
from Screens.Screen import Screen
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Screens.ChoiceBox import ChoiceBox
from EGAMI.EGAMI_tools import runBackCmd, unload_modules, wyszukaj_re, checkkernel
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.GUIComponent import *
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from os import listdir
from Tools.Directories import fileExists
from os import system, listdir, chdir, mkdir, getcwd, rename as os_rename, remove as os_remove
from os.path import dirname, isdir

class EGAMIBackupPanel(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '\n\t\t\t<screen name="EGAMIBackupPanel" position="center,center" size="1040,680" >\n\t\t\t\t<widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;32" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label2" position="10,80" size="840,290" zPosition="1" font="Regular;26" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label3" position="10,110" size="1020,290" zPosition="1" font="Regular;26" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="list" itemHeight="50" font="Regular;28" position="10,170" size="840,290" scrollbarMode="showOnDemand"/>\n\t\t\t\t<ePixmap position="40,604" size="100,40" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="200,604" size="100,40" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="460,604" size="100,40" zPosition="0" pixmap="buttons/yellow.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<widget name="key_red" position="80,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="red" transparent="1" />\n\t\t\t\t<widget name="key_green" position="240,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="green" transparent="1" />\n\t\t\t\t<widget name="key_yellow" position="510,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="yellow" transparent="1" />\n\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen name="EGAMIBackupPanel" position="center,center" size="902,380" title="EGAMI Image Backup Panel - STEP 1" >\n\t\t\t      <widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;25" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <widget name="label2" position="10,80" size="840,290" zPosition="1" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <widget name="label3" position="10,110" size="840,290" zPosition="1" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <widget name="list" position="10,170" size="840,290" scrollbarMode="showOnDemand"/>\n\t\t\t      <ePixmap pixmap="skin_default/buttons/yellow.png" position="72,290" size="140,40" alphatest="on" />\n\t\t\t      <ePixmap pixmap="skin_default/buttons/blue.png" position="284,290" size="140,40" alphatest="on" />\n\t\t\t      <widget name="key_yellow" position="72,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t      <widget name="key_blue" position="284,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t\t</screen>'

    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('EGAMI Backup Panel'))
        m = checkkernel()
        if m == 1:
            print 'EGAMI Valid'
        else:
            self.close()
        self['label1'] = Label(_('1. STEP - Choose option RESTORE / BACKUP'))
        self['label2'] = Label(_('There is not any EGAMI Backup file on connected devices!'))
        self['label3'] = Label(_(''))
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('Restore EGAMI'))
        self['key_yellow'] = Label(_('Backup EGAMI'))
        self.mlist = []
        self['list'] = MenuList(self.mlist)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'red': self.close,
         'cancel': self.close,
         'yellow': self.backuP,
         'green': self.restorE}, -1)
        self.onLayoutFinish.append(self.updateT)

    def updateT(self):
        self.mybackupfile = ''
        mytext = _('There is not any EGAMI Backup file on connected devices!')
        mytext2 = _(' ')
        myfile = ''
        if fileExists('/etc/egami/.egamibackup_location'):
            fileExists('/etc/egami/.egamibackup_location')
            f = open('/etc/egami/.egamibackup_location', 'r')
            mypath = f.readline().strip()
            f.close()
            myscripts = listdir(mypath)
            for fil in myscripts:
                if fil.find('_EGAMI_Backup.egi') != -1:
                    mytext = 'There is EGAMI Backup file:'
                    mytext2 = 'Date:                      Device:                             Name:'

        else:
            fileExists('/etc/egami/.egamibackup_location')
        if myfile == '':
            myfile = self.scan_mediA()
        if fileExists('/etc/egami/.egamibackup_files'):
            fileExists('/etc/egami/.egamibackup_files')
            f = open('/etc/egami/.egamibackup_files', 'r')
            mypath = f.readline().strip()
            f.close()
            if fileExists(mypath):
                mytext = 'There is EGAMI Backup file:'
                mytext2 = 'Date:                      Device:                             Name:'
        else:
            fileExists('/etc/egami/.egamibackup_location')
        self['label2'].setText(_(mytext))
        self['label3'].setText(_(mytext2))

    def scan_mediA(self):
        out = open('/etc/egami/.egamibackup_files', 'w')
        backup = 'ok'
        mylist = ['/media/hdd',
         '/media/cf',
         '/media/card',
         '/media/usb',
         '/media/usb2',
         '/media/usb3']
        for dic in mylist:
            if not fileExists(dic):
                mkdir(dic)
            myscripts = listdir(dic)
            for fil in myscripts:
                if fil.find('_EGAMI_Backup.egi') != -1:
                    fil2 = fil[9:-4]
                    date = fil[0:8]
                    plik = dic + '/' + date + '_' + fil2 + '.egi\n'
                    out.write(plik)
                    plik2 = date + '            ' + dic + '/        ' + '        ' + fil2
                    self.mlist.append((plik2, plik, dic))

        out.close()
        self['list'].setList(self.mlist)

    def myclose(self):
        self.close()

    def backuP(self):
        m = checkkernel()
        if m == 1:
            check = False
            if fileExists('/proc/mounts'):
                fileExists('/proc/mounts')
                f = open('/proc/mounts', 'r')
                for line in f.readlines():
                    if line.find('/media/cf') != -1:
                        check = True
                        continue
                    if line.find('/media/usb') != -1:
                        check = True
                        continue
                    if line.find('/media/usb2') != -1:
                        check = True
                        continue
                    if line.find('/media/usb3') != -1:
                        check = True
                        continue
                    if line.find('/media/card') != -1:
                        check = True
                        continue
                    if line.find('/hdd') != -1:
                        check = True
                        continue

                f.close()
            else:
                fileExists('/proc/mounts')
            if check == False:
                self.session.open(MessageBox, _('Sorry, there is not any connected devices in your STB.\nPlease connect HDD or USB to store/restore Your EGAMI Backup!'), MessageBox.TYPE_INFO)
            else:
                self.session.openWithCallback(self.myclose, EGAMIBackupPanel_Step2)
        else:
            self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)

    def restorE(self):
        m = checkkernel()
        if m == 1:
            check = False
            if fileExists('/proc/mounts'):
                fileExists('/proc/mounts')
                f = open('/proc/mounts', 'r')
                for line in f.readlines():
                    if line.find('/media/cf') != -1:
                        check = True
                        continue
                    if line.find('/media/usb') != -1:
                        check = True
                        continue
                    if line.find('/media/usb2') != -1:
                        check = True
                        continue
                    if line.find('/media/usb3') != -1:
                        check = True
                        continue
                    if line.find('/media/card') != -1:
                        check = True
                        continue
                    if line.find('/hdd') != -1:
                        check = True
                        continue

                f.close()
            else:
                fileExists('/proc/mounts')
            if check == False:
                self.session.open(MessageBox, _('Sorry, there is not any connected devices in your STB.\nPlease connect HDD or USB to store/restore Your EGAMI Backup!'), MessageBox.TYPE_INFO)
            else:
                backup_file = self['list'].l.getCurrentSelection()[1]
                if backup_file != '':
                    message = _('Do you really want to restore the EGAMI Backup:\n ') + self.mybackupfile + ' ?'
                    self.session.openWithCallback(self.restorE_2, MessageBox, message, MessageBox.TYPE_YESNO)
                else:
                    system('umount /media/egamibackup_location')
                    system('rmdir /media/egamibackup_location')
                    self.session.open(MessageBox, _('Sorry, EGAMI Backup not found.'), MessageBox.TYPE_INFO)
        else:
            self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)

    def restorE_2(self, answer):
        if answer is True:
            backup_file = self['list'].l.getCurrentSelection()[1]
            backup_path = self['list'].l.getCurrentSelection()[2]
            self.session.open(EGAMIRestorePanel_Step1, backup_file, backup_path)


class EGAMIBackupPanel_Step2(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '\n\t\t\t<screen name="EGAMIBackupPanel_Step2" position="center,center" size="1040,680" >\n\t\t\t\t<widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;32" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label2" position="10,80" size="840,290" zPosition="1" font="Regular;26" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="config" itemHeight="50" font="Regular;28" position="10,170" size="840,290" scrollbarMode="showOnDemand"/>\n\t\t\t\t<ePixmap position="40,604" size="100,40" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="200,604" size="100,40" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<widget name="key_red" position="80,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="red" transparent="1" />\n\t\t\t\t<widget name="key_green" position="240,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="green" transparent="1" />\n\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen name="EGAMIBackupPanel_Step2" position="center,center" size="902,380" >\n\t\t\t      <widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;25" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <widget name="label2" position="10,80" size="840,290" zPosition="1" halign="center" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <widget name="config" position="130,160" size="450,290" scrollbarMode="showOnDemand"/>\n\t\t\t      <ePixmap pixmap="skin_default/buttons/yellow.png" position="200,340" size="140,40" alphatest="on"/>\n\t\t\t      <ePixmap pixmap="skin_default/buttons/green.png" position="550,340" size="140,40" alphatest="on"/>\n\t\t\t      <widget name="key_yellow" position="200,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <widget name="key_green" position="550,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>\n\t\t\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('EGAMI Backup Location - STEP 2'))
        self.list = []
        self['config'] = MenuList(self.list)
        self['key_green'] = Label(_('Backup EGAMI'))
        self['key_red'] = Label(_('Cancel'))
        self['label1'] = Label(_('2. STEP - Choose backup location'))
        self['label2'] = Label(_('Here is the list of mounted devices in Your STB\nPlease choose a device where You would like to keep Your backup:'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': self.saveMysets,
         'red': self.close,
         'back': self.close})
        self.updateList()

    def updateList(self):
        mycf, myusb, myusb2, myusb3, mysd, myhdd = ('', '', '', '', '', '')
        myoptions = []
        if fileExists('/proc/mounts'):
            fileExists('/proc/mounts')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/cf') != -1:
                    mycf = '/media/cf/'
                    continue
                if line.find('/media/usb') != -1:
                    myusb = '/media/usb/'
                    continue
                if line.find('/media/usb2') != -1:
                    myusb2 = '/media/usb2/'
                    continue
                if line.find('/media/usb3') != -1:
                    myusb3 = '/media/usb3/'
                    continue
                if line.find('/media/card') != -1:
                    mysd = '/media/card/'
                    continue
                if line.find('/hdd') != -1:
                    myhdd = '/media/hdd/'
                    continue

            f.close()
        else:
            fileExists('/proc/mounts')
        if mycf:
            mycf
            self.list.append((_('CF card mounted in:        ') + mycf, mycf))
        else:
            mycf
        if myusb:
            myusb
            self.list.append((_('USB device mounted in:     ') + myusb, myusb))
        else:
            myusb
        if myusb2:
            myusb2
            self.list.append((_('USB 2 device mounted in:   ') + myusb2, myusb2))
        else:
            myusb2
        if myusb3:
            myusb3
            self.list.append((_('USB 3 device mounted in:   ') + myusb3, myusb3))
        else:
            myusb3
        if mysd:
            mysd
            self.list.append((_('SD card mounted in:         ') + mysd, mysd))
        else:
            mysd
        if myhdd:
            myhdd
            self.list.append((_('HDD mounted in:               ') + myhdd, myhdd))
        else:
            myhdd
        self['config'].setList(self.list)

    def myclose(self):
        self.close()

    def saveMysets(self):
        mysel = self['config'].getCurrent()
        out = open('/etc/egami/.egamibackup_location', 'w')
        out.write(mysel[1])
        out.close()
        if fileExists('/etc/egami/.egamibackup_location'):
            fileExists('/etc/egami/.egamibackup_location')
            self.session.openWithCallback(self.myclose, EGAMIBackupPanel_Step3)
        else:
            fileExists('/etc/egami/.egamibackup_location')
            self.session.open(MessageBox, _('You have to setup backup location.'), MessageBox.TYPE_INFO)


class EGAMIBackupPanel_Step3(Screen):
    skin = '\n\t\t<screen name="EGAMIBackupPanel_Step3" position="center,center" size="484,250" flags="wfNoBorder">\n\t\t      <widget name="status" position="0,0" size="484,250" zPosition="-1" pixmaps="/usr/lib/enigma2/python/EGAMI/icons/egami_icons/backup_1.png,egami_icons/backup_2.png,egami_icons/backup_3.png,egami_icons/backup_4.png,egami_icons/backup_5.png,egami_icons/backup_6.png"  />\n\t\t      <widget name="label" position="0,200" halign="center" size="484,60" zPosition="1" font="Regular;20" valign="top" transparent="1" />\n\t\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('EGAMI Backup in progress...'))
        self['status'] = MultiPixmap()
        self['status'].setPixmapNum(0)
        self['label'] = Label('')
        self.mylist = ['Libraries',
         'Firmwares',
         'Binaries',
         'SoftCams',
         'Scripts',
         'Bootlogos',
         'Uninstall files',
         'General Settings',
         'Cron',
         'Settings Channels Bouquets',
         'Openvpn',
         'Satellites Terrestrial',
         'Plugins',
         'END']
        self.mytmppath = '/media/hdd/'
        if fileExists('/etc/egami/.egamibackup_location'):
            fileExists('/etc/egami/.egamibackup_location')
            f = open('/etc/egami/.egamibackup_location', 'r')
            self.mytmppath = f.readline().strip()
            f.close()
        else:
            fileExists('/etc/egami/.egamibackup_location')
        self.mytmppath += 'egamibackup_location'
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updatepix)
        self.onShow.append(self.startShow)
        self.onClose.append(self.delTimer)
        system('rm -rf ' + self.mytmppath)
        system('mkdir ' + self.mytmppath)
        system('mkdir ' + self.mytmppath + '/etc')
        system('mkdir ' + self.mytmppath + '/lib')
        system('mkdir ' + self.mytmppath + '/usr')
        system('mkdir ' + self.mytmppath + '/scripts')
        system('mkdir ' + self.mytmppath + '/media')
        system('mkdir ' + self.mytmppath + '/media/hdd')
        system('mkdir ' + self.mytmppath + '/media/usb')
        system('mkdir ' + self.mytmppath + '/media/usb2')
        system('mkdir ' + self.mytmppath + '/media/usb3')
        configfile.save()

    def startShow(self):
        self.curpix = 0
        self.count = 0
        self.procesS()

    def updatepix(self):
        self.activityTimer.stop()
        self['status'].setPixmapNum(self.curpix)
        self.curpix += 1
        if self.curpix == 6:
            self.curpix = 0
            self.procesS()
        else:
            self.activityTimer.start(150)

    def procesS(self):
        cur = self.mylist[self.count]
        self['label'].setText(cur)
        if cur == 'Libraries':
            ret = system('cp -fd /lib/* ' + self.mytmppath + '/lib')
            ret = system('mkdir ' + self.mytmppath + '/usr/lib')
            ret = system('cp -fd /usr/lib/* ' + self.mytmppath + '/usr/lib')
        elif cur == 'Firmwares':
            ret = system('cp -rf /lib/firmware ' + self.mytmppath + '/lib')
            ret = system('mkdir ' + self.mytmppath + '/lib/modules')
            ret = system('cp -rf /lib/modules/* ' + self.mytmppath + '/lib/modules')
        elif cur == 'Binaries':
            ret = system('cp -fdr /usr/bin ' + self.mytmppath + '/usr')
        elif cur == 'SoftCams':
            ret = system('cp -rf /usr/emu_scripts ' + self.mytmppath + '/usr')
            ret = system('cp -rf /usr/keys ' + self.mytmppath + '/usr')
            ret = system('cp -rf /usr/scce ' + self.mytmppath + '/usr')
            ret = system('cp -rf /usr/scam ' + self.mytmppath + '/usr')
            ret = system('cp -rf /usr/tuxbox ' + self.mytmppath + '/usr')
        elif cur == 'Scripts':
            ret = system('cp -rf /usr/scripts ' + self.mytmppath + '/usr')
            ret = system('cp -rf /scripts/* ' + self.mytmppath + '/scripts')
        elif cur == 'Bootlogos':
            ret = system('mkdir ' + self.mytmppath + '/usr/share')
            ret = system('cp -f /usr/share/*.mvi ' + self.mytmppath + '/usr/share')
        elif cur == 'Uninstall files':
            ret = system('mkdir ' + self.mytmppath + '/usr/tuxbox')
            ret = system('cp -rf /usr/uninstall ' + self.mytmppath + '/usr')
            ret = system('cp -rf /usr/tuxbox/uninstall_emu ' + self.mytmppath + '/usr/tuxbox/')
        elif cur == 'General Settings':
            ret = system('mkdir ' + self.mytmppath + '/media/hdd')
            ret = system('mkdir ' + self.mytmppath + '/media/usb')
            ret = system('mkdir ' + self.mytmppath + '/media/usb2')
            ret = system('mkdir ' + self.mytmppath + '/media/usb3')
            ret = system('cp -rf /media/hdd/crossepg ' + self.mytmppath + '/media/hdd')
            ret = system('cp -rf /media/usb/crossepg ' + self.mytmppath + '/media/usb')
            ret = system('cp -rf /media/usb2/crossepg ' + self.mytmppath + '/media/usb2')
            ret = system('cp -rf /media/usb3/crossepg ' + self.mytmppath + '/media/usb3')
            ret = system('mkdir ' + self.mytmppath + '/etc/network')
            ret = system('cp -f /etc/* ' + self.mytmppath + '/etc')
            ret = system('cp -rf /etc/egami ' + self.mytmppath + '/etc')
            ret = system('cp -f /etc/network/interfaces ' + self.mytmppath + '/etc/network')
            ret = system('cp -rf /etc/MultiQuickButton ' + self.mytmppath + '/etc')
        elif cur == 'Cron':
            ret = system('cp -rf /etc/cron ' + self.mytmppath + '/etc')
        elif cur == 'Settings Channels Bouquets':
            ret = system('mkdir ' + self.mytmppath + '/usr/share/enigma2')
            ret = system('cp -rf /etc/enigma2 ' + self.mytmppath + '/etc')
            ret = system('cp -f /usr/share/enigma2/keymap.xml ' + self.mytmppath + '/usr/share/enigma2/')
        elif cur == 'Openvpn':
            ret = system('cp -rf /etc/openvpn ' + self.mytmppath + '/etc')
        elif cur == 'Satellites Terrestrial':
            ret = system('cp -rf /etc/tuxbox ' + self.mytmppath + '/etc')
        elif cur == 'Plugins':
            ret = system('mkdir ' + self.mytmppath + '/usr/lib/enigma2')
            ret = system('mkdir ' + self.mytmppath + '/usr/lib/enigma2/python')
            ret = system('mkdir ' + self.mytmppath + '/usr/lib/enigma2/python/Plugins')
            ret = system('cp -rf /usr/lib/enigma2/python/Plugins/Extensions ' + self.mytmppath + '/usr/lib/enigma2/python/Plugins')
            ret = system('cp -rf /usr/lib/enigma2/python/Plugins/SystemPlugins ' + self.mytmppath + '/usr/lib/enigma2/python/Plugins')
            self['label'].setText('Plugins')
        if cur != 'END':
            self.count += 1
            self.activityTimer.start(100)
        else:
            mydir = getcwd()
            chdir(self.mytmppath)
            cmd = 'tar -cf EGAMI_Backup.tar etc lib media usr scripts'
            rc = system(cmd)
            import datetime
            import time
            now = datetime.datetime.now()
            czas = now.strftime('%Y%m%d')
            filename = '../' + czas + '_EGAMI_Backup.egi'
            os_rename('EGAMI_Backup.tar', filename)
            chdir(mydir)
            self.session.open(MessageBox, _('EGAMI Backup complete! Please wait...'), MessageBox.TYPE_INFO, timeout=4)
            self.close()

    def delTimer(self):
        del self.activityTimer
        system('rm -rf ' + self.mytmppath)


class EGAMIRestorePanel_Step1(Screen, ConfigListScreen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '\n\t\t\t<screen name="EGAMIRestorePanel_Step1" position="center,center" size="1040,880" >\n\t\t\t\t<widget name="config" itemHeight="50" font="Regular;28" position="10,10" size="1020,750" scrollbarMode="showOnDemand"/>\n\t\t\t\t<ePixmap position="40,804" size="100,40" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="200,804" size="100,40" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<widget name="key_red" position="80,804" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="red" transparent="1" />\n\t\t\t\t<widget name="key_green" position="240,804" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="green" transparent="1" />\n\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen name="EGAMIRestorePanel_Step1" position="center,center" size="902,550" title="EGAMI Backup Restore - STEP 1">\n\t\t\t      <widget name="config" position="30,10" size="840,510" scrollbarMode="showOnDemand"/>\n\t\t\t      <ePixmap pixmap="skin_default/buttons/blue.png" position="380,510" size="140,40" alphatest="on"/>\n\t\t\t      <widget name="key_blue" position="380,510" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <ePixmap pixmap="skin_default/buttons/green.png" position="550,510" size="140,40" alphatest="on"/>\n\t\t\t      <widget name="key_green" position="550,510" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>\n\t\t\t</screen>'

    def __init__(self, session, mypath, backpath):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('EGAMI Backup Restore - STEP 1'))
        self.mypath = mypath
        self.backpath = backpath
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_green'] = Label(_('Restore'))
        self['key_red'] = Label(_('Cancel'))
        self['actions'] = ActionMap(['EGActions', 'OkCancelActions', 'WizardActions'], {'green': self.Continue,
         'ok': self.Continue,
         'cancel': self.cancel,
         'red': self.cancel})
        self.updateList()

    def cancel(self):
        self.close()

    def updateList(self):
        blist = ['Password',
         'Devices',
         'Network',
         'Cron',
         'Swap',
         'Keymaps',
         'Nfs',
         'Openvpn',
         'Inadyn',
         'Httpd',
         'Uninstall files',
         'Settings Channels Bouquets',
         'Satellites Terrestrial',
         'SoftCams',
         'Scripts',
         'Bootlogo',
         'Plugins Extensions',
         'System Plugins']
        for x in blist:
            item = NoSave(ConfigYesNo(default=True))
            item2 = getConfigListEntry(x, item)
            self.list.append(item2)

        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def Continue(self):
        mylist = ['start',
         'extract',
         'lib',
         'lib/firmware',
         'usr/lib',
         'usr/bin',
         'etc']
        for x in self['config'].list:
            if x[1].value == True:
                mylist.append(x[0])
                continue

        mylist.append('END')
        self.session.open(EGAMIRestorePanel_Step2, self.mypath, mylist, self.backpath)
        self.close()


class EGAMIRestorePanel_Step2(Screen):
    skin = '\n\t\t<screen name="EGAMIRestorePanel_Step2" position="center,center" size="484,250" title="EGAMI Restore in progress..." flags="wfNoBorder">\n\t\t\t<widget name="status" position="0,0" size="484,250" zPosition="-1" pixmaps="/usr/lib/enigma2/python/EGAMI/icons/egami_icons/restore_1.png,egami_icons/restore_2.png,egami_icons/restore_3.png,egami_icons/restore_4.png,egami_icons/restore_5.png,egami_icons/restore_6.png"  />\n\t\t\t<widget name="label" position="0,200" halign="center" size="484,60" zPosition="1" font="Regular;20" valign="top" transparent="1" />\n\t\t</screen>'

    def __init__(self, session, mypath, mylist, myback):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('EGAMI Restore in progress...'))
        self.mytext = 'Files extraction in progress...'
        self['status'] = MultiPixmap()
        self['status'].setPixmapNum(0)
        self['label'] = Label('')
        self.mypath = myback + '/egamibackup_location'
        self.mybackupfile = mypath
        self.mylist = mylist
        self.count = 0
        self.go = False
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'DirectionActions'], {'ok': self.hrestBox})
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updatepix)
        self.onShow.append(self.startShow)
        self.onClose.append(self.delTimer)

    def startShow(self):
        self.curpix = 0
        self.count = 0
        self.procesS()

    def updatepix(self):
        self.activityTimer.stop()
        self['status'].setPixmapNum(self.curpix)
        self.curpix += 1
        if self.curpix == 6:
            self.curpix = 0
            self.procesS()
        else:
            self.activityTimer.start(150)

    def procesS(self):
        cur = self.mylist[self.count]
        self['label'].setText(self.mytext)
        if cur == 'start':
            self.mytext = 'Archive Extraction'
        if cur == 'extract':
            system('mkdir ' + self.mypath)
            mydir = getcwd()
            chdir(self.mypath)
            cmd = 'tar -xf ' + self.mybackupfile
            rc = system(cmd)
            chdir(mydir)
        elif cur == 'lib':
            self.mytext = 'Merge directory ' + cur
            ret = self.mergediR('/lib')
        elif cur == 'lib/firmware':
            self.mytext = 'Merge directory ' + cur
            ret = self.mergediR('/lib/firmware')
        elif cur == 'usr/lib':
            self.mytext = 'Merge directory ' + cur
            ret = self.mergediR('/usr/lib')
        elif cur == 'usr/bin':
            self.mytext = 'Merge directory ' + cur
            ret = self.mergediR('/usr/bin')
        elif cur == 'etc':
            self.mytext = 'Merge directory ' + cur
            ret = self.mergediR('/etc')
        elif cur == 'Password':
            self.mytext = 'Restore ' + cur
            ret = system('cp -f ' + self.mypath + '/etc/passwd /etc/')
        elif cur == 'Devices':
            self.mytext = 'Restore ' + cur
            ret = system('cp -f ' + self.mypath + '/etc/fstab /etc/')
            ret = system('cp -f ' + self.mypath + '/scripts/dev_mount_script.sh /scripts/')
        elif cur == 'Network':
            self.mytext = 'Restore ' + cur
            ret = system('cp -f ' + self.mypath + '/etc/resolv.conf /etc/')
            ret = system('cp -f ' + self.mypath + '/etc/wpa_supplicant.conf /etc/')
            ret = system('cp -f ' + self.mypath + '/etc/network/interfaces /etc/network/')
        elif cur == 'Cron':
            self.mytext = 'Restore ' + cur
            ret = system('cp -rf ' + self.mypath + '/etc/cron /etc/')
        elif cur == 'Swap':
            self.mytext = 'Restore ' + cur
            ret = system('cp -f ' + self.mypath + '/scripts/swap_script.sh /scripts/')
        elif cur == 'Keymaps':
            self.mytext = 'Restore ' + cur
            system('cp -f ' + self.mypath + '/usr/share/enigma2/keymap.xml /usr/share/enigma2/')
        elif cur == 'Nfs':
            self.mytext = 'Restore ' + cur
            ret = system('cp -f ' + self.mypath + '/scripts/nfs_server_script.sh /scripts/')
        elif cur == 'Openvpn':
            self.mytext = 'Restore ' + cur
            ret = system('cp -f ' + self.mypath + '/scripts/openvpn_script.sh /scripts/')
            ret = system('cp -rf ' + self.mypath + '/etc/openvpn /etc/')
        elif cur == 'Inadyn':
            self.mytext = 'Restore ' + cur
            ret = system('cp -f ' + self.mypath + '/scripts/inadyn_script.sh /scripts/')
        elif cur == 'Httpd':
            self.mytext = 'Restore ' + cur
            ret = system('cp -f ' + self.mypath + '/scripts/httpd_script.sh /scripts/')
        elif cur == 'Uninstall files':
            self.mytext = 'Restore ' + cur
            ret = system('cp -rf ' + self.mypath + '/usr/uninstall /usr/')
            ret = system('cp -rf ' + self.mypath + '/usr/tuxbox/* /usr/tuxbox')
        elif cur == 'Settings Channels Bouquets':
            self.mytext = 'Restore ' + cur
            ret = system('cp -rf ' + self.mypath + '/etc/enigma2 /etc/')
        elif cur == 'Satellites Terrestrial':
            self.mytext = 'Restore ' + cur
            ret = system('cp -rf ' + self.mypath + '/etc/tuxbox /etc/')
        elif cur == 'SoftCams':
            self.mytext = 'Restore ' + cur
            ret = system('cp -rf ' + self.mypath + '/usr/emu_scripts /usr/')
            ret = system('cp -rf ' + self.mypath + '/usr/keys /usr/')
            ret = system('cp -rf ' + self.mypath + '/usr/scce /usr/')
            ret = system('cp -rf ' + self.mypath + '/etc/tuxbox/config /etc/tuxbox/')
        elif cur == 'Scripts':
            self.mytext = 'Restore ' + cur
            ret = system('cp -rf ' + self.mypath + '/usr/scripts /usr/')
        elif cur == 'Bootlogo':
            self.mytext = 'Restore ' + cur
            ret = system('cp -f ' + self.mypath + '/usr/share/*.mvi /usr/share/')
        elif cur == 'Plugins Extensions':
            self.mytext = 'Merge ' + cur
            ret = self.mergepluginS('Extensions')
        elif cur == 'System Plugins':
            self.mytext = 'Merge ' + cur
            ret = self.mergepluginS('SystemPlugins')
        if cur != 'END':
            self.count += 1
            self.activityTimer.start(100)
        else:
            self.mytext = 'Restore Complete. Click OK to restart the box\n'
            self['label'].setText(_(self.mytext))
            ret = system('umount /media/egamibackup_location')
            ret = system('rmdir /media/egamibackup_location')
            ret = system('rm -rf ' + self.mypath)
            self.go = True

    def mergediR(self, path):
        opath = self.mypath + path
        destpath = path
        odir = listdir(opath)
        destdir = listdir(destpath)
        for fil in odir:
            if fil not in destdir:
                f = opath + '/' + fil
                system('cp -rf ' + f + ' ' + destpath + '/')
                continue

        return 0

    def mergepluginS(self, pdir):
        opath = self.mypath + '/usr/lib/enigma2/python/Plugins/' + pdir
        destpath = '/usr/lib/enigma2/python/Plugins/' + pdir
        odir = listdir(opath)
        destdir = listdir(destpath)
        for fil in odir:
            if fil not in destdir:
                f = opath + '/' + fil
                system('cp -rf ' + f + ' ' + destpath + '/')
                continue

        return 0

    def delTimer(self):
        del self.activityTimer

    def hrestBox(self):
        if self.go == True:
            system('reboot -f')


class EGFullBackup(Screen, ConfigListScreen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '\n\t\t\t<screen name="EGFullBackup" position="center,center" size="1040,680" >\n\t\t\t\t<widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;32" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label2" position="10,80" size="840,290" zPosition="1" font="Regular;26" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="config" itemHeight="50" font="Regular;28" position="10,170" size="840,290" scrollbarMode="showOnDemand"/>\n\t\t\t\t<ePixmap position="40,604" size="100,40" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="200,604" size="100,40" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<widget name="key_red" position="80,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="red" transparent="1" />\n\t\t\t\t<widget name="key_green" position="240,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="green" transparent="1" />\n\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen name="EGFullBackup" position="center,center" size="902,380" >\n\t\t\t      <widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;25" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <widget name="label2" position="10,80" size="840,290" zPosition="1" halign="center" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <widget name="config" position="130,160" size="450,290" scrollbarMode="showOnDemand"/>\n\t\t\t      <ePixmap pixmap="skin_default/buttons/yellow.png" position="200,340" size="140,40" alphatest="on"/>\n\t\t\t      <ePixmap pixmap="skin_default/buttons/green.png" position="550,340" size="140,40" alphatest="on"/>\n\t\t\t      <widget name="key_yellow" position="200,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t      <widget name="key_green" position="550,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>\n\t\t\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('EGAMI Full Image Backup'))
        m = checkkernel()
        if m == 1:
            print 'EGAMI Valid'
        else:
            self.close()
        self.list = []
        self['config'] = MenuList(self.list)
        self['key_green'] = Label(_('Full Backup'))
        self['key_red'] = Label(_('Cancel'))
        self['label1'] = Label(_('1. STEP - Choose backup location'))
        self['label2'] = Label(_('Here is the list of mounted devices in Your STB\nPlease choose a device where You would like to keep Your backup:'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': self.saveMysets,
         'red': self.close,
         'back': self.close})
        self.deviceok = True
        self.updateList()

    def updateList(self):
        mycf, myusb, myusb2, myusb3, mysd, myhdd = ('', '', '', '', '', '')
        myoptions = []
        if fileExists('/proc/mounts'):
            fileExists('/proc/mounts')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/cf') != -1:
                    mycf = '/media/cf/'
                    continue
                if line.find('/media/usb') != -1:
                    myusb = '/media/usb/'
                    continue
                if line.find('/media/usb2') != -1:
                    myusb2 = '/media/usb2/'
                    continue
                if line.find('/media/usb3') != -1:
                    myusb3 = '/media/usb3/'
                    continue
                if line.find('/media/card') != -1:
                    mysd = '/media/card/'
                    continue
                if line.find('/hdd') != -1:
                    myhdd = '/media/hdd/'
                    continue

            f.close()
        else:
            fileExists('/proc/mounts')
        if mycf:
            mycf
            self.list.append((_('CF card mounted in:        ') + mycf, mycf))
        else:
            mycf
        if myusb:
            myusb
            self.list.append((_('USB device mounted in:     ') + myusb, myusb))
        else:
            myusb
        if myusb2:
            myusb2
            self.list.append((_('USB 2 device mounted in:   ') + myusb2, myusb2))
        else:
            myusb2
        if myusb3:
            myusb3
            self.list.append((_('USB 3 device mounted in:   ') + myusb3, myusb3))
        else:
            myusb3
        if mysd:
            mysd
            self.list.append((_('SD card mounted in:         ') + mysd, mysd))
        else:
            mysd
        if myhdd:
            myhdd
            self.list.append((_('HDD mounted in:               ') + myhdd, myhdd))
        else:
            myhdd
        self['config'].setList(self.list)
        print len(self.list)
        if len(self.list) < 1:
            self['label2'].setText(_('Sorry no device found to store backup. Please check your media in EGAMI devices panel.'))
            self.deviceok = False

    def myclose(self):
        self.close()

    def saveMysets(self):
        if self.deviceok == True:
            mysel = self['config'].getCurrent()
            mytitle = 'EGAMI Full Backup on: ' + mysel[1]
            cmd = '/usr/lib/enigma2/python/EGAMI/bin/egami_backup.sh ' + mysel[1]
            self.session.open(Console, title=mytitle, cmdlist=[cmd], finishedCallback=self.myclose)
        else:
            self.session.open(MessageBox, _('Sorry, there is not any connected devices in your STB.\nPlease connect HDD or USB to full backup Your EGAMI Image!'), MessageBox.TYPE_INFO)
