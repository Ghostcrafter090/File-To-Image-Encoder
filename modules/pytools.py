import json
import os
import sys
from win32api import GetModuleHandle, PostQuitMessage
import win32con
from win32gui import NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP, NIM_ADD, NIM_DELETE, NIM_MODIFY, WNDCLASS, CreateWindow, DestroyWindow, LoadIcon, LoadImage, RegisterClass, Shell_NotifyIcon, UpdateWindow
import psutil
import ssl
import smtplib
import urllib
from PIL import Image
from PIL import ImageColor
import subprocess
import requests
import random
from io import BytesIO
from urllib.request import urlopen
from datetime import datetime
import ctypes
from bs4 import BeautifulSoup
import glob
import math as mather
import threading
from suntime import Sun
import datetime as dater
from ctypes import *
import zipfile
import shutil
import pickle
import xmltodict
import sounddevice as sd
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
import time
import gtts
import base64

from ctypes.wintypes import *

import encodings
import ctypes
from collections.abc import ByteString
from typing import Tuple, Optional
import locale

class globals:
    class sound:
        soundArray = [[], 0]
        def initializeSoundArray(n):
            i = 0
            while i < n:
                globals.sound.soundArray[0].append('print("system fucky!")')
                i = i + 1
            return 0
    class color:
        ticn = -3
        jsonData = {}

class system:
    def getCPU(wait):
        error = 0
        try:
            temp = 50
            temp = psutil.cpu_percent(float(wait))
        except:
            print("Unexpected error:", sys.exc_info())
            error = 1
        if error != 0:
            temp = error
        return temp

class IO:
    def getJson(path, doPrint=True):
        import traceback
        error = 0
        try:
            file = open(path, "r")
            jsonData = json.loads(file.read())
            file.close()
        except:
            if doPrint:
                print(traceback.format_exc())
                print("Unexpected error:", sys.exc_info())
                print(path)
            error = 1
        if error != 0:
            jsonData = error
        return jsonData
    
    def getXml(path, doPrint=True):
        return xmltodict.parse(IO.getFile(path, doPrint=doPrint))
    
    def saveXml(path, doPrint=True):
        pass

    def saveJson(path, jsonData):
        error = 0
        try:
            file = open(path, "w")
            file.write(json.dumps(jsonData))
            file.close()
        except:
            print("Unexpected error:", sys.exc_info())
            error = 1
        return error

    def getFile(path, doPrint=True):
        error = 0
        try:
            file = open(path, "r")
            jsonData = file.read()
            file.close()
        except:
            if doPrint:
                print("Unexpected error:", sys.exc_info())
            error = 1
        if error != 0:
            jsonData = error
        return jsonData
    
    def getBytes(path, doPrint=True):
        error = 0
        try:
            file = open(path, "rb")
            jsonData = file.read()
            file.close()
        except:
            if doPrint:
                print("Unexpected error:", sys.exc_info())
            error = 1
        if error != 0:
            jsonData = error
        return jsonData
    
    class console:
        STD_OUTPUT_HANDLE = -11
 
        class COORD(Structure):
            pass
 
        COORD._fields_ = [("X", c_short), ("Y", c_short)]
        
        class textUtils:
            def getTextFromRawBytes(buf: bytes, numChars: int, encoding: Optional[str] = None, errorsFallback: str = "replace"):
                """
                Gets a string from a raw bytes object, decoded using the specified L{encoding}.
                In most cases, the bytes object is fetched by passing the raw attribute of a ctypes.c_char-Array to this function.
                If L{encoding} is C{None}, the bytes object is inspected on whether it contains single byte or multi byte characters.
                As a first attempt, the bytes are encoded using the surrogatepass error handler.
                This handler behaves like strict for all encodings without surrogates,
                while making sure that surrogates are properly decoded when using UTF-16.
                If that fails, the exception is logged and the bytes are decoded
                according to the L{errorsFallback} error handler.
                """
                if encoding is None:
                    # If the buffer we got contains any non null characters from numChars to the buffer's end,
                    # the buffer most likely contains multibyte characters.
                    # Note that in theory, it could also be a multibyte character string
                    # with nulls taking up the second half of the string.
                    # Unfortunately, there isn't a good way to detect those cases.
                    if numChars > 1 and any(buf[numChars:]):
                        encoding = "utf_16_le"
                    else:
                        encoding = locale.getpreferredencoding()
                else:
                    encoding = encodings.normalize_encoding(encoding).lower()
                if encoding.startswith("utf_16"):
                    numBytes = numChars * 2
                elif encoding.startswith("utf_32"):
                    numBytes = numChars * 4
                else: # All other encodings are single byte.
                    numBytes = numChars
                rawText: bytes = buf[:numBytes]
                if not any(rawText):
                    # rawText is empty or only contains null characters.
                    # If this is a range with only null characters in it, there's not much we can do about this.
                    return ""
                try:
                    text = rawText.decode(encoding, errors="surrogatepass")
                except UnicodeDecodeError:
                    text = rawText.decode(encoding, errors=errorsFallback)
                return text

        def printAt(c, r, s):
            
            if IO.console.readAt(len(s), c, r) != s:
            
                h = windll.kernel32.GetStdHandle(IO.console.STD_OUTPUT_HANDLE)
                windll.kernel32.SetConsoleCursorPosition(h, IO.console.COORD(c, r))
            
                c = s.encode("windows-1252")
                windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
        
        # wincon tools https://github.com/nvaccess/nvda/blob/master/source/wincon.py
         
        def readAt(length, x, y):
            
            handle = windll.kernel32.GetStdHandle(IO.console.STD_OUTPUT_HANDLE)
            
            # Use a string buffer, as from an unicode buffer, we can't get the raw data.
            buf=create_string_buffer(length * 2)
            numCharsRead=c_int()
            if windll.kernel32.ReadConsoleOutputCharacterW(handle, buf, length, IO.console.COORD(x,y), byref(numCharsRead)) == 0:
                raise WinError()
            return IO.console.textUtils.getTextFromRawBytes(buf.raw, numChars=numCharsRead.value, encoding="utf_16_le")
            
            
    def saveFile(path, jsonData):
        error = 0
        try:
            file = open(path, "w")
            file.write(jsonData)
            file.close()
        except:
            print("Unexpected error:", sys.exc_info())
            error = 1
        return error
    
    def saveBytes(path, jsonData):
        error = 0
        try:
            file = open(path, "wb")
            file.write(jsonData)
            file.close()
        except:
            print("Unexpected error:", sys.exc_info())
            error = 1
        return error

    def saveList(path, list: Array):
        error = 0
        try:
            file = open(path, "wb")
            pickle.dump(list, file)
            file.close()
        except:
            print("Unexpected error:", sys.exc_info())
            error = 1
        return error

    def getList(path, doPrint=True):
        list = []
        error = 0
        try:
            file = open(path, "rb")
            jsonData = pickle.load(file)
            file.close()
        except:
            if doPrint:
                print("Unexpected error:", sys.exc_info())
            error = 1
        if error != 0:
            jsonData = error
        return [list, jsonData]

    def appendFile(path, jsonData):
        error = 0
        try:
            file = open(path, "a")
            file.write(jsonData)
            file.close()
        except:
            print("Unexpected error:", sys.exc_info())
            error = 1
        return error
    
    def unpack(path, outDir):
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                print(zip_ref.printdir())
                print('Extracting zip resources...')
                zip_ref.extractall(outDir)
                print("Done.")
        except Exception as erro:
                print("Could not unpack zip file.")
                print(erro)

    def pack(path, dir):
        shutil.make_archive(path, 'zip', dir)
        


