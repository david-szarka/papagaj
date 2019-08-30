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

from pynput.mouse import Button
from pynput.keyboard import Key
from pynput import keyboard, mouse
import pickle
import time
from re import findall
#import asyncio
import sys

def playPapagaj(dataAboutPlay,endfunction,startedfunc,alreadyFinishedRep,updateLabels):
    def stop(stopfunction=endfunction):
        listenerk.stop()
        stopfunction()

    def pressed(key):
        if key == datadictionary["pausekeybutton"]:
            if not datadictionary["paused"]:
                datadictionary["paused"] = 1
                updateLabels("Playing paused")
            else:
                datadictionary["paused"] = 2
                #updateLabels("Playing")
        elif datadictionary["paused"] and key == datadictionary["cancelkeybutton"]:
            datadictionary["kill"] = 1

    def released(key):
        if key == datadictionary["pausekeybutton"]:
            if datadictionary["paused"]==2:
                datadictionary["paused"] = 0
                updateLabels("Playing")

    def executeseq(a, b, mousex, keyboardx):
        c= b
        for iii in range(a,repeatition):
            for j,i in enumerate(sequence["sequence"][b:]):
                if datadictionary["paused"]:
                    c=b+j
                    return True,a,c
                if datadictionary["kill"]:
                    c=b+j
                    return False,a,c
                if i[0] in ['keyboardx.press({0})', 'keyboardx.release({0})']:
                    exec(i[0].format('sequence["keydirectory"][i[1]]'))
                else:
                    exec(i[0].format(i[1]))
                c= b+j+1
            b=0
            a = iii+1
            alreadyFinishedRep(a,repeatition,koeficientspeed)
        return False,a,c

    def readWpickle(a):
        with open(a, 'rb') as pickleFile:
            sequenceData = pickle.load(pickleFile)
        return sequenceData

    def initialconfig():
        dataDict={
            "lasttime": 0
            , "paused": False
            , "kill": False
            , "alreadyrepeated": 0
            , "alreadyexecuted": 0
            , "configfile": 'papagajconfig.pcfg'
            }

        with open(dataDict["configfile"],'r') as conf:
            dataRaw = conf.read()

        dataDict["savekeyboarddictto"] = dataAboutPlay['fileToOpen']
        dataDict["pausekeybutton"] = eval(findall('pausekeybutton=<<(.*?)>>',dataRaw)[0])
        dataDict["cancelkeybutton"] = eval(findall('cancelkeybutton=<<(.*?)>>',dataRaw)[0])
        return dataDict

    def sequenceRun():
        def recalcspeed(koeffspeed):
            for i,j in enumerate(sequence["sequence"]):
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
            for i,j in enumerate(sequence["sequence"]):
                if j[0] not in checList:
                    raise
                
        datadictionary = initialconfig()
        sequence = readWpickle(datadictionary["savekeyboarddictto"])
        recalcspeed(koeficientspeed)
        checkCommands()
        return datadictionary, sequence

    def makeListenAndControl():
        mousexx = mouse.Controller()
        keyboardxx = keyboard.Controller()
        listenerkxx = keyboard.Listener(
                on_press = pressed
                ,on_release = released
                )
        listenerkxx.start()
        listenerkxx.wait()
        return mousexx, keyboardxx, listenerkxx

    def startPlay():
        datadictionary["paused"] = 0
        while not datadictionary["kill"]:
            time.sleep(0.2)
            if not datadictionary["paused"]:
                endRun \
                , datadictionary["alreadyrepeated"] \
                , datadictionary["alreadyexecuted"] = executeseq(datadictionary["alreadyrepeated"]
                                                                 , datadictionary["alreadyexecuted"]
                                                                 , mousex
                                                                 , keyboardx
                                                                 )
                if endRun:
                    continue
                else:
                    break
        stop()
        """
        async def conor():
            while not datadictionary["kill"]:
                #time.sleep(0.5)
                await asyncio.sleep(0.1)
                if not datadictionary["paused"]:
                    endRun \
                    , datadictionary["alreadyrepeated"] \
                    , datadictionary["alreadyexecuted"] = executeseq(datadictionary["alreadyrepeated"]
                                                                     , datadictionary["alreadyexecuted"]
                                                                     , mousex
                                                                     , keyboardx
                                                                     )
                    if endRun:
                        continue
                    else:
                        break
            stop()

        def run(aw):
            if sys.version_info >= (3, 7):
                return asyncio.run(aw)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(aw())
            finally:
                loop.close()
                asyncio.set_event_loop(None)
        run(conor)
        """

    repeatition = dataAboutPlay['repeatition']['result']
    koeficientspeed = dataAboutPlay['koeficientspeed']['result']
    datadictionary, sequence = sequenceRun()
    mousex, keyboardx, listenerk = makeListenAndControl()
    startedfunc()
    startPlay()

if __name__ == "__main__":
    #test
    datax={'sequence': ['repeatition', 'koeficientspeed']
           , 'repeatition': {'header': 'Number of repetitions'
                             , 'text': "Tis a consummation\nDevoutly to be wished."
                             , 'button': 'Next'
                             , 'result': 2}
            ,  'koeficientspeed': {'header': 'Speed coefficient'
                                   , 'text': 'ha\nHA'
                                   , 'button': 'Play'
                                   , 'result': 2.0}
            , 'fileToOpen': './Records/f.ppgj'}
    playPapagaj(datax,lambda:print('end'),lambda:print('start'),lambda x,v,y: print(x,v,y),lambda b:print(b)) 
 

#keyboard.type("555")
