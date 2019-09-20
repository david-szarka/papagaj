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
import tkinter as tk
from tkinter import filedialog
import pickle


def saveWpickle(objToSave):
    if not os.path.exists("./Records/"):
        os.makedirs("./Records/", exist_ok=True)
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
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
    root.destroy()

def voteToPlay():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    filenameToPlay = tk.filedialog.askopenfilename(initialdir="./Records/"
                                                   , title="Select record to Play"
                                                   , filetypes=(
            ("papagaj record files", "*.ppgj"),
            ("all files", "*.*")
        )
                                                   )
    if filenameToPlay and os.path.isfile(filenameToPlay):
        return filenameToPlay
    root.destroy()

def readWpickle(fileSequence):
    if fileSequence is None:
        return None
    else:
        with open(fileSequence, 'rb') as pickleFile:
            sequenceData = pickle.load(pickleFile)
        return sequenceData
