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


#import os
import ctypes
from datetime import datetime
from pynput import keyboard, mouse

# recordPapagaj
def recordPapagaj():
    listeners = {
        "listenerk": 0,
        "listenerm": 0
        }
    def stop():
        listeners["listenerk"].stop()
        listeners["listenerm"].stop()
        print("Recording finished")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)

    def sleepafakaprint(lasttimeinput):
        acttime = datetime.now()
        deltatime = round((acttime - lasttimeinput).total_seconds(), 1)
        if deltatime > 0:
            elxprint(sequencelist, 'time.sleep({0})', deltatime)
            lasttimeinput = acttime
        return lasttimeinput

    def elxprint(listToAppend, commandis, elvalue):
        if commandis in ['keyboardx.press({0})', 'keyboardx.release({0})']:
            try:
                try:
                    if elvalue.vk == 0:
                        raise
                except AttributeError:
                    if str(elvalue) == "<0>":
                        raise
            except:
                """if commandis in ['keyboardx.press({0})', ]:
                    print("niektore tlacitko nie je mozne zaznamenat")"""
                return

            strdictElvalue = str(elvalue.__dict__)
            listToAppend["keydirectory"][strdictElvalue] = elvalue
            listToAppend["sequence"].append([commandis, strdictElvalue])
        else:
            listToAppend["sequence"].append([commandis, elvalue])

    def pressed(key):
        if key == datadictionary["pausekeybutton"]:
            if not datadictionary["paused1"]:
                datadictionary["lasttime"] = datetime.now()
                datadictionary["paused1"], datadictionary["paused2"] = True, True
                print("Recording paused")
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)

            else:
                datadictionary["paused1"] = False
        elif key == datadictionary["cancelkeybutton"] and datadictionary["paused2"]:
            stop()
        else:
            if datadictionary["paused2"] != True:
                datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
                elxprint(sequencelist, 'keyboardx.press({0})', key)

    def released(key):
        if key == datadictionary["pausekeybutton"]:
            if not datadictionary["paused1"] and datadictionary["paused2"]:
                datadictionary["lasttime"] = datetime.now()
                datadictionary["paused2"] = False
                print("Recording")
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

        else:
            if datadictionary["paused2"] != True:
                datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
                elxprint(sequencelist, 'keyboardx.release({0})', key)

    def clicked(x, y, button, pressed):
        if datadictionary["paused2"] != True:
            datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
            elxprint(sequencelist, 'mousex.position = ({0[0]} ,{0[1]})', (x, y))
            if pressed:
                elxprint(sequencelist, 'mousex.press({0})', button)
            else:
                elxprint(sequencelist, 'mousex.release({0})', button)

    def scrolled(x, y, dx, dy):
        if datadictionary["paused2"] != True:
            datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
            elxprint(sequencelist, 'mousex.position = ({0[0]} ,{0[1]})', (x, y))
            elxprint(sequencelist, 'mousex.scroll({0[0]} ,{0[1]})', (dx, dy * datadictionary["scrollkoeficient"]))

    def moved(x, y):
        if datadictionary["paused2"] != True:
            datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
            elxprint(sequencelist, 'mousex.position = ({0[0]} ,{0[1]})', (x, y))

    def initialconfig():
        scriptsequence = {
            "sequence": list()
            , "keydirectory": dict()
        }
        elxprint(scriptsequence, 'time.sleep({0})', 0.1)
        datadictionary = {
            "lasttime": 0
            , "paused1": False
            , "paused2": False
        }

        scrollkoeficient = 120
        datadictionary["scrollkoeficient"] = scrollkoeficient
        datadictionary["pausekeybutton"] = keyboard.Key.ctrl_r
        datadictionary["cancelkeybutton"] = keyboard.Key.alt_r
        return datadictionary, scriptsequence

    def listenersRun():
        listeners["listenerk"] = keyboard.Listener(
            on_press=pressed
            , on_release=released
        )
        listeners["listenerk"].start()
        with mouse.Listener(
            on_move=moved,
            on_click=clicked,
            on_scroll=scrolled) as listeners["listenerm"]:
            listeners["listenerm"].join()

    datadictionary, sequencelist = initialconfig()
    datadictionary["lasttime"] = datetime.now()
    print("Record started")
    listenersRun()
    return sequencelist

if __name__ == "__main__":
    print(recordPapagaj())
