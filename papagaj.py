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

print("""\nWelcome in papagaj, bonded by Dávid Szarka
Loading...""")

import time
import ctypes
import sys
import play
import record
import fileutils
import dataforppgj

ctypes.windll.kernel32.SetConsoleTitleW("papagaj")

def record_func():
    for second in range(6, 0, -1):
        print(f"Start after {second} second")
        time.sleep(1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    new_record = record.recordPapagaj()
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    fileutils.saveWpickle(new_record)


def play_func(data_for_play):
    data_for_play['fileToOpen'] = fileutils.readWpickle(fileutils.voteToPlay())
    if not data_for_play.get('fileToOpen'):
        return
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    for question in data_for_play['sequence']:
        print(data_for_play[question]['header'] + " " + data_for_play[question]['text'], end=" ")
        res = input()
        data_for_play[question]['result'] = data_for_play[question]['checkfunc'](res)
        print(f"{question} is {data_for_play[question]['result']}")
    for second in range(6, 0, -1):
        print(f"Start after {second} second")
        time.sleep(1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    play.playPapagaj(data_for_play)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)


def aboutpapagaj_func():
    info = """
    This software is usable for replay keyboard and mouse actions.
    It is possible replay faster and as many time as you want.
    How use it?
    For pause(or continue) press Right SHIFT.
    For stop press pause(Right SHIFT), then press Left ALT.
    Records have extension .ppgj
    """
    homepage = "https://github.com/david-szarka/papagaj"
    lgpl3license = 'https://www.gnu.org/licenses/lgpl-3.0.en.html'
    print("\npapagaj 1.0.1\nCopyright (C) 2019 Dávid Szarka")
    print(info)
    print("Homepage:", homepage)
    print("License:", lgpl3license)
    input("press Enter")


def exitppgj_func():
    sys.exit()


def playagain_func(data_for_play):
    if not data_for_play.get('fileToOpen'):
        return
    if not data_for_play.get('repeatition'):
        return
    for question in data_for_play['sequence']:
        print(f"{question} is {data_for_play[question]['result']}")
    for second in range(2, 0, -1):
        print(f"Start after {second} second")
        time.sleep(1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    play.playPapagaj(data_for_play, 1)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)


def menu_main(data_for_play):
    rawchoiced_menu_item = ""
    meni_itemdict = data_for_play['menudict']
    while True:
        sorted_keys = sorted(meni_itemdict.keys())
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
        if choiced_menu_item == 1:
            record_func()
        elif choiced_menu_item == 2:
            play_func(data_for_play)
        elif choiced_menu_item == 3:
            playagain_func(data_for_play)
        elif choiced_menu_item == 4:
            aboutpapagaj_func()
        elif choiced_menu_item == 5:
            exitppgj_func()


if __name__ == "__main__":
    menu_main(dataforppgj.dataForPlay)
