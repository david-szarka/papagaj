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


import os
import sys
import pickle
import datetime
import time
import threading
from pynput.mouse import Button
from pynput.keyboard import Key
from pynput import keyboard, mouse
import webbrowser as wb
import tkinter as tk
from tkinter import filedialog


# playPapagaj
# recordPapagaj
# main_run

# playPapagaj
def playPapagaj(dataAboutPlay, endfunction, startedfunc, alreadyFinishedRep, updateLabels):
    def stop(stopfunction=endfunction):
        listenerk.stop()
        stopfunction()

    def pressed(key):
        if key == datadictionary["pausekeybutton"]:
            if not datadictionary["paused"]:
                datadictionary["paused"] = 1
                updateLabels("Playing paused")
                app.withdraw()
                app.deiconify()
            else:
                datadictionary["paused"] = 2
        elif datadictionary["paused"] and key == datadictionary["cancelkeybutton"]:
            datadictionary["kill"] = 1

    def released(key):
        if key == datadictionary["pausekeybutton"]:
            if datadictionary["paused"] == 2:
                datadictionary["paused"] = 0
                updateLabels("Playing")
                app.iconify()

    def executeseq(mousex, keyboardx):
        alreadyFinishedRep(0, repeatition, koeficientspeed)
        for iii in range(repeatition):
            for i in sequence["sequence"]:
                if stopAllThread[0]:
                    sys.exit()
                if datadictionary["paused"]:
                    yield None
                if datadictionary["kill"]:
                    yield 1
                if i[0] in ['keyboardx.press({0})', 'keyboardx.release({0})']:
                    exec(i[0].format('sequence["keydirectory"][i[1]]'))
                else:
                    exec(i[0].format(i[1]))
            alreadyFinishedRep(iii + 1, repeatition, koeficientspeed)
        yield 1

    def readWpickle(a):
        with open(a, 'rb') as pickleFile:
            sequenceData = pickle.load(pickleFile)
        return sequenceData

    def initialconfig():
        dataDict = {
            "lasttime": 0
            , "paused": False
            , "kill": False
        }

        dataDict["savekeyboarddictto"] = dataAboutPlay['fileToOpen']
        dataDict["pausekeybutton"] = keyboard.Key.shift_r
        if os.name == "posix":
            cancelbutton = keyboard.Key.alt
        elif os.name == "nt":
            cancelbutton = keyboard.Key.alt_l
        else:
            cancelbutton = keyboard.Key.alt
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
        sequence = readWpickle(datadictionary["savekeyboarddictto"])
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
            if stopAllThread[0]:
                sys.exit()
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
    startedfunc()
    startPlay()


# recordPapagaj
def recordPapagaj(endfunction, updateLabels, saveSeqFunc):
    def stop(stopfunction=updateLabels):
        listeners["listenerk"].stop()
        listeners["listenerm"].stop()
        stopfunction("Recording finished")
        saveSeqFunc(sequencelist)
        endfunction()

    def sleepafakaprint(lasttimeinput):
        acttime = datetime.datetime.now()
        deltatime = round((acttime - lasttimeinput).total_seconds(), 1)
        if deltatime > 0:
            elxprint(sequencelist, 'time.sleep({0})', deltatime)
            lasttimeinput = acttime
        return lasttimeinput

    def elxprint(listToAppend, commandis, elvalue):
        if stopAllThread[0]:
            sys.exit()
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
                datadictionary["lasttime"] = datetime.datetime.now()
                datadictionary["paused1"], datadictionary["paused2"] = True, True
                updateLabels("Recording paused")
                app.withdraw()
                app.deiconify()
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
                datadictionary["lasttime"] = datetime.datetime.now()
                datadictionary["paused2"] = False

                updateLabels("Recording")
                app.iconify()
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

        if os.name == "posix":
            scrollkoeficient = 1
        elif os.name == "nt":
            scrollkoeficient = 120
        else:
            scrollkoeficient = 1

        if os.name == "posix":
            cancelbutton = keyboard.Key.alt
        elif os.name == "nt":
            cancelbutton = keyboard.Key.alt_l
        else:
            cancelbutton = keyboard.Key.alt

        datadictionary["scrollkoeficient"] = scrollkoeficient
        datadictionary["pausekeybutton"] = keyboard.Key.shift_r
        datadictionary["cancelkeybutton"] = cancelbutton
        return datadictionary, scriptsequence

    def listenersKM():
        listeners = {
            "listenerk": 0,
            "listenerm": 0
        }
        listeners["listenerk"] = keyboard.Listener(
            on_press=pressed
            , on_release=released
        )
        listeners["listenerk"].start()
        listeners["listenerm"] = mouse.Listener(
            on_move=moved
            , on_click=clicked
            , on_scroll=scrolled
        )
        listeners["listenerm"].start()
        return listeners

    def sequenceRun():
        datadict, scrptsequenc = initialconfig()
        datadict["lasttime"] = datetime.datetime.now()
        listeners = listenersKM()
        return datadict, scrptsequenc, listeners

    datadictionary, sequencelist, listeners = sequenceRun()


