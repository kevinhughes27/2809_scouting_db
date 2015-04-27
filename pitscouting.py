#! /usr/bin/env python

import Tkinter
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from PIL import Image, ImageTk
#import numpy
#from numpy import *
import sys
import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()
conn.text_factory = str

c.execute('''CREATE TABLE if not exists pitScouting
            (team, drivetrain, notes)''')

teamPhotosDir = None
rootDir = None
dataDir = None

usePitData = None
pictureBtn = None
openPitFileBtn = None

top = Tk()

def main():
    global usePitData, pictureBtn, openPitFileBtn
    global rootDir, TeamEntry, DriveTrainEntry, NotesEntry

    top.title("2809 Pit-Scouting")
    top.resizable(1, 1)
    top.maxsize(2000, 2000)

    #Frm = Frame(top)

    TeamLbl = Label(top, text="Team:")
    TeamLbl.grid(row=0, column=0, sticky=N+E+W+S)

    TeamEntry = Entry(top)
    TeamEntry.grid(row=1, column=0, sticky=N+E+W+S)

    DrivetrainLbl = Label(top, text="Drivetrain:")
    DrivetrainLbl.grid(row=0, column=1, sticky=N+E+W+S)

    DriveTrainEntry = Entry(top)
    DriveTrainEntry.grid(row=1, column=1, sticky=N+E+W+S)

    NotesLbl = Label(top, text="notes:")
    NotesLbl.grid(row=0, column=2, sticky=N+E+W+S)

    NotesEntry = Entry(top)
    NotesEntry.grid(row=1, column=2, sticky=N+E+W+S)


    #PictureBtn = Button(top, text="Load Picture", command=getPicture)
    #PictureBtn.grid(row=2, column=2, sticky=N+E+W+S)

    DoneBtn = Button(top, text="Enter", command=EnterData)

    DoneBtn.grid(row=2, column=1, sticky=N+E+W+S)

    rootDir = os.getcwd()

    top.mainloop()

'''def getPicture():
    global teamPhotosDir,photoWindow, photoWindowFrame, photoTeamNoEntry, teamPhotoCanvas
    global pitTeamNoLookupTbl

    teamPhotosDir = tkFileDialog.askdirectory(parent=top, title=\
                                            "Which Folder are the team photos in?")

    if teamPhotosDir == '' : return

    # turn the button off as a confirmation
    #pictureBtn.config(state=DISABLED)

    # create a window to display the photos in
    photoWindow = Toplevel()
    photoWindow.title("Team Info & Photo")
    photoWindow.protocol("WM_DELETE_WINDOW", photoWindowClose)
    photoWindow.minsize(TIW_WIDTH, TIW_HEIGHT)
    photoWindow.resizable(0, 0)

    scrollFrame = VerticalScrolledFrame(photoWindow, width=TIW_WIDTH, height=TIW_HEIGHT)
    photoWindowFrame = scrollFrame.interior


    teamPhotoCanvas = Canvas(photoWindowFrame)
    teamPhotoCanvas.grid(row=TIW_PIC_ROW, column=0, sticky=N+E+W+S)


    selectTeamFrame = Frame(photoWindowFrame)
    photoTeamNoEntry = Entry(selectTeamFrame, width=7, justify=CENTER)
    photoTeamNoEntry.insert(0, "team_no")
    photoTeamNoEntry.grid(row=1, column=0, sticky=N+S)
    loadTeamStatsBtn = Button(selectTeamFrame, text="Load Info", command=loadTeamStats)
    loadTeamStatsBtn.grid(row=1, column=1, sticky=N+S)
    Button(selectTeamFrame, text="Prev Pic", command=prevPic).grid(row=0, column=0)
    Button(selectTeamFrame, text="Next Pic", command=nextPic).grid(row=0, column=1)

    photoTeamNoEntry.bind("<Return>", loadTeamStats)

    photoTeamNoEntry.focus_set()

    selectTeamFrame.grid(row=TIW_BUTTONS_ROW, column=0, sticky=N+S)

    teamPhotoNum = 0

    scrollFrame.grid(row=0, column=0)
    scrollFrame.columnconfigure(0, weight=1)
    scrollFrame.rowconfigure(0, weight=1)

    # end makeTeamInfoWindow()
'''
def EnterData():
    TeamNumber = int(TeamEntry.get())
    DriveTrain = str(DriveTrainEntry.get())
    Notes = str(NotesEntry.get())
    row = (TeamNumber,DriveTrain,Notes)
    c.execute('INSERT INTO pitScouting VALUES (?,?,?)', row)
    conn.commit()
    conn.close
    TeamEntry.delete(0, END)
    DriveTrainEntry.delete(0, END)
    NotesEntry.delete(0, END)
    TeamEntry.focus_set()

main()
