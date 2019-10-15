# coding=utf-8
# papagaj
# Copyright (C) 2019 Dávid Szarka
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import ctypes
from ctypes import *

def makedefconsole():
    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE  = ctypes.windll.kernel32.GetStdHandle(-11)

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]
        
    def getfont():
        fontinfo = CONSOLE_FONT_INFOEX()
        fontinfo.cbSize = sizeof(CONSOLE_FONT_INFOEX)
        ctypes.windll.kernel32.GetCurrentConsoleFontEx(STD_OUTPUT_HANDLE , c_long(False), ctypes.pointer(fontinfo))
        return fontinfo

    fontx = getfont()
    fontx.nFont = 0
    fontx.dwFontSize.X = 8
    fontx.dwFontSize.Y = 18
    fontx.FontFamily = 54
    fontx.FontWeight = 400
    fontx.FaceName = 'Consolas'

    ctypes.windll.kernel32.SetCurrentConsoleFontEx(STD_OUTPUT_HANDLE, ctypes.c_long(False), ctypes.pointer(fontx))