class winAPI:
    def getWallpaper():
        sbuf = ctypes.create_string_buffer(512) # ctypes.c_buffer(512)
        ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_GETDESKWALLPAPER,len(sbuf),sbuf,0)
        return sbuf.value

    def setWallpaper(path):
        changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
        ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER,0,path.encode(),changed) # "".encode() = b""

    class WindowsBalloonTip:
        def __init__(self, title, msg):
            message_map = {
                    win32con.WM_DESTROY: self.OnDestroy,
            }
            # Register the Window class.
            wc = WNDCLASS()
            hinst = wc.hInstance = GetModuleHandle(None)
            wc.lpszClassName = "PythonTaskbar"
            wc.lpfnWndProc = message_map # could also specify a wndproc.
            classAtom = RegisterClass(wc)
            # Create the Window.
            style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
            self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                    0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                    0, 0, hinst, None)
            UpdateWindow(self.hwnd)
            iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            try:
                hicon = LoadImage(hinst, iconPathName, \
                        win32con.IMAGE_ICON, 0, 0, icon_flags)
            except:
                hicon = LoadIcon(0, win32con.IDI_APPLICATION)
                flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
                nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
                Shell_NotifyIcon(NIM_ADD, nid)
                Shell_NotifyIcon(NIM_MODIFY, \
                            (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                            hicon, "Balloon  tooltip",msg,200,title))
                # self.show_balloon(title, msg)
                os.times.sleep(10)
                DestroyWindow(self.hwnd)
        def OnDestroy(self, hwnd, msg, wparam, lparam):
            nid = (self.hwnd, 0)
            Shell_NotifyIcon(NIM_DELETE, nid)
            PostQuitMessage(0) # Terminate the app.

    def balloon_tip(title, msg):
        w=winAPI.WindowsBalloonTip(title, msg)