# main_run
class tkwind(tk.Tk):
    def __init__(self, xtitle='papagaj', widthsize=400, heightsize=200, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mainframe = tk.Frame(self)
        self.title(xtitle)
        if os.name == "posix":
            try:
                img = tk.Image("photo", file="papagajicon.png")
                self.tk.call('wm', 'iconphoto', self._w, img)
            except:
                pass
        elif os.name == "nt":
            try:
                self.wm_iconbitmap('papagajicon.ico')
            except:
                pass
        self.attributes("-topmost", True)
        self.mainframe.pack(side="top", fill="both", expand=True)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.minsize(width=widthsize, height=heightsize)
        self.maxsize(width=2 * widthsize, height=4 * heightsize)
        self.configure(width=widthsize, height=heightsize)
        # self.resizable(width=False, height=False)
        wWidth = self.winfo_reqwidth()
        wHeight = self.winfo_reqheight()
        positionH = int(self.winfo_screenwidth() / 2 - int(wWidth) / 2)
        positionV = int(self.winfo_screenheight() / 2 - int(wHeight) / 2)
        self.geometry("{}x{}+{}+{}".format(wWidth, wHeight, positionH, positionV))
        self.update()
        self.mainframe.tkraise()

        def appdestroy(x='dddx'):
            stopAllThread[0] = 1
            app.destroy()
            sys.exit()

        self.protocol("WM_DELETE_WINDOW", appdestroy)

    def addwelcomeframe(self):
        self.welcomeframe = welcomeframe(self.mainframe)
        self.welcomeframe.grid(row=0, column=0, sticky="nsew")

    def addsubframe(self):
        self.sframe = subframe(self.mainframe)
        self.sframe.grid(row=0, column=0, sticky="nsew")

    def addplayFrame(self):
        self.sframe2 = playFrame(self.mainframe)
        self.sframe2.grid(row=0, column=0, sticky="nsew")

    def addrecordFrame(self):
        self.sframe3 = recordFrame(self.mainframe)
        self.sframe3.grid(row=0, column=0, sticky="nsew")

    def addShotcuts(self):
        self.sframe4 = Shotcuts(self.mainframe)
        self.sframe4.grid(row=0, column=0, sticky="nsew")

    def addsubframeAbout(self):
        self.sframeAbout = subframeAbout(self.mainframe)
        self.sframeAbout.grid(row=0, column=0, sticky="nsew")

def addtextwidgettext(self, inputtext):
    self.config(state='normal')
    self.insert('end', inputtext)
    self.config(state='disabled')

def nextx(x):
    return next(x, None)

class subframe(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, **yellowstyle)
        self.initialwin(slx)

    def initialwin(self, mdict):
        xxheader = ''
        xxtext = ''
        xxbutton = ''

        self.label1 = tk.Label(self, text=xxheader, bd=3, bg='#3c404d', fg='white', font=('calibri', 13, 'bold'))
        self.buttonback = tk.Button(self, text="Menu", bd=3, **btn2style)
        self.label2frame = tk.Frame(self)
        self.label2 = tk.Text(self.label2frame, bg='#3c404d', fg='white', wrap='word')
        self.label2.insert('end', xxtext)
        self.label2.config(state='disabled')
        self.yscroll = tk.Scrollbar(self.label2frame)
        self.yscroll.config(command=self.label2.yview)
        self.label2.config(yscrollcommand=self.yscroll.set)
        self.entry1 = tk.Entry(self, bg='white', fg='black')
        self.button = tk.Button(self, text=xxbutton, bd=3, **btn2style)

        self.itersequence = iter(mdict['sequence'])
        self.askfornextanswer(mdict, self.itersequence)
        self.button.config(command=lambda: self.confirmb(mdict, self.itersequence))
        self.buttonback.config(command=lambda: self.destroy())
        self.entry1.bind('<Return>', lambda x: self.confirmb(mdict, self.itersequence))
        self.entry1.focus_set()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.label2frame.grid_columnconfigure(0, weight=1)
        self.label2frame.grid_columnconfigure(1, weight=0)
        self.label2frame.grid_rowconfigure(0, weight=1)
        self.label2frame.grid(row=2, column=1, sticky='nswe')
        self.label1.grid(row=1, column=1, sticky='nswe')
        self.buttonback.grid(row=0, column=1, sticky='nswe')
        self.label2.grid(row=0, column=0, sticky='nswe')
        self.yscroll.grid(row=0, column=1, sticky="ns")
        self.entry1.grid(row=3, column=1, sticky='nswe')
        self.button.grid(row=4, column=1, sticky='nswe')
        self.entry1.focus_set()

    def askfornextanswer(self, askresdict, askitersequence):
        self.actualseq = nextx(askitersequence)
        if self.actualseq is None:
            self.destroy()
            app.addplayFrame()

        else:
            self.label1["text"] = askresdict[self.actualseq]['header']
            addtextwidgettext(self.label2, askresdict[self.actualseq]['text'])
            self.button["text"] = askresdict[self.actualseq]['button']
            self.label2.see('end')

    def confirmb(self, resdict, resitersequence):
        self.answer = self.entry1.get()
        ###it works just if answers must be number !!!
        if not self.answer:
            self.answer = 1
        self.answer = resdict[self.actualseq]['checkfunc'](self.answer)
        resdict[self.actualseq]['result'] = self.answer
        self.entry1.delete(0, 'end')
        self.label2.config(state='normal')
        self.label2.insert('end', '\n' + 'your choice:' + str(self.answer) + '\n')
        self.label2.config(state='disabled')
        self.label2.see('end')
        self.askfornextanswer(resdict, resitersequence)

headerstyle = {"activebackground": '#bada55'
    , "activeforeground": 'red'
    , "font": ('calibri', 14, 'bold')
    , "background": '#3c404d'
    , "foreground": 'white'
    , "wraplength": 380
               }

sfstyle = {"activebackground": '#bada55'
    , "activeforeground": 'red'
    , "font": ('calibri', 12, 'bold')
    , "background": '#3c404d'
    , "foreground": 'white'
    , "wraplength": 380
           }

btn2style = {"activebackground": '#bada55'
    , "activeforeground": 'red'
    , "font": ('calibri', 12, 'bold')
    , "background": '#eebf06'
    , "foreground": '#1a4b8f'
    , "wraplength": 380
             }

stopAllThread = [0]

instructionPapagajRec = instructionPapagajPlay = """For pause(or continue) press Right SHIFT.
For stop press pause(Right SHIFT), then press Left ALT.
"""

class playFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent,bg = sfstyle["background"])
        varints = [8, ]
        label = tk.Label(self, text="Play will start after {}s".format(varints[0]), **headerstyle)
        buttonback = tk.Button(self, text="Menu", bd=3, command=self.destroy, **btn2style)
        labelcnt = tk.Label(self, text=" completed 0 from {}\nspeedcoefficient {}".format(slx['repeatition']['result']
                                                                                          , slx['koeficientspeed'][
                                                                                              'result']
                                                                                          )
                            , **sfstyle, anchor="center")
        label2 = tk.Label(self, text=instructionPapagajPlay, **sfstyle)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        label.grid(row=1, column=0, sticky='nswe')
        buttonback.grid(row=0, column=0, sticky='nswe')
        labelcnt.grid(row=2, column=0, sticky='nswe')
        label2.grid(row=3, column=0, sticky='nswe')

        def startedfunc():
            updLabels("Play", instructionPapagajPlay)
            app.iconify()

        def endfunctFinish():
            updLabels("Finished")
            buttonback = tk.Button(self, text="Menu", bd=3, command=self.destroy, **btn2style)
            buttonback.grid(row=3, column=0, sticky='nswe')
            varints[0] = 1
            self.grid_rowconfigure(4, weight=1)
            label2.grid_forget()
            def playAginFun():
                buttonback.destroy()
                updtime()
            buttonback = tk.Button(self, text="Play again", bd=3, command=playAginFun, **btn2style)
            buttonback.grid(row=4, column=0, sticky='nswe')
            app.withdraw()
            app.deiconify()

        def updateAlreadyFined(x, y, z):
            labelcnt["text"] = " completed {} from {}\nspeedcoefficient {}".format(x, y, z)

        def updLabels(lab=0, lab2=0):
            if lab:
                label["text"] = lab
            if lab2:
                label2["text"] = lab2
                self.update()

        def updtime():
            varints[0] -= 1
            label['text'] = "Play will start after {}s".format(varints[0])
            self.update()
            if varints[0] == 2:
                label2["text"] = "Now don't touch keyboard and mouse\n"
            if varints[0] == 0:
                buttonback.destroy()
                playThread = threading.Thread(target=playPapagaj,
                                              args=(slx, endfunctFinish, startedfunc, updateAlreadyFined, updLabels))
                playThread.start()
                self.update()

            else:
                self.after(1000, updtime)

        updtime()

class recordFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent,bg = sfstyle["background"])
        varint = [8, ]
        label = tk.Label(self, text="Recording will start after {}s".format(varint[0]), **headerstyle)
        buttonback = tk.Button(self, text="Menu", bd=3, command=self.destroy, **btn2style)
        label2 = tk.Label(self, text=instructionPapagajRec, **sfstyle)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        label.grid(row=1, column=0, sticky='nswe')
        buttonback.grid(row=0, column=0, sticky='nswe')
        label2.grid(row=2, column=0, sticky='nswe')

        def updLabels(lab=0, lab2=0):
            if lab:
                label["text"] = lab
            if lab2:
                label2["text"] = lab2

        def updtime():
            nah = "Recording will start after {}s"

            if varint[0] > 0:
                label['text'] = nah.format(varint[0])
            if varint[0] == 2:
                label2["text"] = "Now don't touch keyboard and mouse\n"
            elif varint[0] == 0:
                buttonback.destroy()
                recThread = threading.Thread(target=recordPapagaj, args=(self.destroy, updLabels, saveWpickle))
                recThread.start()
                updLabels("Recording", instructionPapagajRec)
            if varint[0] == 0:
                app.iconify()
            else:
                self.after(1000, updtime)
            varint[0] -= 1
        updtime()

