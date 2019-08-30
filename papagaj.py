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

import tkinter as tk
import os
from papagajsee import recordPapagaj
from papagajdo import playPapagaj
import pickle
import webbrowser as wb
import threading
import sys

#from tkinter import * 
#from tkinter.ttk import * 

class tkwind(tk.Tk):
    def __init__(self, xtitle='papagaj', widthsize = 400, heightsize = 200 , *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mainframe = tk.Frame(self)
        self.title(xtitle)
        self.attributes("-topmost", True)
        self.mainframe.pack(side="top", fill="both", expand=True)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.minsize(width=widthsize, height=heightsize)
        self.maxsize(width=2*widthsize, height=4*heightsize)
        self.configure(width=widthsize, height=heightsize)
        #self.resizable(width=False, height=False)
        wWidth = self.winfo_reqwidth()
        wHeight = self.winfo_reqheight()
        positionH = int(self.winfo_screenwidth()/2 - int(wWidth)/2)
        positionV = int(self.winfo_screenheight()/2 - int(wHeight)/2)
        self.geometry("{}x{}+{}+{}".format(wWidth,wHeight,positionH, positionV))
        self.update()
        self.mainframe.tkraise()

        def appdestroy(x='dddx'):
            app.destroy()
            sys.exit()
        self.protocol("WM_DELETE_WINDOW", appdestroy)
        #self.bind("<Destroy>", appdestroy)

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
    return next(x,None)

class subframe(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent,**yellowstyle)
        self.initialwin(slx)
    def initialwin(self, mdict):
        xxheader=''
        xxtext=''
        xxbutton=''

        self.label1 = tk.Label(self, text=xxheader, bd=3,bg = '#3c404d',fg='white',font = ('calibri', 13, 'bold'))
        self.buttonback = tk.Button(self, text="Menu", bd=3, **btn2style)
        self.label2frame = tk.Frame(self)
        self.label2 = tk.Text(self.label2frame,bg = '#3c404d',fg='white', wrap='word')
        self.label2.insert('end', xxtext)
        self.label2.config(state='disabled')
        self.yscroll= tk.Scrollbar(self.label2frame)
        self.yscroll.config(command=self.label2.yview)
        self.label2.config(yscrollcommand=self.yscroll.set)
        self.entry1 = tk.Entry(self,bg = 'white',fg='black')
        self.button = tk.Button(self, text=xxbutton, bd=3,**btn2style)

        self.itersequence = iter(mdict['sequence'])
        self.askfornextanswer(mdict,self.itersequence)#teraz
        self.button.config(command=lambda: self.confirmb(mdict,self.itersequence))
        self.buttonback.config(command=lambda: self.destroy())
        self.entry1.bind('<Return>', lambda x: self.confirmb(mdict,self.itersequence))

        self.grid_columnconfigure(1,weight=1 )
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.label2frame.grid_columnconfigure(0, weight=1)
        self.label2frame.grid_columnconfigure(1, weight=0)
        self.label2frame.grid_rowconfigure(0, weight=1)

        self.label2frame.grid(row = 2,column=1,sticky='nswe')
        self.label1.grid(row = 1,column=1,sticky='nswe')
        self.buttonback.grid(row = 0,column=1,sticky='nswe')
        self.label2.grid(row = 0,column=0,sticky='nswe')
        self.yscroll.grid(row=0, column=1, sticky="ns")
        self.entry1.grid(row = 3,column=1,sticky='nswe')
        self.button.grid(row = 4,column=1,sticky='nswe')

        self.entry1.focus_set()

    def askfornextanswer(self,askresdict,askitersequence):
        self.actualseq = nextx(askitersequence)
        if self.actualseq is None:
            self.destroy()
            app.addplayFrame()

        else:
            self.label1["text"] = askresdict[self.actualseq]['header']
            addtextwidgettext(self.label2, askresdict[self.actualseq]['text'])
            self.button["text"] = askresdict[self.actualseq]['button']
            self.label2.see('end')

    def confirmb(self,resdict,resitersequence):
        self.answer = self.entry1.get()
        #it works just if answers must be number
        if not self.answer:
            self.answer = 1
        self.answer = resdict[self.actualseq]['checkfunc'](self.answer)
        resdict[self.actualseq]['result']= self.answer
        self.entry1.delete(0,'end')
        self.label2.config(state='normal')
        self.label2.insert('end', '\n' + 'your choice:' + str(self.answer) + '\n')
        self.label2.config(state='disabled')
        self.label2.see('end')
        self.askfornextanswer(resdict, resitersequence)

headerstyle={ "activebackground" : '#bada55'
    ,"activeforeground" : 'red'
    , "font" : ('calibri', 14, 'bold')
    , "background" : '#3c404d'
    , "foreground" : 'white'
    , "wraplength":380
    }

sfstyle={ "activebackground" : '#bada55'
    ,"activeforeground" : 'red'
    , "font" : ('calibri', 12, 'bold')
    , "background" : '#3c404d'
    , "foreground" : 'white'
    , "wraplength":380
          }

btn2style={ "activebackground" : '#bada55'
    ,"activeforeground" : 'red'
    , "font" : ('calibri', 12, 'bold')
    , "background" : '#eebf06'
    , "foreground" : '#1a4b8f'
    , "wraplength":380
          }

instructionPapagaj = """For Pause/Continue press Right SHIFT
For stop,first pause runing and then press Left ALT
"""

class playFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        varints=[8,]
        label = tk.Label( self, text="Play will start after {}s".format(varints[0]), **headerstyle)
        buttonback = tk.Button(self, text="Menu", bd=3, command= self.destroy, **btn2style)
        labelcnt = tk.Label( self, text=" completed 0 from {}\nspeedcoefficient {}".format(slx['repeatition']['result']
                                                                                              ,slx['koeficientspeed']['result']
                                                                                              )
                             , **sfstyle, anchor="center")
        label2 = tk.Label( self, text=instructionPapagaj, **sfstyle)
        self.grid_columnconfigure(0,weight=1 )
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        label.grid(row = 1,column=0,sticky='nswe')
        buttonback.grid(row = 0,column=0,sticky='nswe')
        labelcnt.grid(row = 2,column=0,sticky='nswe')
        label2.grid(row = 3,column=0,sticky='nswe')
        
        def startedfunc():
            label2["text"] = instructionPapagaj
            label['text'] = "Play"
            self.update()
            app.iconify()

        def endfunctFinish():
            label['text'] = "Finished"
            buttonback = tk.Button(self, text="Menu", bd=3, command= self.destroy, **btn2style)
            buttonback.grid(row = 3,column=0,sticky='nswe')
            
        def updateAlreadyFined(x,y,z):
            labelcnt["text"] = " completed {} from {}\nspeedcoefficient {}".format(x,y,z)
            self.update()
        def updtime():
            def updLabels(lab=0, lab2=0):
                if lab:
                    label["text"] = lab
                if lab2:
                    label2["text"] = lab2
                    self.update()
            varints[0] -=1
            label['text'] = "Play will start after {}s".format(varints[0])
            self.update()
            if varints[0] == 2:
                label2["text"] = "Now don't touch keyboard and mouse\n" # + instructionPapagaj
            if varints[0] == 0:
                buttonback.destroy()
                #playPapagaj(slx,endfunctFinish,startedfunc,updateAlreadyFined,updLabels)
                playThread = threading.Thread(target=playPapagaj, args=(slx,endfunctFinish,startedfunc,updateAlreadyFined,updLabels))
                playThread.start()

                self.update()
                """
                #app.withdraw()
                app.iconify()
                #app.wm_state('iconic')
                """
            else:
                self.after(1000,updtime)
        updtime()

class recordFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        varint = [8,]
        label = tk.Label( self, text="Recording will start after {}s".format(varint[0]), **headerstyle)
        buttonback = tk.Button(self, text="Menu", bd=3, command= self.destroy, **btn2style)
        label2 = tk.Label( self, text= instructionPapagaj, **sfstyle)

        self.grid_columnconfigure(0,weight=1 )
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        label.grid(row = 1,column=0,sticky='nswe')
        buttonback.grid(row = 0,column=0,sticky='nswe')
        label2.grid(row = 2,column=0,sticky='nswe')

        def updtime():
            nah = "Recording will start after {}s"
            def updLabels(lab=0, lab2=0):
                if lab:
                    label["text"] = lab
                if lab2:
                    label2["text"] = lab2
            if varint[0] > 0:
                label['text'] = nah.format(varint[0])
            if varint[0] == 2:
                label2["text"] = "Now don't touch keyboard and mouse\n"
            elif varint[0] == 0:
                buttonback.destroy()
                #recordPapagaj(self.destroy, updLabels,saveWpickle)
                recThread = threading.Thread(target=recordPapagaj, args=(self.destroy, updLabels,saveWpickle))
                recThread.start()
                
                label["text"] = "Recording"
                label2["text"] = instructionPapagaj
            if varint[0] == 0:
                app.iconify()
            else:
                self.after(1000,updtime)
            varint[0]-=1
        updtime()

class Shotcuts(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg= '#3c404d')
        label = tk.Label( self, text="Shotcuts", **sfstyle)
        buttonback = tk.Button(self, text="Menu", bd=3, command= self.destroy, **btn2style)
        self.grid_columnconfigure(0,weight=1 )
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        label.grid(row = 1,column=0,sticky='nswe',padx=(20, 20),pady=(20, 15))
        buttonback.grid(row = 0,column=0,sticky='nswe')

        def gitpage():
            wb.open_new_tab('https://github.com/david-szarka/papagaj')

        def homepagedsz():
            wb.open_new_tab('http://davidszarka.pythonanywhere.com/')
            
        buttongit = tk.Button(self, text="Git - Source code", bd=3, command= gitpage, **btn2style)
        buttonweb = tk.Button(self, text="Homepage", bd=3, command= homepagedsz, **btn2style)
        buttongit.grid(row = 3,column=0,sticky='nswe',padx=(20, 20),pady=(15, 15))
        buttonweb.grid(row = 2,column=0,sticky='nswe',padx=(20, 20),pady=(15, 15))
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        

class subframeAbout(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg= '#3c404d')
        buttonback = tk.Button(self, text="Menu", bd=3, command= self.destroy, **btn2style)
        labelversion = tk.Label( self, text="papagaj v0.6\nlicense: lgpl-3.0", **sfstyle)
        labelinfo = tk.Text(self,bg = '#3c404d',fg='white', wrap='word')
        info = """This software is usable for replay keyboard and mouse actions,\
 it is possible replay faster and as many time as you want.
"""
        labelinfo.insert('end', info)
        labelinfo.config(state='disabled')
        self.grid_columnconfigure(0,weight=1 )
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        

        labelversion.grid(row = 1,column=0,sticky='nswe',padx=(15, 15),pady=(5, 5))
        labelinfo.grid(row = 2,column=0,sticky='nswe',padx=(15, 15),pady=(5, 5))
        buttonback.grid(row = 0,column=0,sticky='nswe')

        def lgplpage():
            wb.open_new_tab('https://www.gnu.org/licenses/lgpl-3.0.en.html')
        buttonweb = tk.Button(self, text="lgpl-3.0", bd=3, command= lgplpage, **btn2style)
        buttonweb.grid(row = 3,column=0,sticky='nswe')
        """buttongit = tk.Button(self, text="Git", bd=3, command= gitpage, **btn2style)
        buttonweb = tk.Button(self, text="Homepage", bd=3, command= gitpage, **btn2style)
        buttongit.grid(row = 3,column=0,sticky='nswe',padx=(20, 20),pady=(15, 15))
        buttonweb.grid(row = 2,column=0,sticky='nswe',padx=(20, 20),pady=(15, 15))
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)"""


class welcomeframe(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, **yellowstyle)

        bttnstyle={ "activebackground" : '#bada55'
            ,"activeforeground" : 'red'
            , "font" : ('calibri', 14, 'bold')
            , "background" : '#3c404d'
            , "foreground" : 'white'}
        
        self.recordbutt = tk.Button(self, text="  Record   ", **bttnstyle)
        self.recordbutt.grid(row=1,column=0,sticky='nswe',padx =(40, 20),pady=(30, 15))
        self.dobutt = tk.Button(self, text="    Play    ", **bttnstyle)
        self.dobutt.grid(row=1,column=1,sticky='nswe',padx=(20, 40),pady=(30, 15))
        self.editbutt  = tk.Button(self, text="Homepage", **bttnstyle)
        self.editbutt.grid(row=2,column=0,sticky='nswe',padx=(40, 20),pady=(15, 30))
        self.About = tk.Button(self, text="   About   ", **bttnstyle)
        self.About.grid(row=2,column=1,sticky='nswe',padx=(20, 40),pady=(15, 30))
        self.grid_columnconfigure(0,weight=1 )
        self.grid_columnconfigure(1,weight=1 )
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        def voteToPlay():
            filenameToPlay =  tk.filedialog.askopenfilename(initialdir = "./Records/"
                                                        ,title = "Select record to Play"
                                                        ,filetypes = (
                                                            ("papagaj record files","*.ppgj")
                                                            ,("all files","*.*")
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
    saveToPath =  tk.filedialog.asksaveasfilename(initialdir = "./Records/"
                                                  ,title = "Save record to File"
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

def repeatitionCheck(x):
    try:
        repeatition = int(x)
    except:
        repeatition = 1
    return repeatition

def coefficientCheck(x):
    try:
        koeficientspeed = float(x.replace(",","."))
    except:
        koeficientspeed = 1
    return koeficientspeed

yellowstyle = { 
    "bg" : '#eebf06'
    }

slx = {
    'sequence':['repeatition','koeficientspeed'],
    'repeatition':{
        'header':"Number of repetitions",
        'text':"""
Enter real number, how many imes you want replay actions, or press enter, default is 1
""",
        'button':"Next",
        'result':"",
        'checkfunc':repeatitionCheck
        },

    'koeficientspeed':{
        'header':"Speed coefficient",
        'text':"""
Enter speedcoefficient, example: 0.5 is 2×faster, or press enter, default is 1
""",
        'button':"Play",
        'result':"",
        'checkfunc':coefficientCheck
        },
    }

app = tkwind(xtitle = 'papagaj')
app.addwelcomeframe()
app.mainloop()