class color:
    def tempCalc(temp):
        if temp > 298:
            temptype = "hot"
        elif temp > 285:
            temptype = "warm"
        elif temp > 273:
            temptype = "cool"
        elif temp > 263:
            temptype = "cold"
        elif temp <= 263:
            temptype = "freeze"
        else:
            temptype = "warm"
        return temptype

    def saturateRGB(rgb):
        rgbn = [0, 0, 0]
        if rgb[0] > rgb[1]:
            maxRGB = rgb[0]
        else:
            maxRGB = rgb[1]
        if rgb[2] > maxRGB:
            maxRGB = rgb[2]
        if rgb[0] < rgb[1]:
            minRGB = rgb[0]
        else:
            minRGB = rgb[1]
        if rgb[2] < maxRGB:
            minRGB = rgb[2]
        satMult = 255 / maxRGB
        if minRGB == rgb[0]:
            rgbn[0] = int(rgb[0] / satMult)
        elif maxRGB == rgb[0]:
            rgbn[0] = int(rgb[0] * satMult)
        else:
            rgbn[0] = rgb[0]
        if minRGB == rgb[1]:
            rgbn[1] = int(rgb[1] / satMult)
        elif maxRGB == rgb[1]:
            rgbn[1] = int(rgb[1] * satMult)
        else:
            rgbn[1] = rgb[1]
        if minRGB == rgb[2]:
            rgbn[2] = int(rgb[2] / satMult)
        elif maxRGB == rgb[2]:
            rgbn[2] = int(rgb[2] * satMult)
        else:
            rgbn[2] = rgb[2]
        return rgbn

    def getWeatherb(weather):
        weatherb = 0
        if weather == "clear":
            weatherb = 0
        if weather == "fewcloud":
            weatherb = 1000
        if weather == "somecloud":
            weatherb = 2000
        if weather == "cloud":
            weatherb = 3000
        if weather == "rain":
            weatherb = 4000
        if weather == "snow":
            weatherb = 5000
        if weather == "thunder":
            weatherb = 6000
        return weatherb

    def returnSunInfo(clouds):
        jsonData = {
            "x": "-1",
            "y": "-1",
            "z": "-1",
        }
        current = 0
        weatherb = int(clouds) * 77.5
        sunrise = (int(str(Sun(44.766, -63.686).get_local_sunrise_time(dater.date.today())).split(" ")[1].split(":")[0].split("-")[0]) * 60 * 60) + (int(str(Sun(44.766, -63.686).get_local_sunrise_time(dater.date.today())).split(" ")[1].split(":")[1].split("-")[0]) * 60) + (int(str(Sun(44.766, -63.686).get_local_sunrise_time(dater.date.today())).split(" ")[1].split(":")[2].split("-")[0]))
        sunset = (int(str(Sun(44.766, -63.686).get_local_sunset_time(dater.date.today())).split(" ")[1].split(":")[0].split("-")[0]) * 60 * 60) + (int(str(Sun(44.766, -63.686).get_local_sunset_time(dater.date.today())).split(" ")[1].split(":")[1].split("-")[0]) * 60) + (int(str(Sun(44.766, -63.686).get_local_sunset_time(dater.date.today())).split(" ")[1].split(":")[2].split("-")[0]))
        current = (int((str(dater.datetime.now().strftime("%H:%M:%S")).split(":")[0])) * 60 * 60) + (int((str(dater.datetime.now().strftime("%H:%M:%S")).split(":")[1])) * 60) + (int((str(dater.datetime.now().strftime("%H:%M:%S")).split(":")[2])))
        weatherr = (9000 * ((3) ** (-0.0000001 * ((current - sunrise) ** 2)))) + (-1.0002 ** ((-2 * current) + 45000 + (2 * sunrise))) + (9000 * ((3) ** (-0.0000001 * ((current - sunset) ** 2)))) + (-1.0002 ** ((2 * current) + 45000 - (2 * sunset))) + (2300 * ((3) ** (-0.00000005 * ((current - sunset + 3700) ** 2)))) + (2300 * ((3) ** (-0.00000005 * ((current - sunrise - 3700) ** 2))))
        nf = 6000 - weatherr + weatherb
        rgb = color.tempToRGB(nf)
        limit = 1
        limit = (1.0013 ** (current - sunset - (sunset / 80))) + (1.0013 ** -(current - sunrise - (sunrise / 80)))
        if limit < 1:
            limit = 1
        rgb[0] = int(rgb[0] / limit)
        rgb[1] = int(rgb[1] / limit)
        rgb[2] = int(rgb[2] / limit)
        if rgb[0] < 0:
            rgb[0] = 0
        if rgb[0] > 255:
            rgb[0] = 255
        if rgb[1] < 0:
            rgb[1] = 0
        if rgb[1] > 255:
            rgb[1] = 255
        if rgb[2] < 0:
            rgb[2] = 0
        if rgb[2] > 255:
            rgb[2] = 255
        if (jsonData['x'] != str(rgb[0])) or (jsonData['y'] != str(rgb[1])) or (jsonData['z'] != str(rgb[2])):
            jsonData['x'] = str(int(rgb[0]))
            jsonData['y'] = str(int(rgb[1]))
            jsonData['z'] = str(int(rgb[2]))
            print(str(current) + " ::: " + str(jsonData) + ", colorTemp: " + str(nf) + "K" + ", weatherr: " + str(weatherr) + "K" + ", weatherb: " + str(weatherb) + "K")
        return [current, jsonData, nf, weatherr, weatherb]

    def tempToRGB(nf):
        red = 0
        green = 0
        blue = 0
        try:
            if nf < 4483:
                red = int((-1.002 ** -(nf - 2990)) + 309)
            elif nf < 18823:
                red = int((((-4 * (10 ** -11)) * (nf ** 3) + 806) / (0.001 * nf)) + 130)
            else:
                red = int((-1.0004 ** (nf - 14200)) + 165)
        except:
            pass
        try:
            if nf < 6600:
                green = int((-1.0004 ** -(nf - 14200)) + 269)
            elif nf < 17900:
                green = int((((-4 * (10 ** -11)) * (nf ** 3) + 527) / (0.001 * nf)) + 170)
            else:
                green = int((-1.0004 ** (nf - 14200)) + 191)
        except:
            pass
        try:
            if nf < 6424:
                blue = int((-1.0004 ** -(nf - 16400)) + 309)
            else:
                blue = int((-1.0004 ** (nf - 16400)) + 255)
        except:
            pass
        if red < 0:
            red = 0
        if red > 255:
            red = 255
        if green < 0:
            green = 0
        if green > 255:
            green = 255
        if blue < 0:
            blue = 0
        if blue > 255:
            blue = 255
        return [red, green, blue]
    