class Shotcuts(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='#3c404d')
        label = tk.Label(self, text="Shotcuts", **sfstyle)
        buttonback = tk.Button(self, text="Menu", bd=3, command=self.destroy, **btn2style)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        label.grid(row=1, column=0, sticky='nswe', padx=(20, 20), pady=(20, 15))
        buttonback.grid(row=0, column=0, sticky='nswe')

        def gitpage():
            wb.open_new_tab('https://github.com/david-szarka/papagaj')

        def homepagedsz():
            wb.open_new_tab('http://davidszarka.pythonanywhere.com/')

        buttongit = tk.Button(self, text="Git - Source code", bd=3, command=gitpage, **btn2style)
        buttonweb = tk.Button(self, text="Homepage", bd=3, command=homepagedsz, **btn2style)
        buttongit.grid(row=3, column=0, sticky='nswe', padx=(20, 20), pady=(15, 15))
        buttonweb.grid(row=2, column=0, sticky='nswe', padx=(20, 20), pady=(15, 15))
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

class subframeAbout(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='#3c404d')
        buttonback = tk.Button(self, text="Menu", bd=3, command=self.destroy, **btn2style)
        labelversion = tk.Label(self, text="papagaj " + versionOfPapagaj + "   license: lgpl-3.0", **sfstyle)
        labelinfo = tk.Text(self, bg='#3c404d', fg='white', wrap='word')
        info = """  This software is usable for replay keyboard and mouse actions.\
It is possible replay faster and as many time as you want.
For pause or continue recording press Right SHIFT.
For stop recording(or playing) press pause (Right SHIFT), then press Left ALT.
Records have extension .ppgj
"""
        labelinfo.insert('end', info)
        labelinfo.config(state='disabled')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        labelversion.grid(row=1, column=0, sticky='nswe', padx=(15, 15), pady=(5, 5))
        labelinfo.grid(row=2, column=0, sticky='nswe', padx=(15, 15), pady=(5, 5))
        buttonback.grid(row=0, column=0, sticky='nswe')

        def lgplpage():
            wb.open_new_tab('https://www.gnu.org/licenses/lgpl-3.0.en.html')

        buttonweb = tk.Button(self, text="lgpl-3.0", bd=3, command=lgplpage, **btn2style)
        buttonweb.grid(row=3, column=0, sticky='nswe')

