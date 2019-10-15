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
from papagaj_packages import customconsole, consolecorrect
"""import customconsole
import consolecorrect"""

customconsole.makedefconsole()
consolecorrect.correctize_console()
ctypes.windll.user32.SetWindowPos(ctypes.windll.kernel32.GetConsoleWindow(),-1,100,200,600,350,0)
ctypes.windll.kernel32.SetConsoleTitleW("papagaj")

from papagaj_packages import play, record, fileutils, dataforppgj, screenshot
import time, sys

"""
import time
import sys
import play
import record
import fileutils
import dataforppgj
import screenshot"""

print("""\nWelcome in papagaj, bonded by Dávid Szarka""")


def record_func():
    print("Selected Record")
    for second in range(6, 0, -1):
        print(f"Start after {second} second")
        time.sleep(1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    new_record = record.recordPapagaj()
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    fileutils.saveWpickle(new_record)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    

def record_func_w_shot():
    print("Selected Record with screenshot")
    for second in range(6, 0, -1):
        print(f"Start after {second} second")
        if second == 6:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
            time.sleep(1)
            shot = screenshot.makepscreenshot()
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        else:
            time.sleep(1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    new_record = record.recordPapagaj()
    new_record['shot'] = shot
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    fileutils.saveWpickle(new_record)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    

def play_func(data_for_play):
    print("Selected Play")
    data_for_play['fileToOpen'] = fileutils.readWpickle(fileutils.voteToPlay())
    if not data_for_play.get('fileToOpen'):
        return
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    print("")
    for question in data_for_play['sequence']:
        print(data_for_play[question]['header'] + " " + data_for_play[question]['text'], end=" ")
        res = input()
        data_for_play[question]['result'] = data_for_play[question]['checkfunc'](res)
        if data_for_play[question]['result'] == None:
            return
        print(f"{question} is {data_for_play[question]['result']}")
    for second in range(6, 0, -1):
        print(f"Start after {second} second")
        time.sleep(1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    play.playPapagaj(data_for_play)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)


def play_func_w_shot(data_for_play):
    print("Selected Play with screenshot")
    data_for_play['fileToOpen'] = fileutils.readWpickle(fileutils.voteToPlay())
    if not data_for_play.get('fileToOpen'):
        return
    if not data_for_play['fileToOpen'].get('shot'):
        print('There is no screenshot')
        return
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    screenshot.showscreenshot(data_for_play['fileToOpen'].get('shot'))
    input("Press Enter to continue")
    print("")
    for question in data_for_play['sequence']:
        print(data_for_play[question]['header'] + " " + data_for_play[question]['text'], end=" ")
        res = input()
        data_for_play[question]['result'] = data_for_play[question]['checkfunc'](res)
        if data_for_play[question]['result'] == None:
            return
        print(f"{question} is {data_for_play[question]['result']}")
    for second in range(6, 0, -1):
        print(f"Start after {second} second")
        time.sleep(1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    play.playPapagaj(data_for_play)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)


def playagain_func(data_for_play):
    print("Selected Play Again")
    if not data_for_play.get('fileToOpen'):
        print("Impossible play again before play first time.")
        return
    if not data_for_play.get('repeatition'):
        print("Impossible play again before play first time.")
        return
    for question in data_for_play['sequence']:
        print(f"{question} is {data_for_play[question]['result']}")
    for second in range(2, 0, -1):
        print(f"Start after {second} second")
        time.sleep(1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    play.playPapagaj(data_for_play, 1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)


def aboutpapagaj_func():
    info = """
    This software record manipulation with mouse and keyboard.
    You can replay record multiple times and run it faster or slower.
    There is option make screenshot before start Recording.
    Then you can see it when choose Play with screenshot.
    During recording and playing:
        For pause(or continue) press Right Ctrl.
        For stop press pause(Right Ctrl), then press Right ALT.
    Take care to set same keyboard language(layout)
    on start Play as it was set on start of Record.
    Records have extension .ppgj
    """
    homepage = "https://github.com/david-szarka/papagaj"
    lgpl3license = 'https://www.gnu.org/licenses/lgpl-3.0.en.html'
    print("\npapagaj_v1.0.6\nCopyright (C) 2019 Dávid Szarka")
    print(info)
    print("Homepage:", homepage)
    print("License:", lgpl3license)
    input("press Enter")


def exitppgj_func():
    print("Exit")
    sys.exit()


def menu_main(data_for_play):
    rawchoiced_menu_item = ""
    meni_itemdict = data_for_play['menudict']
    while True:
        sorted_keys = sorted(meni_itemdict.keys())
        sorted_keys = [*sorted_keys[1:],sorted_keys[0]]
        print("""
MENU:
""")
        for keyx in sorted_keys:
            print(f"{keyx}. {meni_itemdict[keyx]}")
        try:
            print("\nEnter number from menu:", end=" ")
            rawchoiced_menu_item = input().strip()
            print()
            choiced_menu_item = int(rawchoiced_menu_item)
            if choiced_menu_item not in meni_itemdict.keys():
                raise KeyError
        except ValueError:
            print(f"Wrong choice, '{rawchoiced_menu_item}' is not number! Please enter correct number.")
            continue
        except KeyError:
            print(f"Wrong choice, '{rawchoiced_menu_item}' don't exist! Please enter correct number.")
            continue
        if choiced_menu_item == 0:
            exitppgj_func()
        elif choiced_menu_item == 1:
            record_func()
        elif choiced_menu_item == 2:
            play_func(data_for_play)
        elif choiced_menu_item == 3:
            playagain_func(data_for_play)
        elif choiced_menu_item == 4:
            record_func_w_shot()
        elif choiced_menu_item == 5:
            play_func_w_shot(data_for_play)
        elif choiced_menu_item == 6:
            aboutpapagaj_func()

if __name__ == "__main__":
    menu_main(dataforppgj.dataForPlay)