class calc:
    def subtractLarge(numbera, numberb):
            i = 0
            out = ""
            next = numbera[-(i + 1)]
            while i < len(numbera):
                if numbera[-(i + 1)] != next:
                    math = next - int(numberb[-(i + 1)])
                else:
                    math = int(numbera[-(i + 1)]) - int(numberb[-(i + 1)])
                if math < 0:
                    try:
                        next = int(numbera[-(i + 2)]) - 1
                    except:
                        next = 0 - 1
                    math = math + 10
                else:
                    try:
                        next = int(numbera[-(i + 2)])
                    except:
                        next = 0
                if math < 0:
                    math = 0
                out = str(out) + str(math)
                i = i + 1

    def findLargestPrime(x):
        print("The factors of",x,"are:")
        nonprime = [0]
        i = 1
        exit = 0
        while exit == 0:
            if x % i == 0:
                x = x / i
                n = x
            if i > (n / 2):
                exit = 1
            i = i + 1
        return n

    def addLarge(numbera: str, numberb: str):
        if numbera.find('-') != -1:
            nega = '-'
        else:
            nega = ''
        if numberb.find('-') != -1:
            negb = '-'
        else:
            negb = ''
        numbera = numbera.replace('-', '')
        numberb = numberb.replace('-', '')
        if numbera.find(".") == -1:
            numbera = numbera + ".0"
        if numberb.find(".") == -1:
            numberb = numberb + ".0"
        print(numbera + ";" + numberb)
        decimalloc = calc.findLargestDecimal(numbera, numberb)
        numbera = numbera.replace('.', '')
        numberb = numberb.replace('.', '')
        i = 0
        out = ""
        carry = 0
        while i < len(numbera):
            print(numbera + ";" + numberb)
            math = int(nega + numbera[-(i + 1)]) + int(negb + numberb[-(i + 1)]) + int(carry)
            print(math)
            if math > 9:
                carry = str(math)[0]
                math = str(math)[1]
            else:
                carry = 0
            out = str(out) + str(math)
            i = i + 1
        if int(carry) > 0:
            out = out + str(carry)
        i = 0
        outn = ""
        while i < len(out):
            outn = outn + out[-(i + 1)]
            i = i + 1
        print(decimalloc)
        if outn[1] == '-':
            neg = -1
        else:
            neg = 1
        if neg < 0:
            outf = "-" + (outn[0:mather.floor(decimalloc / 2)] + '.' + outn[mather.floor(decimalloc / 2):len(outn)]).replace('-', '')
            locf = calc.findLargestDecimal(outf, outf)
            if locf != decimalloc:
                print('fuck')
                i = 0
                outl = outf
                while (locf != decimalloc) and (i < len(outl)):
                    try:
                        outf = "-" + (outn[-len(outn):-mather.floor(i / 2)] + '.' + outn[-mather.floor(i / 2):-1] + outn[-1]).replace('-', '')
                        locf = calc.findLargestDecimal(outf, outf)
                    except:
                        pass
                    i = i + 1
                i = 0
                while (locf != decimalloc) and (i < len(outl)):
                    try:
                        outf = "-" + (outn[0:mather.floor(i / 2)] + '.' + outn[mather.floor(i / 2):len(outn)]).replace('-', '')
                        locf = calc.findLargestDecimal(outf, outf)
                    except:
                        pass
                    i = i + 1
        else:
            outf = (outn[-len(outn):-mather.floor(decimalloc / 2)] + '.' + outn[-mather.floor(decimalloc / 2):-1] + outn[-1]).replace('-', '')
            locf = calc.findLargestDecimal(outf, outf)
            if locf != decimalloc:
                print('fuck')
                i = 0
                outl = outf
                while (locf != decimalloc) and (i < len(outl)):
                    try:
                        outf = (outn[0:mather.floor(i / 2)] + '.' + outn[mather.floor(i / 2):len(outn)]).replace('-', '')
                        locf = calc.findLargestDecimal(outf, outf)
                    except:
                        pass
                    i = i + 1
                i = 0
                while (locf != decimalloc) and (i < len(outl)):
                    try:
                        outf = (outn[-len(outn):-mather.floor(i / 2)] + '.' + outn[-mather.floor(i / 2):-1] + outn[-1]).replace('-', '')
                        locf = calc.findLargestDecimal(outf, outf)
                    except:
                        pass
                    i = i + 1
        return outf

    def addLargeInt(numbera: str, numberb: str):
        i = 0
        out = ""
        carry = 0
        while i < len(numbera):
            print(numbera + ";" + numberb)
            math = int(numbera[-(i + 1)]) + int(numberb[-(i + 1)]) + int(carry)
            print(math)
            if math > 9:
                carry = str(math)[0]
                math = str(math)[1]
            else:
                carry = 0
            out = str(out) + str(math)
            i = i + 1
        if int(carry) > 0:
            out = out + str(carry)
        i = 0
        outn = ""
        while i < len(out):
            outn = outn + out[-(i + 1)]
            i = i + 1
        return outn

    def findLargestDecimal(numbera, numberb):
        i = 0
        a = 0
        while i < len(numbera):
            if numbera[-(i + 1)] == '.':
                a = i
            i = i + 1
        i = 0
        b = 0
        while i < len(numberb):
            if numberb[-(i + 1)] == '.':
                b = i
            i = i + 1
        out = a + b
        print(';' + str(out))
        return out

    def multiplyLarge(numbera, numberb):
        i = 0
        outls = []
        if numbera.find(".") == -1:
            numbera = numbera + ".0"
        if numberb.find(".") == -1:
            numberb = numberb + ".0"
        decimalloc = calc.findLargestDecimal(numbera, numberb)
        numbera = numbera.replace('.', '')
        numberb = numberb.replace('.', '')
        while i < len(numberb):
            n = 0
            carry = 0
            outa = ""
            while n < len(numbera):
                math = (int(numbera[-(n + 1)]) * int(numberb[-(i + 1)])) + carry
                if 9 < math:
                    print(math)
                    carry = int(str(math)[0])
                    math = int(str(math)[1])
                else:
                    carry = 0
                outa = outa + str(math)
                n = n + 1
            outa = outa + str(carry)
            f = 0
            outb = ""
            while f < len(outa):
                outb = outb + outa[-(f + 1)]
                f = f + 1
            outls.append(outb)
            i = i + 1
        i = 0
        outn = "0"
        print(outls)
        zero = ""
        while i < len(outls):
            values = calc.equalizeDigits(outn, outls[i] + str(zero))
            outn = calc.addLargeInt(values[0], values[1]).split(".")[0]
            zero = zero + "0"
            print(values)
            i = i + 1
        exit = 0
        i = 0
        while exit == 0:
            if outn[i] != "0":
                sub = i
                exit = 1
            i = i + 1
        return outn[-len(outn):-(decimalloc)] + "." + outn[-(decimalloc):-1] + outn[-1] + "0"

    def equalizeDigits(numbera, numberb):
        if numbera.find('-') != -1:
            nega = '-'
        else:
            nega = ''
        if numberb.find('-') != -1:
            negb = '-'
        else:
            negb = ''
        numbera = numbera.replace('-', '')
        numberb = numberb.replace('-', '')
        if len(numbera.split(".")[0]) < len(numberb.split(".")[0]):
            i = len(numbera.split(".")[0])
            while i < len(numberb.split(".")[0]):
                numbera = "0" + numbera
                i = i + 1
        elif len(numberb.split(".")[0]) < len(numbera.split(".")[0]):
            i = len(numberb.split(".")[0])
            while i < len(numbera.split(".")[0]):
                numberb = "0" + numberb
                i = i + 1
        try:
            if len(numbera.split(".")[1]) < len(numberb.split(".")[1]):
                i = len(numbera.split(".")[1])
                while i < len(numberb.split(".")[1]):
                    numbera = numbera + "0"
                    i = i + 1
            elif len(numberb.split(".")[1]) < len(numbera.split(".")[1]):
                i = len(numberb.split(".")[1])
                while i < len(numbera.split(".")[1]):
                    numberb = numberb + "0"
                    i = i + 1
        except:
            pass
        return [nega + numbera, negb + numberb]
    
    def cleanNumber(number: str):
        i = 0
        while i < len(number):
            if number[i] != "0":
                start = i
                if number[i] == '.':
                    start = i - 1
                i = len(number)
            i = i + 1
        i = 0
        while i < len(number):
            if number[-(i + 1)] != "0":
                end = -(i)
                if number[i] == '.':
                    end = -i + 1
                i = len(number)
            i = i + 1
        print(str(start) + ";" + str(end))
        out = number[start:end]
        if start == 0:
            if end == 0:
                out = number
        return out + "0"

    def mathLargeFloat(numbera: str, arth: str, numberb: str):
        if arth == "+":
            if numbera.find('.') == -1:
                numbera = numbera + ".0"
            if numberb.find('.') == -1:
                numberb = numberb + ".0"
        values = calc.equalizeDigits(numbera, numberb)
        numberan = values[0]
        numberbn = values[1]
        if arth == "+":
            print(numberan + '#' + numberbn)
            outn = calc.addLarge(numberan, numberbn)
        if arth == "-":
            i = 0
            out = ""
            next = numbera[-(i + 1)]
            while i < len(numbera):
                if numbera[-(i + 1)] != next:
                    math = next - int(numberb[-(i + 1)])
                else:
                    math = int(numbera[-(i + 1)]) - int(numberb[-(i + 1)])
                if math < 0:
                    try:
                        next = int(numbera[-(i + 2)]) - 1
                    except:
                        next = 0 - 1
                    math = math + 10
                else:
                    try:
                        next = int(numbera[-(i + 2)])
                    except:
                        next = 0
                if math < 0:
                    math = 0
                out = str(out) + str(math)
                i = i + 1
        if arth == "*":
            outn = calc.multiplyLarge(numbera, numberb)
            # outn = ""
            # while i < len(out):
            #     outn = outn + out[-(i + 1)]
            #     i = i + 1
        print(outn)
        return calc.cleanNumber(outn)

    def abs(num):
        out = num
        if str(num)[0] == '-':
            out = str(num)[1:]
        return out

