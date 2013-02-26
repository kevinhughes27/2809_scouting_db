import Tkinter
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from PIL import Image, ImageTk
import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()
teamNumber = int(raw_input('Enter a team number: '))

for row in c.execute('SELECT * FROM pitScouting'):
    if row[0] == teamNumber:
        print row
        top = Tk()
        getPicture()

def getPicture():
    global teamPhotosDir,photoWindow, photoWindowFrame, photoTeamNoEntry, teamPhotoCanvas
    global pitTeamNoLookupTbl
    teamPhotosDir = tkFileDialog.askdirectory(parent=top, title=\
                                            "Which Folder are the team photos in?")
    photoWindow = Toplevel()
    photoWindow.title("Team Photo")
    photoWindow.protocol("WM_DELETE_WINDOW", photoWindowClose)
    photoWindow.minsize(TIW_WIDTH, TIW_HEIGHT)
    photoWindow.resizable(0, 0)
    scrollFrame = VerticalScrolledFrame(photoWindow, width=TIW_WIDTH, height=TIW_HEIGHT)
    photoWindowFrame = scrollFrame.interior


    teamPhotoCanvas = Canvas(photoWindowFrame)
    teamPhotoCanvas.grid(row=TIW_PIC_ROW, column=0, sticky=N+E+W+S)
    scrollFrame.grid(row=0, column=0)
    scrollFrame.columnconfigure(0, weight=1)
    scrollFrame.rowconfigure(0, weight=1)
    


raw_input('press any key to continue...')
