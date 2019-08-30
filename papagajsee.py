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

from pynput import keyboard,mouse
import datetime
import pickle
import time
from re import findall
import os
from tkinter import filedialog

def recordPapagaj(endfunction,updateLabels,saveSeqFunc):
    
    def stop(stopfunction=updateLabels):
        listeners["listenerk"].stop()
        listeners["listenerm"].stop()
        stopfunction("Recording finished")
        saveSeqFunc(sequencelist)
        endfunction()

    def sleepafakaprint(lasttimeinput):
        acttime=datetime.datetime.now()
        deltatime = round((acttime - lasttimeinput ).total_seconds(),1)
        if deltatime > 0:
            elxprint(sequencelist,'time.sleep({0})',deltatime)
            lasttimeinput = acttime
        return lasttimeinput

    def elxprint(listToAppend,commandis,elvalue):
        if commandis in ['keyboardx.press({0})', 'keyboardx.release({0})']:
            try:
                try:
                    if elvalue.vk == 0:#elvalue == "<0>" or elvalue.vk == 0
                        raise
                except AttributeError:
                    if str(elvalue) == "<0>":#elvalue == "<0>" or elvalue.vk == 0
                        raise
            except:
                return
                if commandis in ['keyboardx.press({0})',]:
                    print("niektore tlacitko nie je mozne zaznamenat")
                
            strdictElvalue = str(elvalue.__dict__)
            listToAppend["keydirectory"][strdictElvalue] = elvalue
            listToAppend["sequence"].append([commandis,strdictElvalue])
        else:
            listToAppend["sequence"].append([commandis,elvalue])

    def pressed(key):
        if key == datadictionary["pausekeybutton"]:
            if not datadictionary["paused1"]:
                datadictionary["lasttime"] = datetime.datetime.now()
                datadictionary["paused1"], datadictionary["paused2"] = True,True
                updateLabels("Recording paused")
            else:
                datadictionary["paused1"] = False
        elif key == datadictionary["cancelkeybutton"] and datadictionary["paused2"]:
            stop()
        else:
            if datadictionary["paused2"] != True:
                datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
                elxprint(sequencelist,'keyboardx.press({0})',key)

    def released(key):
        if key == datadictionary["pausekeybutton"]:
            if not datadictionary["paused1"] and datadictionary["paused2"]:
                datadictionary["lasttime"] = datetime.datetime.now()
                datadictionary["paused2"] = False

                updateLabels("Recording")
        else:
            if datadictionary["paused2"] != True:
                datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
                elxprint(sequencelist,'keyboardx.release({0})',key)

    def clicked(x, y, button, pressed):
        if datadictionary["paused2"] != True:
            datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
            elxprint(sequencelist,'mousex.position = ({0[0]} ,{0[1]})',(x, y))
            if pressed:
                elxprint(sequencelist,'mousex.press({0})',button)
            else:
                elxprint(sequencelist,'mousex.release({0})',button)  

    def scrolled(x, y, dx, dy):
        if datadictionary["paused2"] != True:
            datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
            elxprint(sequencelist,'mousex.position = ({0[0]} ,{0[1]})',(x, y))
            elxprint(sequencelist,'mousex.scroll({0[0]} ,{0[1]})',(dx,dy*datadictionary["scrollkoeficient"]))

    def moved(x, y):
        if datadictionary["paused2"] != True:
            datadictionary["lasttime"] = sleepafakaprint(datadictionary["lasttime"])
            elxprint(sequencelist,'mousex.position = ({0[0]} ,{0[1]})',(x, y))

    def initialconfig():
        scriptsequence = {
            "sequence":list()
            , "keydirectory":dict()
            }
        datadictionary={
            "lasttime": 0
            ,"paused1": False
            ,"paused2": False
            ,"configfile": 'papagajconfig.pcfg'
            }
        if not os.path.isfile(datadictionary["configfile"]):
            bkpconfig()
        with open(datadictionary["configfile"],'r') as conf:
            dataRaw = conf.read()
        scrollkoeficient = int(findall('scrollkoeficient=<<(.*?)>>',dataRaw)[0])
        if not scrollkoeficient:
            if os.name == "posix":
                scrollkoeficient = 1
            elif os.name == "nt":
                scrollkoeficient = 120
            else:
                scrollkoeficient = 120
        datadictionary["scrollkoeficient"] = scrollkoeficient
        #datadictionary["savekeyboarddictto"] = str(findall('savekeyboarddictto=<<(.*?)>>',dataRaw)[0])
        datadictionary["pausekeybutton"] = eval(findall('pausekeybutton=<<(.*?)>>',dataRaw)[0])
        datadictionary["cancelkeybutton"] = eval(findall('cancelkeybutton=<<(.*?)>>',dataRaw)[0])
        return datadictionary, scriptsequence

    def bkpconfig():
        configbackup ="""
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

scrollkoeficient=<<0>> for windows 120 for linux 1
pausekeybutton=<<keyboard.Key.shift_r>>
cancelkeybutton=<<keyboard.Key.alt>>"""
        with open('papagajconfig.pcfg', 'w') as configbakupfl:
            configbakupfl.write(configbackup)

    def listenersKM():
        listeners = {
            "listenerk":0,
            "listenerm":0
            }
        listeners["listenerk"] = keyboard.Listener(
            on_press = pressed
            , on_release = released
            #,suppress=True
            )
        listeners["listenerk"].start()
        listeners["listenerm"] = mouse.Listener(
            on_move= moved
            , on_click = clicked
            , on_scroll = scrolled
            #,suppress=True
            )
        listeners["listenerm"].start()
        return listeners
            
    def sequenceRun():
        datadict, scrptsequenc = initialconfig()
        datadict["lasttime"] = datetime.datetime.now()
        listeners = listenersKM()
        return datadict, scrptsequenc, listeners

    datadictionary, sequencelist, listeners = sequenceRun()
 

if __name__ == "__main__":

    def saveWpickle(objToSave):
        if not os.path.exists("./Records/"):
            os.makedirs("./Records/", exist_ok=True)
        saveToPath =  filedialog.asksaveasfilename(initialdir = "./Records/"
                                                      ,title = "Save record to File as 'f'"
                                                      ,filetypes = (
                                                          ("papagaj record files","*.ppgj")
                                                          ,("all files","*.*")
                                                          )
                                                 )
        if saveToPath:
            if os.path.dirname(saveToPath):
                os.makedirs(os.path.dirname(saveToPath), exist_ok=True)
            with open(saveToPath, 'wb') as dicty:
                pickle.dump(objToSave, dicty, protocol=pickle.HIGHEST_PROTOCOL)

    recordPapagaj(lambda:print(888),lambda x:print(x),saveWpickle)
    