class net:
    def sendEmail(userEmail, password, toEmail, inputType, messageData, server, port):
        try:
            error = 0
            smtp_server = server
            sender_email = userEmail
            receiver_email = toEmail
            if inputType == 0:
                message = messageData
            elif inputType == 1:
                message = str(IO.getFile(messageData)).encode('ascii', 'ignore')
            else:
                error = 1
                print("Please enter a valid message format, formats are < -text | -file>")
            try:
                if error != 1:
                    context = ssl.create_default_context()
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.ehlo()  # Can be omitted
                        server.starttls(context=context)
                        server.ehlo()  # Can be omitted
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)
                    print("email sent")
                    error = 0
                else:
                    print("email failed to send.")
                    error = 1
            except Exception as err:
                print("email failed to send.")
                print("Email messaging error:", sys.exc_info())
                error = err
        except Exception as err:
            print("Unexpected error:", sys.exc_info())
            error = err
        return error

    def getJsonAPI(url, timeout=10):
        ssl._create_default_https_context = ssl._create_unverified_context
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        response = urlopen(req, timeout=timeout)
        h = response.read()
        data_json = json.loads(h)
        return data_json
    
    def getRawAPI(url, myobj):
        ssl._create_default_https_context = ssl._create_unverified_context
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        response = urlopen(req)
        data_json = response.read()
        return data_json

    def makePostRequest(url, myobj):
        myobj['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        ssl._create_default_https_context = ssl._create_unverified_context
        response = requests.post(url, data = myobj)
        # req = urllib.request.Request(
        #     url, 
        #     data=None, 
        #     headers={
        #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        #     }
        # )
        # response = urlopen(req)
        # data_json = response.read()
        data_json = response.text
        return data_json

    def getTextAPI(url):
        ssl._create_default_https_context = ssl._create_unverified_context
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        response = urlopen(req)
        data_json = BeautifulSoup(response.read(), 'html.parser')
        text = data_json.find_all(text=True)
        data_out = cipher.listToString(text)
        return data_out

    def postAPI(url, node, data, encodeBool):
        ssl._create_default_https_context = ssl._create_unverified_context
        if int(encodeBool) != 0:
            encodedData = cipher.base64_encode(data)
        else:
            encodedData = data
        url = url + "?" + node + "=" + encodedData
        print(url)
        response = urlopen(url)
        data_json = response.read()
        return data_json
    
    def download(urlf, path, maxB):
        i = 0
        n = 0
        local_filename = path
        # NOTE the stream=True parameter below
        with requests.get(urlf, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    i = i + 1
                    f.write(chunk)
                    percent = (n / maxB) * 100
                    print("Download Progress: " + str(int(percent)) + "% ::: iter_bytepos: " + str(n) + " ::: writing file chunk " + str(i) + "...")
                    n = n + 8192
        return local_filename

class cipher:  
    def base64_encode(s, isBytes=False):
        if not isBytes:
            encode = base64.standard_b64encode(bytes(s, encoding="utf-8")).decode("utf-8").replace("=", "?")
        else:
            encode = base64.standard_b64encode(s).decode("utf-8").replace("=", "?")
        return encode
        
    def base64_decode(s: str, isBytes=False):
        if not isBytes:
            decode = base64.standard_b64decode(s.replace("?", "=")).decode("utf-8")
        else:
            decode = base64.standard_b64decode(s.replace("?", "="))
        return decode

    def listToString(s):
        str1 = " "
        return (str1.join(s))

    class tools:
        def removeDuplicateChars(string: str):
            newString = ""
            i = 0
            while i < len(string):
                if newString.find(string[i]) == -1:
                    newString = newString + string[i]
                i = i + 1
            return newString

        def listToString(s):
            str1 = " "
            return (str1.join(s))
    
    class enigma:
        class globals:
            null = ""
            charToNum = {' ': '32', '!': '33', '"': '34', '#': '35', '$': '36', '%': '37', '&': '38', "'": '39', '(': '40', ')': '41', '*': '42', '+': '43', ',': '44', '-': '45', '.': '46', '/': '47', '0': '48', '1': '49', '2': '50', '3': '51', '4': '52', '5': '53', '6': '54', '7': '55', '8': '56', '9': '57', ':': '58', ';': '59', '<': '60', '=': '61', '>': '62', '?': '63', '@': '64', 'A': '65', 'B': '66', 'C': '67', 'D': '68', 'E': '69', 'F': '70', 'G': '71', 'H': '72', 'I': '73', 'J': '74', 'K': '75', 'L': '76', 'M': '77', 'N': '78', 'O': '79', 'P': '80', 'Q': '81', 'R': '82', 'S': '83', 'T': '84', 'U': '85', 'V': '86', 'W': '87', 'X': '88', 'Y': '89', 'Z': '90', '[': '91', '\\': '92', ']': '93', '^': '94', '_': '95', '`': '96', 'a': '97', 'b': '98', 'c': '99', 'd': '100', 'e': '101', 'f': '102', 'g': '103', 'h': '104', 'i': '105', 'j': '106', 'k': '107', 'l': '108', 'm': '109', 'n': '110', 'o': '111', 'p': '112', 'q': '113', 'r': '114', 's': '115', 't': '116', 'u': '117', 'v': '118', 'w': '119', 'x': '120', 'y': '121', 'z': '122', '{': '123', '|': '124', '}': '125', '~': '126'}
            numToChar = {'32': ' ', '33': '!', '34': '"', '35': '#', '36': '$', '37': '%', '38': '&', '39': "'", '40': '(', '41': ')', '42': '*', '43': '+', '44': ',', '45': '-', '46': '.', '47': '/', '48': '0', '49': '1', '50': '2', '51': '3', '52': '4', '53': '5', '54': '6', '55': '7', '56': '8', '57': '9', '58': ':', '59': ';', '60': '<', '61': '=', '62': '>', '63': '?', '64': '@', '65': 'A', '66': 'B', '67': 'C', '68': 'D', '69': 'E', '70': 'F', '71': 'G', '72': 'H', '73': 'I', '74': 'J', '75': 'K', '76': 'L', '77': 'M', '78': 'N', '79': 'O', '80': 'P', '81': 'Q', '82': 'R', '83': 'S', '84': 'T', '85': 'U', '86': 'V', '87': 'W', '88': 'X', '89': 'Y', '90': 'Z', '91': '[', '92': '\\', '93': ']', '94': '^', '95': '_', '96': '`', '97': 'a', '98': 'b', '99': 'c', '100': 'd', '101': 'e', '102': 'f', '103': 'g', '104': 'h', '105': 'i', '106': 'j', '107': 'k', '108': 'l', '109': 'm', '110': 'n', '111': 'o', '112': 'p', '113': 'q', '114': 'r', '115': 's', '116': 't', '117': 'u', '118': 'v', '119': 'w', '120': 'x', '121': 'y', '122': 'z', '123': '{', '124': '|', '125': '}', '126': '~'}

        class enigma:
            salt = 0
            rotors = []
            plugboard = {}
            plugboardRev = {}
            plugboardKey = ""
            plugboardMax = 0
            rotorCount = 0
            class rotor:
                def count():
                    i = 0
                    cipher.enigma.enigma.rotors[0] = cipher.enigma.enigma.rotors[0] + 1
                    while i < 5:
                        if cipher.enigma.enigma.rotors[i] > 95:
                            cipher.enigma.enigma.rotors[i + 1] = cipher.enigma.enigma.rotors[i + 1] + 1
                            cipher.enigma.enigma.rotors[i] = 0
                        i = i + 1

            def init(salt, rotorCount: int, plugboardKey: str):
                cipher.enigma.enigma.plugboardKey = cipher.tools.removeDuplicateChars(plugboardKey)
                i = 0
                cipher.enigma.enigma.rotorCount = rotorCount
                while i < rotorCount:
                    cipher.enigma.enigma.rotors.append(0)
                    i = i + 1
                cipher.enigma.enigma.salt = (salt)
                i = 32
                plugboardMax = 0
                while i < 127:
                    if i < (len(cipher.enigma.enigma.plugboardKey) + 32):
                        cipher.enigma.enigma.plugboard[str(i)] = cipher.enigma.globals.charToNum[cipher.enigma.enigma.plugboardKey[int(i - 32)]]
                        if plugboardMax < int(cipher.enigma.globals.charToNum[str(cipher.enigma.enigma.plugboardKey[int(i - 32)])]):
                            plugboardMax = int(cipher.enigma.globals.charToNum[str(cipher.enigma.enigma.plugboardKey[int(i - 32)])])
                    else:
                        if str(cipher.enigma.enigma.plugboard).find(": \'" + str(i) + "\'") != -1:
                            n = 32
                            exitN = 0
                            while (n < 127) and (exitN != 1):
                                if str(cipher.enigma.enigma.plugboard).find(": \'" + str(n) + "\'") == -1:
                                    cipher.enigma.enigma.plugboard[str(i)] = str(n)
                                    exitN = 1
                                n = n + 1
                        else:
                            cipher.enigma.enigma.plugboard[str(i)] = str(i)

                    i = i + 1
                cipher.enigma.enigma.plugboardMax = plugboardMax
                i = 32
                while i < 127:
                    key = cipher.enigma.enigma.plugboard[str(i)]
                    cipher.enigma.enigma.plugboardRev[key] = str(i)
                    i = i + 1

        def dummy(dum):
            return dum

        class work:
            def encode(string):
                rotorCount = cipher.enigma.enigma.rotorCount
                cipher.enigma.enigma.rotors =  []
                i = 0
                cipher.enigma.enigma.rotorCount = rotorCount
                while i < rotorCount:
                    cipher.enigma.enigma.rotors.append(0)
                    i = i + 1
                i = 0
                new = ""
                newString = ""
                while i < len(string):
                    try:
                        dummy(cipher.enigma.globals.charToNum[string[i]])
                        new = int(cipher.enigma.enigma.plugboard[cipher.enigma.globals.charToNum[string[i]]])
                        n = 0
                        while n < len(cipher.enigma.enigma.rotors):
                            new = new + cipher.enigma.enigma.rotors[n]
                            if new > 126:
                                new = new - 95
                            cipher.enigma.enigma.rotor.count()
                            n = n + 1
                        n = 0
                        while n < len(cipher.enigma.enigma.rotors):
                            new = new + cipher.enigma.enigma.rotors[len(cipher.enigma.enigma.rotors) - (n + 1)]
                            if new > 126:
                                new = new - 95
                            cipher.enigma.enigma.rotor.count()
                            n = n + 1
                        if new > 126:
                            new = new - 95
                        new = cipher.enigma.enigma.plugboard[str(new)]
                        newString = newString + cipher.enigma.globals.numToChar[str(new)]
                    except:
                        newString = newString + string[i]
                    i = i + 1
                return newString
            
            def decode(string):
                rotorCount = cipher.enigma.enigma.rotorCount
                cipher.enigma.enigma.rotors =  []
                i = 0
                cipher.enigma.enigma.rotorCount = rotorCount
                while i < rotorCount:
                    cipher.enigma.enigma.rotors.append(0)
                    i = i + 1
                i = 0
                new = ""
                newString = ""
                while i < len(string):
                    try:
                        dummy(cipher.enigma.globals.charToNum[string[i]])
                        new = int(cipher.enigma.enigma.plugboardRev[cipher.enigma.globals.charToNum[string[i]]])
                        n = 0
                        while n < len(cipher.enigma.enigma.rotors):
                            new = new - cipher.enigma.enigma.rotors[n]
                            if new < 32:
                                new = new + 95
                            cipher.enigma.enigma.rotor.count()
                            n = n + 1
                        n = 0
                        while n < len(cipher.enigma.enigma.rotors):
                            new = new - cipher.enigma.enigma.rotors[len(cipher.enigma.enigma.rotors) - (n + 1)]
                            if new < 32:
                                new = new + 95
                            cipher.enigma.enigma.rotor.count()
                            n = n + 1
                        if new > 126:
                            new = new - 95
                        new = cipher.enigma.enigma.plugboardRev[str(new)]
                        newString = newString + cipher.enigma.globals.numToChar[str(new)]
                    except:
                        newString = newString + string[i]
                    i = i + 1
                return newString

class imageWorker:
    def getRGB(path):
        image_url = path
        resp = requests.get(image_url)
        assert resp.ok
        img = Image.open(BytesIO(resp.content)).convert('RGB')
        img2 = img.resize((1, 1))
        nf = img2.getpixel((0, 0))
        colorrgb = ImageColor.getcolor('#{:02x}{:02x}{:02x}'.format(*nf), "RGB")
        # print('#{:02x}{:02x}{:02x}'.format(*nf))
        return colorrgb

class clock:
    def getDateTime(utc = False):
        if utc:
            daten = datetime.utcnow()
        else:
            daten = datetime.now()
        dateArray = [1970, 1, 1, 0, 0, 0]
        dateArray[0] = int(str(daten).split(" ")[0].split("-")[0])
        dateArray[1] = int(str(daten).split(" ")[0].split("-")[1])
        dateArray[2] = int(str(daten).split(" ")[0].split("-")[2])
        dateArray[3] = int(str(daten).split(" ")[1].split(":")[0])
        dateArray[4] = int(str(daten).split(" ")[1].split(":")[1])
        dateArray[5] = int(str(daten).split(" ")[1].split(":")[2].split(".")[0])
        return dateArray

    def utcFormatToArray(string, seperators="-T:+"):
        year = int(string.split(seperators[0])[0])
        month = int(string.split(seperators[0])[1])
        day = int(string.split(seperators[0])[2].split(seperators[1])[0])
        hour = int(string.split(seperators[1])[1].split(seperators[2])[0])
        minute = int(string.split(seperators[1])[1].split(seperators[2])[1])
        second = int(string.split(seperators[1])[1].split(seperators[2])[2].split(seperators[3])[0])
        millis = 0
        return [year, month, day, hour, minute, second]

    def getTimeDialation():
        staArray = clock.getDateTime()
        utcArray = clock.getDateTime(True)
        diaArray = [0, 0, 0, 0, 0, 0]
        # i = 0
        # while i < len(diaArray):
        #     diaArray[i] = staArray[i] - utcArray[i]
        #     i = i + 1
        diaArray[3] = 24 - (staArray[3] - utcArray[3])
        return diaArray
    
    def getDateArrayFromUST(stamp):
        timef = datetime.fromtimestamp(stamp)
        return [timef.year, timef.month, timef.day, timef.hour, timef.minute, timef.second]

    def fixDateArray(dateArray):
        while dateArray[4] > 60:
            dateArray[4] = dateArray[4] - 60
            dateArray[3] = dateArray[3] + 1
        while dateArray[3] > 24:
            dateArray[3] = dateArray[3] - 24
            dateArray[2] = dateArray[2] + 1
        while dateArray[2] > clock.getMonthEnd(dateArray[1]):
            dateArray[2] = dateArray[2] - clock.getMonthEnd(dateArray[1])
            dateArray[1] = dateArray[1] + 1
        while dateArray[1] > 12:
            dateArray[1] = dateArray[1] - 12
            dateArray[0] = dateArray[0] + 1
        return dateArray

    def solveForDialation(diaArray, staArray):
        outArray = [0, 0, 0, 0, 0, 0]
        xArray = [1, 12, "me", 24, 60, 60]
        i = 0
        while i < len(diaArray):
            outArray[i] = (staArray[i] - diaArray[i])
            i = i + 1
        i = len(outArray) - 1
        while i > 1:
            while outArray[i] < 0:
                    if xArray[i] != "me":
                        outArray[i] = outArray[i] + xArray[i]
                    else:
                        outArray[i] = outArray[i] + clock.getMonthEnd(outArray[1])
                    outArray[i - 1] = outArray[i - 1] - 1
            i = i - 1
        return outArray
    
    def UTCToDateArray(utc):
        
        fourYearFloat = utc / (1461 * 24 * 60 * 60)
        
        dayOfFourYears = (fourYearFloat - mather.floor(fourYearFloat)) * 1461
        
        if dayOfFourYears < 367:
            dayOfYear = dayOfFourYears
            year = mather.floor(fourYearFloat) * 4
        else:
            year = (mather.floor(fourYearFloat) * 4) + 1
            dayOfYear = dayOfFourYears - 366
            while dayOfYear > 365:
                year = year + 1
                dayOfYear = dayOfYear - 365
        
        month = 1
        while (clock.getMonthEnd(month, year) + 1) < dayOfYear:
            dayOfYear = dayOfYear - clock.getMonthEnd(month, year)
            month = month + 1
        day = mather.floor(dayOfYear)
        hour = mather.floor((dayOfYear - day) * 24)
        minute = mather.floor((((dayOfYear - day) * 24) - mather.floor((dayOfYear - day) * 24)) * 60)
        second  = (((((dayOfYear - day) * 24) - mather.floor((dayOfYear - day) * 24)) * 60) - mather.floor((((dayOfYear - day) * 24) - mather.floor((dayOfYear - day) * 24)) * 60)) * 60
        return [int(year), int(month), int(day), int(hour), int(minute), int(second)]

    def getDayOfWeek(dateArray=False):
        if not dateArray:
            out = datetime.today().weekday() + 1
        else:
            out = datetime(*dateArray).weekday() + 1
        if out == 7:
            out = 0
        return out
        
    def getMonthEnd(month, year=False):
        
        if not year:
            year = clock.getDateTime()[0]
        
        mon31 = [12, 10, 8, 7, 5, 3, 1]
        i = 0
        out = 28
        while i < len(mon31):
            if (mon31[i] == month):
                out = 31
            i = i + 1
        if out != 31:
            if month != 2:
                out = 30
        
        if (month == 2) and ((year % 4) == 0):
            out = 29
        
        return out

    def getMidnight(dateArray):
        datef = clock.getMonthEnd(dateArray[1])
        midnight = [dateArray[0], dateArray[1], dateArray[2] + 1, 0, 0, 0]
        if midnight[2] > datef:
            midnight[1] = midnight[1] + 1
            if midnight[1] > 12:
                midnight[1] = 1
                midnight[0] = midnight[0] + 1
        if midnight[2] > clock.getMonthEnd(dateArray[1]):
            midnight[2] = midnight[2] - clock.getMonthEnd(dateArray[1])
            
        return midnight
        
    def dateArrayToUTC(dateArray):
        
        yearsSince0 = clock.getYearDecimal(dateArray)
        
        daysSince0 = (mather.floor(yearsSince0 / 4) * 1461) + clock.getDayOfFourYear(dateArray) + 1
        
        return daysSince0 * 24 * 60 * 60
    
    def getYearUTC():
        utc = clock.dateArrayToUTC(clock.getDateTime())
        start = clock.dateArrayToUTC([clock.getDateTime()[0], 1, 1, 0, 0, 0])
        return utc - start
    
    def getYearDecimal(dateArray):
        day = -1
        month = 1
        while month < dateArray[1]:
            day = day + clock.getMonthEnd(month, year=dateArray[0])
            month = month + 1
        day = day + dateArray[2] + (dateArray[3] / 24) + (dateArray[4] / 24 / 60) + (dateArray[5] / 24 / 60 / 60)
        if (dateArray[0] % 4) == 0:
            return dateArray[0] + (day / 366)
        else:
            return dateArray[0] + (day / 365)
        
    def getDayOfYear(dateArray):
        day = -1
        month = 1
        while month < dateArray[1]:
            day = day + clock.getMonthEnd(month, year=dateArray[0])
            month = month + 1
        day = day + dateArray[2] + (dateArray[3] / 24) + (dateArray[4] / 24 / 60) + (dateArray[5] / 24 / 60 / 60)
        return day
    
    def getDayOfFourYear(dateArray):
        day = -1
        month = 1
        while month < dateArray[1]:
            day = day + clock.getMonthEnd(month, year=dateArray[0])
            month = month + 1
        day = day + dateArray[2] + (dateArray[3] / 24) + (dateArray[4] / 24 / 60) + (dateArray[5] / 24 / 60 / 60)
        
        yearf = mather.floor(dateArray[0] / 4) * 4
        while yearf != dateArray[0]:
            if (yearf % 4) == 0:
                day = day + 366
            else:
                day = day + 365
            yearf = yearf + 1
        
        return day
    
def dummy(*args):
    if args[0] == args[0]:
        pass
    return 0

def dummyf(var):
    pass
    
def runFile(path):
    code = IO.getFile(path)
    out = exec(code)
    return out

def libHelp(self):
    help(self)

if False:
    print("type help(pytools) or pytools.libHelp(pytools) to get more info about the library!")