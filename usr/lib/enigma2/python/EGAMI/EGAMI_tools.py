from Components.Label import Label
from Components.config import config, configfile
from Screens.Screen import Screen
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_SKIN, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from os import path as os_path
from enigma import eConsoleAppContainer
import re, string
import os
from socket import *
import socket
from Components.About import about

def checkkernel():
    mycheck = 0
    if not fileExists('/media/usb'):
        os.system('mkdir /media/usb')
    if os.path.isfile('/proc/stb/info/vumodel') and os.path.isfile('/proc/stb/info/version'):
        if open('/proc/stb/info/vumodel').read().startswith('uno') or open('/proc/stb/info/vumodel').read().strip() == 'duo' or open('/proc/stb/info/vumodel').read().startswith('solo') or open('/proc/stb/info/vumodel').read().startswith('ultimo') or open('/proc/stb/info/vumodel').read().startswith('solo2') or open('/proc/stb/info/vumodel').read().startswith('duo2'):
            if about.getKernelVersionString() == '3.13.5' or about.getKernelVersionString() == '3.9.6':
                mycheck = 1
        else:
            mycheck = 0
        return mycheck


def readEmuName():
    try:
        fp = open('/etc/magic/.emuname', 'r')
        emuLine = fp.readline()
        fp.close()
        emuLine = emuLine.strip('\n')
        return emuLine
    except:
        return 'CI'


def readEcmFile():
    try:
        ecmfile = file('/tmp/ecm.info', 'r')
        ecmfile_r = ecmfile.read()
        ecmfile.close()
        return ecmfile_r
    except:
        return 'ECM Info not aviable!'


def sendCmdtoEGEmuD(cmd):
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect('/tmp/magic.socket')
        print '[EG-EMU MANAGER] communicate with socket'
        s.send(cmd)
        s.close()
    except socket.error:
        print '[EG-EMU MANAGER] could not communicate with socket'
        if s is not None:
            s.close()


def runBackCmd(cmd):
    eConsoleAppContainer().execute(cmd)


def getRealName(string):
    if string.startswith(' '):
        while string.startswith(' '):
            string = string[1:]

    return string


def hex_str2dec(str):
    ret = 0
    try:
        ret = int(re.sub('0x', '', str), 16)
    except:
        pass

    return ret


def norm_hex(str):
    return '%04x' % hex_str2dec(str)


def loadcfg(plik, fraza, dlugosc):
    wartosc = '0'
    if fileExists(plik):
        f = open(plik, 'r')
        for line in f.readlines():
            line = line.strip()
            if line.find(fraza) != -1:
                wartosc = line[dlugosc:]

        f.close()
    return wartosc


def loadbool(plik, fraza, dlugosc):
    wartosc = '0'
    if fileExists(plik):
        f = open(plik, 'r')
        for line in f.readlines():
            line = line.strip()
            if line.find(fraza) != -1:
                wartosc = line[dlugosc:]

        f.close()
    if wartosc == '1':
        return True
    else:
        return False


def unload_modules(name):
    try:
        from sys import modules
        del modules[name]
    except:
        pass


def wyszukaj_in(zrodlo, szukana_fraza):
    wyrazenie = string.strip(szukana_fraza)
    for linia in zrodlo.xreadlines():
        if wyrazenie in linia:
            return True

    return False


def wyszukaj_re(szukana_fraza):
    wyrazenie = re.compile(string.strip(szukana_fraza), re.IGNORECASE)
    zrodlo = open('/usr/share/enigma2/' + config.skin.primary_skin.value, 'r')
    for linia in zrodlo.xreadlines():
        if re.search(wyrazenie, linia) != None:
            return True

    zrodlo.close()
    return False

