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


from PIL import ImageGrab,Image
import win32gui,  win32ui,  win32con, win32api
from io import BytesIO
    
"""def makepscreenshot():
    snapshot = ImageGrab.grab()
    return snapshot"""



def makepscreenshot():
    #this module use edited code from link below
    #https://bytes.com/topic/python/answers/576924-win32ui-vs-wxpy-screen-capture-multi-monitor
    hwnd = win32gui.GetDesktopWindow()
    #print (hwnd)
    # you can use this to capture only a specific window
    #l, t, r, b = win32gui.GetWindowRect(hwnd)
    #w = r - l
    #h = b - t
    # get complete virtual screen including all monitors
    SM_XVIRTUALSCREEN = 76
    SM_YVIRTUALSCREEN = 77
    SM_CXVIRTUALSCREEN = 78
    SM_CYVIRTUALSCREEN = 79
    #SM_CMONITORS = 80
    #print (win32api.GetSystemMetrics(SM_CMONITORS))
    w = vscreenwidth = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    h = vscreenheigth = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
    l = vscreenx = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
    t = vscreeny = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
    r = l + w
    b = t + h
    #print( l, t, r, b, ' -> ', w, h)
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (l, t),  win32con.SRCCOPY)
    #saveBitMap.SaveBitmapFile(saveDC,  'screencapture.bmp')
    bmpinfo = saveBitMap.GetInfo()
    #print(bmpinfo)
    bmpstr = saveBitMap.GetBitmapBits(True)
    #'BGRX'
    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw','BGRX' , 0, 1)
    #im.save('screencapture.jpg', format = 'jpeg', quality = 85)
    #im.save('screencapture.png', format = 'png')
    g = BytesIO()
    im.save(g, format = 'PNG')
    saveDC.DeleteDC()
    win32gui.DeleteObject(saveBitMap.GetHandle())
    return g

def showscreenshot(snapshotb):
    snapshot = Image.open(snapshotb)
    return snapshot.show()


if __name__ == "__main__":
    d = makepscreenshot()
    showscreenshot(d)

