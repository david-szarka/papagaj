from os import path
import ctypes
import time
from pynput.mouse import Button
from pynput.keyboard import Key
from pynput import keyboard, mouse
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


# playPapagaj
def playPapagaj(dataAboutPlay,runagain = 0):
    def stop():
        listenerk.stop()
        print("Play finished")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        
    def pressed(key):
        if key == datadictionary["pausekeybutton"]:
            if not datadictionary["paused"]:
                datadictionary["paused"] = 1
                print("Playing paused")
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
            else:
                datadictionary["paused"] = 2
        elif datadictionary["paused"] and key == datadictionary["cancelkeybutton"]:
            datadictionary["kill"] = 1

    def released(key):
        if key == datadictionary["pausekeybutton"]:
            if datadictionary["paused"] == 2:
                datadictionary["paused"] = 0
                print("Playing")
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

    def executeseq(mousex, keyboardx):
        print(f"Completed 0 from {repeatition}")
        for iii in range(repeatition):
            for i in sequence["sequence"]:
                if datadictionary["paused"]:
                    yield None
                if datadictionary["kill"]:
                    yield 1
                if i[0] in ['keyboardx.press({0})', 'keyboardx.release({0})']:
                    exec(i[0].format('sequence["keydirectory"][i[1]]'))
                else:
                    exec(i[0].format(i[1]))
            print(f"Completed {iii + 1} from {repeatition}")
        yield 1

    def initialconfig():
        dataDict = {
            "lasttime": 0
            , "paused": False
            , "kill": False
        }
        dataDict["fileToOpen"] = dataAboutPlay['fileToOpen']
        dataDict["pausekeybutton"] = keyboard.Key.ctrl_r
        cancelbutton = keyboard.Key.alt_r
        dataDict["cancelkeybutton"] = cancelbutton
        return dataDict

    def sequenceRun():
        def recalcspeed(koeffspeed):
            for i, j in enumerate(sequence["sequence"]):
                if "time.sleep(" in j[0]:
                    timesleep = float(j[1])
                    timesleep *= koeffspeed
                    sequence["sequence"][i][1] = timesleep

        def checkCommands():
            checList = {
                'time.sleep({0})'
                , 'keyboardx.press({0})'
                , 'keyboardx.release({0})'
                , 'keyboardx.type({0})'
                , 'mousex.press({0})'
                , 'mousex.release({0})'
                , 'mousex.position = ({0[0]} ,{0[1]})'
                , 'mousex.scroll({0[0]} ,{0[1]})'
            }
            for i, j in enumerate(sequence["sequence"]):
                if j[0] not in checList:
                    raise

        datadictionary = initialconfig()
        sequence = datadictionary["fileToOpen"]
        if not runagain:
            recalcspeed(koeficientspeed)
        checkCommands()
        return datadictionary, sequence

    def makeListenAndControl():
        mousexx = mouse.Controller()
        keyboardxx = keyboard.Controller()
        listenerkxx = keyboard.Listener(
            on_press=pressed
            , on_release=released
        )
        listenerkxx.start()
        listenerkxx.wait()
        return mousexx, keyboardxx, listenerkxx

    def startPlay():
        datadictionary["paused"] = 0
        exeseq = executeseq(mousex, keyboardx)
        while not datadictionary["kill"]:
            time.sleep(0.2)
            if not datadictionary["paused"]:
                endRun = next(exeseq)
                if endRun:
                    exeseq.close()
                    break
                else:
                    continue
        stop()

    repeatition = dataAboutPlay['repeatition']['result']
    koeficientspeed = dataAboutPlay['koeficientspeed']['result']
    datadictionary, sequence = sequenceRun()
    mousex, keyboardx, listenerk = makeListenAndControl()
    print("Play started")
    startPlay()

if __name__ == "__main__":
    import pickle
    from tkinter import filedialog
    import tkinter as tk

    def voteToPlay():
        root = tk.Tk()
        root.withdraw()
        filenameToPlay = tk.filedialog.askopenfilename(initialdir="./Records/"
                                                       , title="Select record to Play"
                                                       , filetypes=(
                ("papagaj record files", "*.ppgj"),
                ("all files", "*.*")
            )
                                                       )
        if filenameToPlay and path.isfile(filenameToPlay):
            return filenameToPlay

    
    def readWpickle(fileSequence):
        if fileSequence is not None:
            with open(fileSequence, 'rb') as pickleFile:
                sequenceData = pickle.load(pickleFile)
            return sequenceData
    
    filee = readWpickle(voteToPlay())
    dataabout={
    'sequence': ['repeatition', 'koeficientspeed'],
    'repeatition': {
        'header': "Number of repetitions",
        'text': """
Enter real number, how many imes you want replay actions, or press enter, default is 1
""",
        'button': "Next",
        'result': ""

    },

    'koeficientspeed': {
        'header': "Speed coefficient",
        'text': """
Enter speedcoefficient, example: 0.5 is 2×faster, or press enter, default is 1
""",
        'button': "Play",
        'result': ""

    },
}
    dataabout['fileToOpen']= filee
    dataabout['repeatition']['result'] = 2
    dataabout['koeficientspeed']['result'] = 0.5
    
    playPapagaj(dataabout) 
