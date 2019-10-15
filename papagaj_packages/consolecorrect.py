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


from ctypes import byref
from ctypes import windll as windll
from ctypes.wintypes import DWORD, HANDLE


def GetStdHandle(nStdHandle):
    hConsoleHandle = windll.kernel32.GetStdHandle(nStdHandle)
    return HANDLE(hConsoleHandle)


def GetConsoleMode(nStdHandle):
    dwMode = DWORD(0)    
    hConsoleHandle = GetStdHandle(nStdHandle)
    windll.kernel32.GetConsoleMode(hConsoleHandle, byref(dwMode))
    return dwMode


def SetConsoleMode(dwMode, hConsoleHandle):
    windll.kernel32.SetConsoleMode(hConsoleHandle, dwMode)


def correctize_console():
    SetConsoleMode(439, GetStdHandle(-10))


if __name__ == "__main__":
    input("123")
    correctize_console()
    input()