class welcomeframe(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, **yellowstyle)
        bttnstyle = {"activebackground": '#bada55'
            , "activeforeground": 'red'
            , "font": ('calibri', 14, 'bold')
            , "background": '#3c404d'
            , "foreground": 'white'}

        self.recordbutt = tk.Button(self, text="  Record   ", **bttnstyle)
        self.recordbutt.grid(row=1, column=0, sticky='nswe', padx=(40, 20), pady=(30, 15))
        self.dobutt = tk.Button(self, text="    Play    ", **bttnstyle)
        self.dobutt.grid(row=1, column=1, sticky='nswe', padx=(20, 40), pady=(30, 15))
        self.editbutt = tk.Button(self, text="Homepage", **bttnstyle)
        self.editbutt.grid(row=2, column=0, sticky='nswe', padx=(40, 20), pady=(15, 30))
        self.About = tk.Button(self, text="   About   ", **bttnstyle)
        self.About.grid(row=2, column=1, sticky='nswe', padx=(20, 40), pady=(15, 30))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        def voteToPlay():
            filenameToPlay = tk.filedialog.askopenfilename(initialdir="./Records/"
                                                           , title="Select record to Play"
                                                           , filetypes=(
                    ("papagaj record files", "*.ppgj"),
                    ("all files", "*.*")
                )
                                                           )
            if filenameToPlay and os.path.isfile(filenameToPlay):
                slx['fileToOpen'] = filenameToPlay
                app.addsubframe()

        def voteToRecord():
            app.addrecordFrame()

        self.recordbutt.configure(command=voteToRecord)
        self.dobutt.configure(command=voteToPlay)
        self.editbutt.configure(command=app.addShotcuts)
        self.About.configure(command=app.addsubframeAbout)

def saveWpickle(objToSave):
    if not os.path.exists("./Records/"):
        os.makedirs("./Records/", exist_ok=True)
    saveToPath = tk.filedialog.asksaveasfilename(initialdir="./Records/"
                                                 , title="Save record to File"
                                                 , defaultextension='.ppgj'
                                                 , filetypes=(
            ("papagaj record files", "*.ppgj"),
            # ("all files","*.*")
        )
                                                 )
    if saveToPath:
        if os.path.dirname(saveToPath):
            os.makedirs(os.path.dirname(saveToPath), exist_ok=True)
        with open(saveToPath, 'wb') as dicty:
            pickle.dump(objToSave, dicty, protocol=pickle.HIGHEST_PROTOCOL)

def repeatitionCheck(x):
    try:
        repeatition = int(x)
    except:
        repeatition = 1
    return repeatition

def coefficientCheck(x):
    try:
        koeficientspeed = float(x.replace(",", "."))
    except:
        koeficientspeed = 1
    return koeficientspeed

yellowstyle = {
    "bg": '#eebf06'
}

slx = {
    'sequence': ['repeatition', 'koeficientspeed'],
    'repeatition': {
        'header': "Number of repetitions",
        'text': """
Enter real number, how many imes you want replay actions, or press enter, default is 1
""",
        'button': "Next",
        'result': "",
        'checkfunc': repeatitionCheck
    },

    'koeficientspeed': {
        'header': "Speed coefficient",
        'text': """
Enter speedcoefficient, example: 0.5 is 2×faster, or press enter, default is 1
""",
        'button': "Play",
        'result': "",
        'checkfunc': coefficientCheck
    },
}

versionOfPapagaj = "v0.6.6"
app = tkwind(xtitle='papagaj ' + versionOfPapagaj)
app.addwelcomeframe()
app.mainloop()
sys.exit()
