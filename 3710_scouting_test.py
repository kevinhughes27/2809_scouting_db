############################################################
# Pick List Generator and Scouting Tool.
#
# Written by Mike Ounsworth for FIRST Robotics Team 3710
# Cyber Falcons, Frontenac Secondary School, Kingston, On.
# Last modified: Oct. 8, 2011
#
# Copyright (C) 2011
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License which can be
#    found at <http://www.gnu.org/licenses/>.
#
# Runs with python 2.6
###########################################################

import Tkinter
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from PIL import Image, ImageTk
import numpy
from numpy import *


############################################################
# Before running, INSTALL :
# - python 2.7 idle (forces python & tk)
# - Python Imaging Library
# - NumPy (Numerical Python, lin alg for OPR calculations)
###########################################################


# The main data structure. Structure is matchDatabase[teamNo][matchNo][task]
matchDatabase = []

matchDataColHeaders = []
pitDataColHeaders = []

# format pitDatabase[teamNo][feature]
pitDatabase = []

# holds the maximum value we saw in each column (used for normalizing)
matchColMaxes = []

# assigns a squential integer to each team number based on the order which they appeared 
# in the input file. Use hashTbl.index(teamNo) to get the hash value
matchTeamNoLookupTbl = []
pitTeamNoLookupTbl = []

# GUI related global variables
taskWeights = []
taskUse = []
taskAllNone = None
ignoreList = []
pitSelectListbox = None
pitSelectAndOr = None
usePitData = False
useMatchScoutingData = False
teamStatsFrame = None
useMatchResultsData = False
compareTeamsNum = 0
teamPhotoNum = 0
photoList = []
photoDir = ''
teamList = []
teamOPR = []
teamScheduleToughness = []

# directory where the team photos are held
teamPhotosDir = None
rootDir = None
dataDir = None

# some Tkinter components that need to be globals
matchResultsFrm = None
scoutingFrm = None
noTeamsEntrybox = None
gameElemFrame = None
photosBtn = None
photoWindow = None
photoWindowFrame = None
photoTeamNoEntry = None
teamPhotoCanvas = None
ignoreListBtn = None
genListBtn = None
ignoreListWindow = None
ignoreListEntry = None
howManyTeamsFrame = None
fileNotFoundLbl = None
pitElemFrame = None
gameElemFrame = None
openMatchResultsBtn = None
openMatchFileBtn = None
openPitFileBtn = None
matchResultsFrm = None
compareTeamsBtn = None
OPR_ToughnessFrame = None
compareTeamsWindow = None
compareTeamsFrm = None
compareTeamNoEntry = None
loadedPic = None

top = Tk()
        

def main() :
    global usePitData, photosBtn, openMatchResultsBtn, openMatchFileBtn, openPitFileBtn
    global matchResultsFrm, scoutingFrm
    global rootDir
    
    top.title("3710 Pick List Generator")
    top.resizable(1, 1)
    top.maxsize(2000,2000)
    
    matchResultsFrm = Frame(top)
    
    matchResultsDataLbl = Label(matchResultsFrm, text="Match Results")
    matchResultsDataLbl.grid(row=0, column=0, sticky=N+E+W+S)
    
    openMatchResultsBtn = Button(matchResultsFrm, text="Load Results Data",\
                                 command=loadmatchResultsDataFile)
    openMatchResultsBtn.grid(row=1, column=0, sticky=N+S)
    
    matchResultsFrm.grid(row=0, column=0, sticky=N+E+W+S)
        
    
    scoutingFrm = Frame(top)
    matchDataLbl = Label(scoutingFrm, text="Scouting Data")
    matchDataLbl.grid(row=0, column=0, sticky=N+E+W+S)
        
    openMatchFileBtn = Button(scoutingFrm, text="Load Match Data",\
                                        command=loadMatchScoutingFile)
    openMatchFileBtn.grid(row=1, column=0, sticky=N+E+W+S)
        

    pitDataLbl = Label(scoutingFrm, text="Pit Data")
    pitDataLbl.grid(row=0, column=1, sticky=N+E+W+S)

    openPitFileBtn = Button(scoutingFrm, text="Load Pit Data", command=loadPitFile)
    openPitFileBtn.grid(row=1, column=1, sticky=N+E+W+S)
    
    ckbxVar = StringVar(scoutingFrm)
    ckbxVar.set('0')
    
    photosBtn = Button(top, text="Team Info & Photo", command=makeTeamInfoWindow)
    photosBtn.grid(row=3, column=1, sticky=N+S)
    
    scoutingFrm.grid(row=0, column=1, sticky=N+E+W+S)
    
    rootDir = os.getcwd()
    
    top.mainloop()
    # end main()


# takes a team number and calculates their average score in each task based 
# on all their matches. It also normalizes the data by dividing by the highest
# value that any team got in that column
def averageCols(teamIdx) :
    global matchColMaxes
    
    calcColMaxes()
    
    # make a list of the column averages across all their matches
    averageStats = []
    for task in range(0, len(matchDatabase[teamIdx][0])-1) :
        averageStats.append(0)
        
        # look at that column across all matches
        numberOfMatches = 0
        for match in matchDatabase[teamIdx] :
            if match[task+1] != None :
                averageStats[task] = averageStats[task] + match[task+1]
                numberOfMatches = numberOfMatches + 1

        # average the column and force it to be a floating point number
        if numberOfMatches == 0 :
            averageStats[task] = None
        else:
            averageStats[task] = averageStats[task] / float(numberOfMatches)
        
            # normalize it, it's already a float from above
            if matchColMaxes[task] == 0 :
                averageStats[task] = 0
            else:
                averageStats[task] = averageStats[task] / matchColMaxes[task]
        # end if
        # end for
        
    return averageStats
    # end averageCols()
    

def bothFilesAreLoaded() :
    return (useMatchScoutingData and usePitData)


# walks through the database and finds the maximum entry in each column
def calcColMaxes() :
    global matchColMaxes
    
    matchColMaxes = []
    
    for task in range(0, len(matchDatabase[0][0])) :
        colMax = matchDatabase[0][0][task]
        
        for team in range(0, len(matchDatabase)) :
            for match in matchDatabase[team] :
                if (match[task] != None) :
                    if colMax == None or match[task] > colMax :
                        colMax = match[task]
                
        matchColMaxes.append(colMax)
    # end calcColMaxes()


# This checks to make sure that all teams that appear in one file also appear in the other,
# if not it will pop up a dialog box warning the user"""
def checkFilesMatch() :
    
    # only run this check if both files have been loaded
    if not bothFilesAreLoaded() :
        return
        
    errorTeams = ""

    foundInMatch = False
    matchErrorTeams = ""
    for teamNo in matchTeamNoLookupTbl : 
        if pitTeamNoLookupTbl.count(teamNo) == 0 :
            matchErrorTeams = matchErrorTeams + "{0:d}\n".format(teamNo)
            foundInMatch = True
    if foundInMatch :
        errorTeams = "Appears in\nMatch Data\n" + matchErrorTeams

    foundInPit = False
    pitErrorTeams = ""
    for teamNo in pitTeamNoLookupTbl :
        if matchTeamNoLookupTbl.count(teamNo) == 0 :
            pitErrorTeams = pitErrorTeams + "{0:d}\n".format(teamNo)
            foundInPit = True
    if foundInPit :
        errorTeams += "\nAppears in\nPit Data\n" + pitErrorTeams

    if errorTeams != "" :
        errorMsg = "Warning: The following team(s)\n"+\
                    "appear in one of the data files\n"+\
                    "but not the other:"
        scrollDialog(title="Missing Data!", warning=errorMsg, messageList=errorTeams)
    #end checkFilesMatch()
    
    
def checkNoTeamsBox() :
    try:
        int( noTeamsEntrybox.get() )
    except ValueError :
        trollfaceDialog("The number of teams has to be, uhh, a number.")
    
# make sure the user entered a number
def checkWeightsboxes() :
    for box in taskWeights :
        try:
            int( box.get() )
        except ValueError :
            trollfaceDialog(message="Weights have to be whole numbers.")     
    # end checkWeightsboxes()
    
    
def displayPickList(rankingScores) :
    
    # this list will store the pick list so we can reference it later (ie save it
    # to file.
    pickList = []
    
    # create a new window
    pickListWindow = Toplevel(top)
    pickListWindow.transient(top)
    pickListWindow.title("Pick List")
    pickListWindow.resizable(0, 0)
    
    pickListfrm = Frame(pickListWindow)
    
    # display the pick list
    pos = 1
    maxRS = 0 # used to display heat
    minRS = 0
    try:
        (teamNo, RS) = rankingScores[0]
        tmpLbl = Label(pickListfrm, text="{0:d}) {1:d}".format(pos,teamNo), \
                          justify=LEFT)
        tmpLbl.grid(row=1, column=0, sticky=N+E+W+S)
        
        maxRS = minRS = RS

        Label(pickListfrm, text="Team").grid(row=0, column=0, sticky=N+E+W+S)
        Label(pickListfrm, text="Ranking").grid(row=0, column=1, sticky=N+E+W+S)
        Label(pickListfrm, text="Score").grid(row=0, column=2, sticky=N+E+W+S)
        
        pickList.append(teamNo)
        
        # display the RS
        tmpLbl = Label(pickListfrm, text="{0:.2f}".format(RS), justify=LEFT)
        tmpLbl.grid(row=1, column=2, sticky=N+E+W+S)
    except IndexError:
        # this means that no teams made it past the pit filter
        tmpLbl = Label(pickListfrm, text="This list contains no teams.", \
                          justify=LEFT)
        tmpLbl.grid(row=1, column=0, sticky=N+E+W+S) 

    for (teamNo, RS) in rankingScores[1:] :
        pos = pos + 1
        if pos > int(noTeamsEntrybox.get()) : break
        tmpLbl = Label(pickListfrm, text="{0:d}) {1:d}".format(pos,teamNo), \
                          justify=LEFT)
        tmpLbl.grid(row=pos, column=0, sticky=N+E+W+S)
        
        if RS > maxRS :
            maxRS = RS
        if RS < minRS :
            minRS = RS
            
        pickList.append(teamNo)
        
        
        # display the RS
        tmpLbl = Label(pickListfrm, text="{0:.2f}".format(RS), justify=LEFT)
        tmpLbl.grid(row=pos, column=2, sticky=N+E+W+S)
        
    
    # display the heat boxes (RS represented as a colour in the red<->blue gradient)
    pos = 0
    for (teamNo, RS) in rankingScores :
        pos = pos + 1
        if pos > int(noTeamsEntrybox.get()) : break
        
        # calculate the colour
        try:
            red = int((RS - minRS) / (maxRS - minRS) * 255)
        except ZeroDivisionError :
            red = 0
        if red < 0 : red = 0
        blue = 255 - red
        
        colour = "#{0:02x}00{1:02x}".format(red, blue)
        
        tmpLbl = Label(pickListfrm, height=1, width=3, background=colour)
        tmpLbl.grid(row=pos, column=1,  padx=15, sticky=N+E+W+S)
        
    pickListfrm.grid(row=1, column=0, sticky=N+E+W+S)
    
    tmpEntryBox = Entry(pickListWindow, width=10, justify=CENTER)
    tmpEntryBox.insert(0,"List_Name")
    tmpEntryBox.grid(row=0, column=0)

    saveListButton = Button(pickListWindow, text="Save to File")

    # This is a nested function, that's right savePickList() is INSIDE
    # displayPickList(). It has implications for scope of variables.
    def savePickList(event) :
        try:
            fileName = tkFileDialog.asksaveasfilename\
            (parent=pickListWindow,filetypes=[('Text','*.txt')],\
            title="Save the picklist as...")
        except TypeError :
            return

        try :
            pickListFile = open(fileName, 'w')
        except IOError :
            return
        except TypeError :
            return

        for teamNo in pickList :
            pickListFile.write(str(teamNo)+ "\n")

        pickListFile.close()
        pickListWindow.title(os.path.basename(fileName)[:-4])
        #end savePickList()

    saveListButton.bind("<Button-1>", savePickList)
    saveListButton.grid(row=2, column=0, sticky=N+S)
    # end displayPickList()
    

# the event handler for the GenerateList button
def generateList() :
    global taskUse
    
    checkWeightsboxes()
    checkNoTeamsBox()
     
    
    # calculate the ranking score for each team
    rankingScores = []
    for teamIdx in range(0, len(matchDatabase)) :
        # if they've been filtered out by the pit data selector then we skip them
        if not pitFilter(matchTeamNoLookupTbl[teamIdx]): continue
        
        # if they've been filtered out by the ignore list then we skip them
        if ignoreList.count(matchTeamNoLookupTbl[teamIdx]) != 0: continue
    
        # average each task across all matches they played
        aveTaskScores = averageCols(teamIdx)
        
        # calculate Ranking Score
        RS = 0
        for task in range(0, len(aveTaskScores)) :
            if taskUse[task].get() :
                weight = int(taskWeights[task].get())
            else : weight = 0
                
            if aveTaskScores[task] != None :
                RS = RS + (aveTaskScores[task] * weight)
            

        # update the list of tuples of the form (teamNo, RankingScore)
        # we don't acutally know the team number, only which line in the database
        # we're on, so we'll need to look that up.
        rankingScores.append( (matchTeamNoLookupTbl[teamIdx], RS ))
        
    # sort them by ranking score, highest to lowest
    #rankingScores = RSsort(rankingScores)
        rankingScores.sort(key=lambda x: x[1])
        rankingScores.reverse()
    
    # make a popup window that displays the calculated list
    displayPickList(rankingScores)
    # end generateList()


def ignoreListUpdate() :
    global ignoreList, matchDatabase
    
    ignoreList = []
    newList = ignoreListEntry.get()
    
    newList = newList.split(',')
    
    strInvalid = ""
    
    for i in range(0,len(newList)) :
        # remove whitespace
        newList[i] = newList[i].strip()
        
        
        # clean the input
        
        if newList[i] == "" : continue
        
        if not (newList[i].isdigit()) :
            # if it's not an int then clean it up
            newStr = ""
            for s in newList[i] :
                if s.isdigit() : newStr += s
            newList[i] = newStr
                
            # if there were no numbers then skip
            if newStr == "" : continue
        
        # check for duplicates
        flag = False
        for team in newList[0:i] :
            if team == newList[i] : 
                flag = True
        
                
        # make sure it's a valid team number
        if matchTeamNoLookupTbl.count(int(newList[i])) == 0 :
            flag = True
            strInvalid += newList[i] + "\n"
        
        if flag : continue
        
        # it passed all the tests --> copy it over
        ignoreList.append(int(newList[i]))
    
    
    entryText = ""
    for team in ignoreList :
        entryText += repr(team) + ","
        
    ignoreListEntry.delete(0, END)
    ignoreListEntry.insert(0, entryText)
        
        
    if not strInvalid == "" :       
        trollfaceDialog("Warning, the following team(s) do not exist,\nSkipping "+\
                        "them\n{0:s}".format(strInvalid))
    # end ignoreListUpdate()
        
    
def ignoreListWindow() :
    global ignoreListBtn, ignoreListWindow, ignoreListEntry, ignoreList
    
    # turn the button off as a confirmation
    ignoreListBtn.config(state=DISABLED)
    
    # create a window to display the ignore list in
    ignoreListWindow = Toplevel()
    ignoreListWindow.title("Ignore List")
    ignoreListWindow.protocol("WM_DELETE_WINDOW", ignoreListWindowClose)
    ignoreListWindow.resizable(0, 0)
    
    instructLbl = Label(ignoreListWindow, text="Provide a comma separated list of "+\
                                       "team numbers\n to ignore when generating "+\
                                       "pick lists.")
    instructLbl.grid(row=0, column=0, sticky=N+E+W+S)
    
    entryText = ""
    for team in ignoreList :
        entryText += repr(team) + ","
        
    ignoreListEntry = Entry(ignoreListWindow, width=40)
    ignoreListEntry.insert(0, entryText)
    ignoreListEntry.grid(row=1, column=0, sticky=N+E+W+S)
    
    updateBtn = Button(ignoreListWindow, text="Update", command=ignoreListUpdate)
    updateBtn.grid(row=2, column=0, sticky=N+S)
    # end ignoreListWindow()
    
def ignoreListWindowClose() :
    ignoreListBtn.config(state=ACTIVE)
    ignoreListWindow.destroy()
   
   
   
     
TIW_PIC_ROW = 0
TIW_BUTTONS_ROW = 1
TIW_STATS_ROW = 3
TIW_PIT_ROW = 2
TIW_MATCH_ROW = 4

TIW_WIDTH = 1000
TIW_HEIGHT = 600

def makeTeamInfoWindow() :
    global teamPhotosDir,photoWindow, photoWindowFrame, photoTeamNoEntry, teamPhotoCanvas
    global pitTeamNoLookupTbl
    
    teamPhotosDir = tkFileDialog.askdirectory(parent=top, title=\
                                        "Which Folder are the team photos in?")

    if teamPhotosDir == '' : return
    
    # turn the button off as a confirmation
    photosBtn.config(state=DISABLED)

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
    
    
def loadTeamStats(self=None, event=None) :
    global fileNotFoundLbl, teamStatsFrame, photoList, photoDir, photoWindowFrame
    global matchTeamNoLookupTbl, usePitData, pitDatabase, pitDataColHeaders
    global matchDatabase
    
    # read the entrybox
    teamNo = photoTeamNoEntry.get()
    
    # need to distinguish between operating systems because linux and mac use "/"
    # for directories while windows uses "\"
    if os.name == 'posix' :
        photoDir = teamPhotosDir +"/"+ teamNo + "/"
    else :
        photoDir = teamPhotosDir +"\\"+ teamNo + "\\"

    try :
        photoList = os.listdir(photoDir)
    except OSError :
        photoList = []

    loadPhoto()

    # display the average stats for this team.
    
    if fileNotFoundLbl != None :
        fileNotFoundLbl.destroy()

    # destroy the old frame (if it existed) and create a new one
    if teamStatsFrame != None :
        teamStatsFrame.destroy()
    teamStatsFrame = Frame(photoWindowFrame)

    OPRcol=1

    if useMatchScoutingData :
        try:
            # we're now using teamNo as an index to a list, so it needs to be an int
            teamNo = int(teamNo)
            teamIdx = matchTeamNoLookupTbl.index(teamNo)
            colAve = averageCols(teamIdx)
            for colIdx in range(0,len(matchDataColHeaders)) :
                lbl1 = Label(teamStatsFrame, text=str(matchDataColHeaders[colIdx]), padx=5, pady=10)
                lbl1.grid(row=0, column=colIdx+1, sticky=N+E+W+S)

                ave = round(colAve[colIdx]*matchColMaxes[colIdx], 1)
                lbl2 = Label(teamStatsFrame, text=str(ave))
                lbl2.grid(row=1, column=colIdx+1)
                
                # Improvement Over Time
                teamMatches = matchDatabase[teamIdx]
                teamMatches.sort(key=lambda x: x[0]) #sort by match number
                
                Y = empty(len(teamMatches))
                for matchIdx in range(0, len(teamMatches)) :
                    Y[matchIdx] = teamMatches[matchIdx][colIdx+1]
                X = array( [arange(len(teamMatches)), ones(len(teamMatches))] )
                
                slope = linalg.lstsq(X.T, Y)[0][0]
                
                lbl = Label(teamStatsFrame, text="{:+.1f}".format(slope))
                lbl.grid(row=2, column=colIdx+1)
                
                
            
            OPRcol=colIdx+2
            Label(teamStatsFrame, text="Averages:").grid(row=1, column=0, sticky=N+E+W+S)
            Label(teamStatsFrame, text="Impr. over\nTime:").grid(row=2, column=0, sticky=N+E+W+S)
        except ValueError, UnboundLocalError :
            lbl = Label(teamStatsFrame, text="No match data for this team.")
            lbl.grid(row=1, column=0, sticky=N+S)
    else :
        lbl = Label(teamStatsFrame, text="No match data for this team.")
        lbl.grid(row=1, column=0, sticky=N+S)
    
    
    # if available, also add OPR and Toughness
    if useMatchResultsData :
        try :
            lbl1 = Label(teamStatsFrame, text="OPR", padx=5)
            lbl1.grid(row=0, column=OPRcol, sticky=N+E+W+S)
            lbl1 = Label(teamStatsFrame, text="Schd_Tough.")
            lbl1.grid(row=0, column=OPRcol+1, sticky=N+E+W+S)


            teamOPR.sort(key=lambda x: x[0])
            teamScheduleToughness.sort(key=lambda x: x[0])
            teamList.sort()
            teamIdx = teamList.index(str(teamNo))
            
            OPR = teamOPR[teamIdx][1]
            toughness = teamScheduleToughness[teamIdx][1]
            
            OPRlbl = Label(teamStatsFrame, text=trunc(OPR, 2), padx=5)
            OPRlbl.grid(row=1, column=OPRcol, sticky=N+E+W+S)
            toughLbl = Label(teamStatsFrame, text=str(trunc(toughness**6, 2)))
            toughLbl.grid(row=1, column=OPRcol+1, sticky=N+E+W+S)
        except ValueError, UnboundLocalError :
            # no match results or scouting data for this team
            pass

    
    teamStatsFrame.grid(row=TIW_STATS_ROW, column=0, sticky=N+E+W+S)
    
    pitDataStr = ''
    # display pit information if it exists
    if usePitData :
        try:
            # we're now using teamNo as an index to a list, so it needs to be an int
            teamNo = int(teamNo)
            teamIdx = pitTeamNoLookupTbl.index(teamNo)
            teamPitData = pitDatabase[teamIdx]
            
            for i in range(len(teamPitData)) :
                if int(teamPitData[i]) != 0 :
                    pitDataStr = pitDataStr + "    " + pitDataColHeaders[i]
            
        except ValueError, UnboundLocalError :
            pitDataStr="No pit data for this team."
    else :
        pitDataStr = "No pit data for this team."
    
    pitDataLbl = Label(photoWindowFrame, text=pitDataStr, pady=10)
    pitDataLbl.grid(row=TIW_PIT_ROW, column=0, sticky=N+E+W+S)
    
    
    # Now display the match data
    if useMatchScoutingData :
        
        try:
        
            matchDataFrame = Frame(photoWindowFrame)
            
            # print the column headers
            lbl = Label(matchDataFrame, text="Match No.", padx=5)
            lbl.grid(row=0, column=0, sticky=N+E+W+S)
            # we're now using teamNo as an index to a list, so it needs to be an int
            teamNo = int(teamNo)
            teamIdx = matchTeamNoLookupTbl.index(teamNo)
            for colIdx in range(0,len(matchDataColHeaders)) :
                lbl = Label(matchDataFrame, text=str(matchDataColHeaders[colIdx]), padx=5, pady=10)
                lbl.grid(row=0, column=colIdx+1, sticky=N+E+W+S)
            
            # print the data
            # the first column should be the match number
            for matchIdx in range(0,len(matchDatabase[teamIdx])) :
                for colIdx in range(0, len(matchDatabase[teamIdx][0])) :
                    lbl = Label(matchDataFrame, text=str(matchDatabase[teamIdx][matchIdx][colIdx]), padx=5)
                    lbl.grid(row=matchIdx+1, column=colIdx)

            matchDataFrame.grid(row=TIW_MATCH_ROW, column=0, sticky=N+E+W+S)
        except ValueError, UnboundLocalError :
            # no match results or scouting data for this team
            pass
    # end loadTeamStats()


def prevPic() :
    global teamPhotoNum, photoList
    
    if len(photoList) == 0: return
    teamPhotoNum = teamPhotoNum -1
    if teamPhotoNum < 0: teamPhotoNum = len(photoList)-1
    
    loadPhoto()
    
def nextPic() :
    global teamPhotoNum, photoList
    
    if len(photoList) == 0: return
    teamPhotoNum = (teamPhotoNum +1) % len(photoList)
    loadPhoto()



def loadPhoto() :
    global teamPhotoCanvas, teamPhotoNum, loadedPic, photoList
    global rootDir
    
    noRobotPic = False
    try :   
        startedOn = teamPhotoNum
        while (True) :
        
            if 0 >= len(photoList) :
                noRobotPic = True
                break
            
            photoPath = photoDir + photoList[teamPhotoNum]
            try :
                pic = Image.open(photoPath)
                break
            except IOError :
                # this is not a image file, remove it.
                photoList.pop(teamPhotoNum)
                #teamPhotoNum = teamPhotoNum +1 % len(photoList)
                
            
                if (teamPhotoNum +1) % len(photoList) == startedOn :
                    noRobotPic = True
                        
                    break
    except OSError, IndexError :        
        noRobotPic = True
        
    if noRobotPic :
        # display a fake robot instead
        if os.name == 'posix' :
            photoPath = rootDir + "/images/robot.png"
        else :
            photoPath = rootDir + "\\images\\robot.png"

        if os.path.isfile(photoPath) :
            pic = Image.open(photoPath)
    
    try :
        # scale it down if we need to
        pic.thumbnail((640, 480), Image.ANTIALIAS)
        
        #convert from Image to PhotoImage
        loadedPic = ImageTk.PhotoImage(pic)
        teamPhotoCanvas.config(width=loadedPic.width(), height=loadedPic.height()) 
        teamPhotoCanvas.create_image(2,2,image=loadedPic, anchor=NW)
    except UnboundLocalError :
        # do nothing
        pass
        
    teamPhotoCanvas.grid(row=0, column=0, sticky=N+S)
    
def makeCompareTeamsWindow() :
    global compareTeamsWindow, compareTeamsBtn, compareTeamsFrm, compareTeamNoEntry
    
    # create a window to display the photos in
    compareTeamsWindow = Toplevel()
    compareTeamsWindow.title("Compare Teams")
    compareTeamsWindow.protocol("WM_DELETE_WINDOW", compareTeamsWindowClose)
    compareTeamsWindow.resizable(1, 1)
    
    compareTeamsBtn.config(state=DISABLED)
    
    selectTeamFrame = Frame(compareTeamsWindow)
    compareTeamNoEntry = Entry(selectTeamFrame, width=7, justify=CENTER)
    compareTeamNoEntry.insert(0, "team_no")
    compareTeamNoEntry.grid(row=0, column=0, sticky=N+E+W+S)
    addTeam = Button(selectTeamFrame, text="+Add", command=addTeamToComparison)
    addTeam.grid(row=0, column=1, sticky=N+E+W+S)

    selectTeamFrame.grid(row=1, column=0, sticky=N+S)
    
    
    compareTeamsFrm = Frame(compareTeamsWindow)
    for colIdx in range(0,len(matchDataColHeaders)) :
            lbl1 = Label(compareTeamsFrm, text=str(matchDataColHeaders[colIdx]), padx=5)
            lbl1.grid(row=0, column=colIdx+1, sticky=N+E+W+S)
         
    
    # if available, also add OPR and Toughness
    lbl1 = Label(compareTeamsFrm, text="OPR", padx=5)
    lbl1.grid(row=0, column=colIdx+2, sticky=N+E+W+S)
    lbl1 = Label(compareTeamsFrm, text="Schd_Tough.")
    lbl1.grid(row=0, column=colIdx+3, sticky=N+E+W+S)
        
       
    compareTeamsFrm.grid(row=0, column=0, sticky=N+E+W+S)

def compareTeamsWindowClose() :
    global compareTeamsBtn, compareTeamsWindow
    
    compareTeamsBtn.config(state=ACTIVE)
    compareTeamsWindow.destroy()
    
    
def addTeamToComparison() :
    global compareTeamsFrm, compareTeamsWindow, compareTeamsNum
    global teamList, teamOPR, teamScheduleToughness
    
    compareTeamsNum = compareTeamsNum +1
    
    # read the entrybox
    teamNo = compareTeamNoEntry.get()
    
    # we're now using teamNo as an index to a list, so it needs to be an int
    teamNo = int(teamNo)
    try:
        colAve = averageCols(matchTeamNoLookupTbl.index(teamNo))
        for colIdx in range(0,len(matchDataColHeaders)) :
        
            ave = round(colAve[colIdx]*matchColMaxes[colIdx], 1)
            lbl2 = Label(compareTeamsFrm, text=str(ave))
            lbl2.grid(row=compareTeamsNum, column=colIdx+1, sticky=N+E+W+S)
        Label(compareTeamsFrm, text=str(teamNo)+" :").grid(row=compareTeamsNum, column=0, sticky=N+E+W+S)
    except ValueError :
        pass
        
        
    # if available, also add OPR and Toughness
    try :
        teamIdx = teamList.index(str(teamNo))
        
        OPR = teamOPR[teamIdx][1]
        toughness = teamScheduleToughness[teamIdx][1]
        
        OPRlbl = Label(compareTeamsFrm, text=trunc(OPR,2), padx=5)
        OPRlbl.grid(row=compareTeamsNum, column=colIdx+2, sticky=N+E+W+S)
        toughLbl = Label(compareTeamsFrm, text=str(trunc(toughness**6, 2)))
        toughLbl.grid(row=compareTeamsNum, column=colIdx+3, sticky=N+E+W+S)
    except ValueError: 
        # no match results data for this team
        pass
    

def makeGenListBtn() :
    global noTeamsEntrybox, ignoreListBtn, howManyTeamsFrame, genListBtn, compareTeamsBtn

    # generate list button
    genListBtn = Button(scoutingFrm, text="Generate\nPick List", command=generateList)
    
    # How Many Teams? entrybox
    howManyTeamsFrame = Frame(scoutingFrm)
    lbl1 = Label(howManyTeamsFrame, text="Generate a list of ")
    lbl2 = Label(howManyTeamsFrame, text="teams.")
    noTeamsEntrybox = Entry(howManyTeamsFrame, width=3, justify=RIGHT)
    noTeamsEntrybox.insert(0,"24")
    
    ignoreListBtn = Button(scoutingFrm, text="Teams to\nIgnore", command=ignoreListWindow)
    
    # add to GUI grid
    lbl1.grid(row=0, column=0, pady=5, sticky=N+E+W+S)
    noTeamsEntrybox.grid(row=0, column=1, sticky=N+E+W+S)
    lbl2.grid(row=1, column=0, sticky=N+E+W+S)
    howManyTeamsFrame.grid(row=3, column=0, sticky=N+E+W+S)
    genListBtn.grid(row=4, column=1, sticky=N+E+W+S)
    ignoreListBtn.grid(row=4, column=0, sticky=N+E+W+S)
    
    compareTeamsBtn = Button(top, text="Compare Teams", command=makeCompareTeamsWindow)
    compareTeamsBtn.grid(row=4, column=1, sticky=N+S)
    
    
def photoWindowClose() :
    photosBtn.config(state=ACTIVE)
    photoWindow.destroy()
    

# returns whether or not a given team has one of the machine features selected
# in the pit selection listbox
def pitFilter(teamNo) :
    # if we don't have pit data for this team, let them through
    try :
        pitTeamNoLookupTbl.index(teamNo)
    except ValueError :
        # this means they're not in the database
        return True

    # if we're not using pit data or
    # they havn't selected anything than don't bother filtering
    if not usePitData or pitSelectListbox.curselection() == () :
        return True

    if pitSelectAndOr.get() == 'and' : return pitFilterAnd(teamNo)
    else : return pitFilterOr(teamNo)
    # end pitFilter()

def pitFilterAnd(teamNo) :
    # get the selected features list
    for feat in pitSelectListbox.curselection() :
        feat = int(feat)
        
        if pitDatabase[pitTeamNoLookupTbl.index(teamNo)][feat].strip() == '0' :
            return False
    return True
    # end pitFilferAnd()

def pitFilterOr(teamNo) :
    # get the selected features list
    for feat in pitSelectListbox.curselection() :
        feat = int(feat)
        if pitDatabase[pitTeamNoLookupTbl.index(teamNo)][feat].strip() == '1' :
            return True
    return False
    # end pitFilterOr()



def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    return ('%.*f' % (n + 1, f))[:-1]


def loadmatchResultsDataFile():
    global useMatchResultsData, openMatchResultsBtn, matchResultsFrm, OPR_ToughnessFrame
    global teamList, teamOPR, teamScheduleToughness
    global dataDir
    
    # constants
    R1=0; R2=1; R3=2; B1=3; B2=4; B3=5; R_Score=6; B_Score=7
    win=0; loss=1; tie=2
    
    # unload the file if we click again.
    if useMatchResultsData :
        unloadMatchResultsFile()
        return
    
    
    # 1) find the file
          
    try:
        if dataDir != None : folder = dataDir
        else :  folder = os.getcwd()
        
        fileName = tkFileDialog.askopenfilename(parent=top, title=\
        "Choose A .csv File", defaultextension="*.csv", initialdir=folder)
    except TypeError :
        return
    
    if fileName == '' : return
    
    # save the location of the data
    dataDir = os.path.dirname(fileName)
            
    try :   
        matchFile = open(fileName, 'r')
    except IOError, TypeError :
        trollfaceDialog('Unable to open file')
        return
    

    # the whole file as a list of strings
    matchResultsData = matchFile.readlines()
    matchFile.close()
    
    # check that this file is in the right foramt
    illegalFormat = False
    if len(matchResultsData[0].split(',')) != 10 : illegalFormat = True
    
    
    for n in matchResultsData[0].split(',')[1:] :
        try:
            float(n)
        except ValueError, TypeError : illegalFormat = True
        
    if illegalFormat :
        trollfaceDialog('''I want the match results as downloaded from FIRST. 
You will have to open the file in a text editor and remove the 
column headers etc so that the file only contains data in the format

Time, MatchNo, R1, R2, R3, B1, B2, B3, R_Score, B_Score''')
        return
    
    # 2) load team numbers and match data
    
    teamList = []
    
    # info about teams, kept in the same order as teamList for cross-reference
    
    # this will be [matchNo1, matchNo2, ...]
    teamMatchesPlayed = [] 
    teamWLT = []
    teamScheduleToughness = []
    
    for match in range(0, len(matchResultsData)) :
        # split the data into cells and throw away the time and match No.
        matchResultsData[match] = matchResultsData[match].split(',')[2:]
        
        # populate the list of teams and which matches each was in
        for teamIdx in range(0,6) :
            teamNo = matchResultsData[match][teamIdx]
            
            # add them to the global list of teams and this match to their list
            if teamList.count(teamNo) == 0 : 
                teamList.append(teamNo)
                teamMatchesPlayed.append([])
                teamWLT.append([0,0,0])
                teamScheduleToughness.append([teamNo, 0])
            
            idx = teamList.index(teamNo)
            teamMatchesPlayed[idx].append(match)
            
            
            # update their WLT record
            
            # were they red or blue?
            if (matchResultsData[match][R1] == teamNo) | (matchResultsData[match][R2] == teamNo) \
            | (matchResultsData[match][R3] == teamNo) :
                if   int(R_Score) > int(B_Score) : teamWLT[idx][win] = teamWLT[idx][win] +1
                elif int(R_Score) < int(B_Score) : teamWLT[idx][loss] = teamWLT[idx][loss] +1
                else                             : teamWLT[idx][tie] = teamWLT[idx][tie] +1
            else :
                if   int(R_Score) < int(B_Score) : teamWLT[idx][win] = teamWLT[idx][win] +1
                elif int(R_Score) > int(B_Score) : teamWLT[idx][loss] = teamWLT[idx][loss] +1
                else                             : teamWLT[idx][tie] = teamWLT[idx][tie] +1
            
        # end for
    
    
    # 3) make Team Photos directories
    makePhotoDirectory(teamList, dataDir)
    
    
    # 4) calculate OPR
    
    numMatches = len(matchResultsData)
    # participation matrix, which team was in which match
    # it's twice the number of matches cause we treat the red and blue alliances as completely seperate matches
    Partic = numpy.empty((2*numMatches, len(teamList)))
    Partic[:] = 0
    
    
    # scores vector, the red or blue score for each match
    Score = numpy.empty((2*numMatches, 1))
    Score[:] = 0;
    
    
    for matchNo in range(0, len(matchResultsData)) :
        match = matchResultsData[matchNo]
        # red
        for i in range(R1, R3+1) :
            # find the index for this team
            teamIdx = teamList.index(match[i])
            
            Partic[matchNo][teamIdx] = 1
        # blue
        for i in range(B1, B3+1) :
            # find the index for this team
            teamIdx = teamList.index(match[i])
            
            Partic[matchNo + numMatches][teamIdx] = 1
    
    
        # score
        Score[matchNo] = match[R_Score]
        Score[matchNo + numMatches] = match[B_Score]
        
    OPR = numpy.linalg.lstsq(Partic, Score)
    
    
    teamOPR = []
    for i in range(0,len(teamList)) :
        teamOPR.append([teamList[i], OPR[0][i]]) # accessing elements in numpy matrices is complicated
    
    
    
    # 5) calculate Toughness of Schedule
        
    
    for teamIdx in range(0, len(teamList)) :
        team = teamList[teamIdx]
        
        for matchNo in teamMatchesPlayed[teamIdx] :
            alStr = 0; opStr = 0
            
            # were they red or blue?
            if (matchResultsData[matchNo][R1] == team) | (matchResultsData[matchNo][R2] == team) \
            | (matchResultsData[matchNo][R3] == team) :
                
                for al in range(0,3) :
                    alTeam = matchResultsData[matchNo][al]
                    if alTeam == team : continue
                    alTeamIdx = teamList.index(alTeam)
                    
                    alStr = alStr + teamWLT[alTeamIdx][win] + 0.5*teamWLT[alTeamIdx][tie]
                
                for op in range(3,6) :
                    opTeam = matchResultsData[matchNo][op]
                    opTeamIdx = teamList.index(opTeam)
                    
                    opStr = opStr + teamWLT[opTeamIdx][win] + 0.5*teamWLT[opTeamIdx][tie]
            else :
            
                for al in range(3,6) :
                    alTeam = matchResultsData[matchNo][al]
                    if alTeam == team : continue
                    alTeamIdx = teamList.index(alTeam)
                    
                    alStr = alStr + teamWLT[alTeamIdx][win] + 0.5*teamWLT[alTeamIdx][tie]
                
                for op in range(0,3) :
                    opTeam = matchResultsData[matchNo][op]
                    opTeamIdx = teamList.index(opTeam)
                    
                    opStr = opStr + teamWLT[opTeamIdx][win] + 0.5*teamWLT[opTeamIdx][tie]
            
            alStr = float(alStr)/2 +0.01 # the +1 is to avoid 1/0 errors
            opStr = float(opStr)/3 +0.01
            
            
            teamScheduleToughness[teamIdx][1] = teamScheduleToughness[teamIdx][1] + (opStr / alStr)
            
        teamScheduleToughness[teamIdx][1] = teamScheduleToughness[teamIdx][1] / len(teamMatchesPlayed[teamIdx])
    
    
    
    
    # 6) display everything.
    
    OPR_ToughnessFrame = Frame(matchResultsFrm)
    
    matchResultsFrm = Frame(top)
    
    #### OPR ####
    
    OPRLbl = Label(OPR_ToughnessFrame, text='OPR')
    OPRLbl.grid(row=0, column=0, sticky=N+E+W+S)
    
    teamOPR.sort(key=lambda x: x[1])
    teamOPR.reverse()
    
    OPRLabelText = ''
    
    for team in teamOPR :
        OPRLabelText = OPRLabelText + team[0] + ' '*(7-len(team[0])) + trunc(team[1], 2) + '\n'
    
    OPRText = Text(OPR_ToughnessFrame)
    OPRText.insert(END, OPRLabelText)
    
    # only add a scroll bar if the message is really long.
    if OPRLabelText.count("\n") > 10 :
        OPRscrollY = Scrollbar ( OPR_ToughnessFrame, orient=VERTICAL)#, cFommand=frame.yview )
        OPRscrollY.grid ( row=1, column=1, sticky=N+E+W+S )
        OPRscrollY.config(command=OPRText.yview)
        OPRText.config(yscrollcommand=OPRscrollY.set, width=13)
    else :
        OPRText.config(width=13, height=OPRLabelText.count("\n"))

    OPRText.grid(row=1, column=0, sticky=N+E+W+S)
    
    #### Toughness  ####
    
    toughnessLbl = Label(OPR_ToughnessFrame, text='Schedule\nToughness')
    toughnessLbl.grid(row=0, column=2, sticky=N+E+W+S)
    
    teamScheduleToughness.sort(key=lambda x: x[1])
    teamScheduleToughness.reverse()
    
    toughnessLabelText = ''
    
    for team in teamScheduleToughness :
        toughnessLabelText = toughnessLabelText + team[0] + ' '*(7-len(team[0])) + trunc(team[1]**6, 2) + '\n'
    
    
    
    toughnessText = Text(OPR_ToughnessFrame)
    toughnessText.insert(END, toughnessLabelText)

    # only add a scroll bar if the message is really long.
    if toughnessLabelText.count("\n") > 10 :
        toughScrollY = Scrollbar ( OPR_ToughnessFrame, orient=VERTICAL)#, command=frame.yview )
        toughScrollY.grid ( row=1, column=3, sticky=N+E+W+S )
        toughScrollY.config(command=toughnessText.yview)
        toughnessText.config(yscrollcommand=toughScrollY.set, width=13)
    else :
        toughnessText.config(width=13, height=toughnessLabelText.count("\n"))
    
    toughnessText.grid(row=1, column=2, sticky=N+E+W+S)
    
    
    matchResultsFrm.grid(row=2, column=0, sticky=N+E+W+S)
    
    useMatchResultsData = True
    openMatchResultsBtn.config(text="Unload Data")
    
    OPR_ToughnessFrame.grid(row=2, column=0, sticky=N+S+E+W)
    
    return
    # end loadmatchResultsDataFile()



def unloadMatchResultsFile() :
    global matchResultsFrm, openMatchResultsBtn, useMatchResultsData, OPR_ToughnessFrame
    
    OPR_ToughnessFrame.destroy()
    matchResultsFrm.destroy()
    
    useMatchResultsData = False
    openMatchResultsBtn.config(text="Load Results Data")
    


def loadMatchScoutingFile():
    global matchDatabase, matchDataColHeaders, matchTeamNoLookupTbl,\
            gameElemWeights, gameElemFrame, taskUse, taskAllNone
    global useMatchScoutingData, dataDir

    if useMatchScoutingData :
        unloadMatchScoutingFile()
        return

    # reinitialize the databases in case they have already loaded in a file
    matchDatabase = []
    matchTeamNoLookupTbl = []
    
    
    try:
        if dataDir != None : folder = dataDir
        else :  folder = os.getcwd()
        
        fileName = tkFileDialog.askopenfilename(parent=top, title=\
        "Choose A .csv File", defaultextension="*.csv", initialdir=folder)
    except TypeError :
        return
      
    # save the location of the data
    dataDir = os.path.dirname(fileName)
        
    try :   
        matchFile = open(fileName, 'r')
    except IOError :
        return
    except TypeError :
        return
    
    # the whole file as a list of strings
    lines = matchFile.readlines()
    
    matchFile.close()
    
    # first line contains the column headers. Split this into a list of strings.
    matchDataColHeaders = lines[0].strip().split(',')
    
    # throw away the "Team Number" and "Match Number" columns. I make the assumption that these will 
    # be the first two columns.
    matchDataColHeaders = matchDataColHeaders[2:]
    
    # throw away the headers line that we just dealt with.
    data = lines[1:] 
    
    # enter the data
    for match in range(0, len(data)) :
        data[match] = data[match].split(',') # split the data back into cells
        try:
            teamNo = int(data[match][0])
        except ValueError :
            trollfaceDialog(message="Corrupted file? I can't read the team number"+\
            " in line {0:d}:\n".format(match+2) +\
            "\nYou should have a look at that.\n"+\
            "(P.S. I can only read *.csv files)")
            matchDatabase = []
            return
        
        # throw away the team number column and clean the data
        data[match] = data[match][1:]
        
        
        for i in range(0, len(data[match])) :
            if data[match][i] == '': data[match][i] = '0'
            
            try:
                data[match][i] = int(data[match][i])
            except ValueError :
                # this is needed because sometimes an 'x' is used to 
                # denote a null value
                data[match][i] = None
        
        # see if this is the first time this team number has shown up.
        # if not, throw it in the table
        try:
            teamNoIdx = matchTeamNoLookupTbl.index(teamNo)
        except ValueError :
            matchTeamNoLookupTbl.append(teamNo)
            teamNoIdx = matchTeamNoLookupTbl.index(teamNo)
            # seeing as this is the first time we've seen this team
            # we also need to add it to the database
            matchDatabase.append([])
    
        # append this match to the database under its team number.
        matchDatabase[teamNoIdx].append(data[match])
    # end for
    
    # create a frame to hold the game elements and their weight box
    # (this is needed for alignment reasons)
    if gameElemFrame != None : gameElemFrame.destroy()
    gameElemFrame = Frame(scoutingFrm)

    taskLbl = Label(gameElemFrame, text="Task")
    taskLbl.grid(row=0, column=0, sticky=N+E+W+S)

    weightLbl = Label(gameElemFrame, text="Weight")
    weightLbl.grid(row=0, column=1, sticky=N+E+W+S)
    
    useLbl = Label(gameElemFrame, text="Use")
    useLbl.grid(row=0, column=2, sticky=N+E+W+S)

    # create a label for each column header (aka game element)
    gameElemNo = 0
    for gameElem in matchDataColHeaders :
        # text labels
        tmpLbl = Label(gameElemFrame, text=gameElem)
        tmpLbl.grid(row=gameElemNo+1, column=0, sticky=N+E+W+S)
        
        # entry boxes
        tmpEntrybox = Entry(gameElemFrame, width=3, justify=RIGHT)
        tmpEntrybox.insert(0,"10")
        tmpEntrybox.grid(row=gameElemNo+1, column=1, sticky=N+E+W+S)
        taskWeights.append(tmpEntrybox)
        
        # 'use' check boxes
        ckbxVar = BooleanVar(scoutingFrm)
        ckbxVar.set(1)
        taskUse.append(ckbxVar)
        
        tmpCheckBox = Checkbutton(gameElemFrame, variable=taskUse[gameElemNo])
        tmpCheckBox.grid(row=gameElemNo+1, column=2, sticky=N+E+W+S)
        
        gameElemNo = gameElemNo + 1
    
    selectAllLbl = Label(gameElemFrame, text="All/None:")
    selectAllLbl.grid(row=gameElemNo+1, column=0, sticky=N+E+W+S)
    
    taskAllNone = BooleanVar()
    taskAllNone.set(True)
    taskAllNoneckbx = Checkbutton(gameElemFrame, variable=taskAllNone,\
                        command=taskSelectAllNone)
    taskAllNoneckbx.grid(row=gameElemNo+1, column=2, sticky=N+E+W+S)
    
    gameElemFrame.grid(row=2, column=0, sticky=N+E+W+S)

    useMatchScoutingData = True
    openMatchFileBtn.config(text="Unload Match Data")

    
    if bothFilesAreLoaded() : checkFilesMatch()
    
    makeGenListBtn()
    
    # make a directory structure for the team photos
    makePhotoDirectory(matchTeamNoLookupTbl, dataDir)
    
    
    # end loadMatchScoutingFile

def unloadMatchScoutingFile() :
    global pitDatabase, matchTeamNoLookupTbl, matchColMaxes, useMatchScoutingData
    global taskWeights, taskUse, taskAllNone, ignoreList, compareTeamsBtn
    
    # re-initialize the pit related data structures
    matchDatabase = []
    matchDataColHeaders = []
    matchColMaxes = []
    matchTeamNoLookupTbl = []
    taskWeights = []
    taskUse = []
    taskAllNone = None
    ignoreList = []

    # erase and reset the GUI elements related to match data
    gameElemFrame.destroy()
    if ignoreListBtn != None : ignoreListBtn.destroy()
    if howManyTeamsFrame != None : howManyTeamsFrame.destroy()
    if genListBtn != None : genListBtn.destroy()
    if compareTeamsBtn != None : compareTeamsBtn.destroy()
    openMatchFileBtn.config(text="Load Match File")
    useMatchScoutingData = False


def loadPitFile() :
    global pitDatabase, pitTeamNoLookupTbl, pitSelectListbox, pitSelectAndOr, pitElemFrame, usePitData, pitDataColHeaders
    global dataDir

    # check if we need to load, or unload the file. If Load then stay in this function
    # if Unload go to unloadPitData()
    if usePitData :
        unloadPitFile()
        return
    
    # reinitialize the databases in case they have already loaded in a file
    pitDatabase = []
    pitTeamNoLookupTbl = []
    
    try:
        if dataDir != None : folder = dataDir
        else :  folder = os.getcwd()
        
        fileName = tkFileDialog.askopenfilename(parent=top, title=\
            "Choose A .csv File",defaultextension="*.csv", initialdir=folder)
    except TypeError :
        return
    
    # save the location of the data
    dataDir = os.path.dirname(fileName)
     
    try :
        matchFile = open(fileName, 'r')
    except IOError :
        return
    except TypeError :
        return
    
    # the whole file as a list of strings
    lines = matchFile.readlines()
    matchFile.close()
    
    pitElemFrame = Frame(scoutingFrm)
    pitInstructLbl = Label(pitElemFrame, text='Pick only robots with:')
        
    # first line contains the column headers. Split this into a list of strings.
    pitDataColHeaders = lines[0].split(',')
    
    # throw away the "team number" column. I make the assumption that this will 
    # be the first column.
    pitDataColHeaders = pitDataColHeaders[1:]
    
    # throw away the headers line that we just dealt with.
    data = lines[1:] 

    # for each line place it in the database, ensuring that it only appeared once.
    for team in data :
        team = team.split(',') # split the data back into cells
        try:
            teamNo = int(team[0])
        except ValueError :
            trollfaceDialog(message="Corrupted file? I can't read the file." +\
            "\nYou should have a look at that.\n"+\
            "(P.S. I can only read *.csv files)")
            pitDatabase = []
            return
        
        # throw away the team number column and turn empty cells into '0'
        team = team[1:]
        for i in range(len(team)) :
            if team[i] == '': team[i] = 0

        # each team should only appear once. if the team number if already in the list 
        # we have a problem
        if pitTeamNoLookupTbl.count(teamNo) != 0 :
            errorMsg = "Warning: There are multiple data entries for team {0:d}.\
                Ignoring some data.".format(teamNo)
            messageBox.showinfo(message=errorMsg)
        else :
            pitTeamNoLookupTbl.append(teamNo)
            teamNoIdx = pitTeamNoLookupTbl.index(teamNo)
            # seeing as this is the first time we've seen this team
            # we also need to add it to the database
            pitDatabase.append([])

            # append this pit data to the database under its team number.
            pitDatabase[teamNoIdx] = team
    # end for
    
    # radio buttons for and / or selecting mode
    pitRadioBtnFrame = Frame(pitElemFrame)
    pitSelectAndOr = StringVar(pitElemFrame)
    andRbtn = Radiobutton(pitRadioBtnFrame, text='and', variable=pitSelectAndOr,\
                            value='and')
    andRbtn.grid(row=0, column=0, sticky=N+E+W+S)
    orRbtn = Radiobutton(pitRadioBtnFrame, text='or', variable=pitSelectAndOr,\
                            value='or')
    orRbtn.grid(row=0, column=1, sticky=N+E+W+S)
    andRbtn.invoke()
    
    pitSelectListbox = Listbox(pitElemFrame, selectmode=Tkinter.MULTIPLE)
    
    for feature in pitDataColHeaders :
        pitSelectListbox.insert(END, feature.strip())
    
    pitInstructLbl.grid(row=0, column=0, sticky=N+E+W+S)
    pitRadioBtnFrame.grid(row=1, column=0, sticky=N+E+W+S)
    pitSelectListbox.grid(row=2, column=0, sticky=N+E+W+S)
    
    pitElemFrame.grid(row=2, column=1, sticky=N+E+W+S)    
    
    usePitData = True
    openPitFileBtn.config(text="Unload Pit Data")
    
    if bothFilesAreLoaded() : checkFilesMatch()
    # end loadPitFile()

    
def unloadPitFile() :
    global pitDatabase, pitTeamNoLookupTbl, pitSelectListbox, pitSelectAndOr, usePitData
    # re-initialize the pit related data structures
    pitDatabase = []
    pitTeamNoLookupTbl = []
    pitSelectListbox = None
    pitSelectAndOr = None

    # erase and reset the GUI elements related to pit data
    pitElemFrame.destroy()
    openPitFileBtn.config(text="Load Pit File")
    usePitData = False
     
    
def makePhotoDirectory(teamList, location) :
    global dataDir
        
    if not os.access(location, os.W_OK):
        print("Error in makePhotoDirectory(): the location supplied, "+str(location)+", is not a directory, or is not writable")
        return
        

    # make Team Photos directories
    os.chdir(location)
    try :
        os.mkdir('Team Photos')
    except OSError : pass
    
    os.chdir('Team Photos')
    
    for team in teamList :
        try :
            os.mkdir(str(team))
        except OSError : pass
        
    
    
    
    
def taskSelectAllNone() :
    global taskAllNone
    
    if taskAllNone.get() :
        setTo = True
    else : setTo = False
    
    for i in range(0,len(taskUse)) :
        taskUse[i].set(setTo)
    
def trollfaceDialog(message='') :
    global rootDir
    
    # create a new window
    tfDia = Toplevel(top)
    tfDia.transient(top)
    tfDia.title("Problem?")
    
    # load the trollface pic
    canvas = Canvas(tfDia)
    
    if os.name == 'posix' :
        photoPath = rootDir + "/images/trollface.gif"
    else :
        photoPath = rootDir + "\\images\\trollface.gif"
        
    if os.path.isfile(photoPath) :
        pic = PhotoImage(file=photoPath)
        canvas.config(width=pic.width(), height=pic.height()) 
        canvas.create_image(2,2,image=pic, anchor=NW)
    canvas.grid(row=0,column=0, sticky=N+E+W+S)
    
    lbl = Label(tfDia, text=message)
    lbl.grid(row=1, column=0, sticky=N+E+W+S)
    
    # ok button that closes the window
    okBtn = Button(tfDia, text="I'll fix that.", command=tfDia.destroy)
    okBtn.grid(row=2, column=0, sticky=N+E+W+S)
    
    tfDia.mainloop()


def scrollDialog(title='', warning= '', messageList='') :
    global top
    
    # create a new window
    scrlDia = Toplevel(top)
    scrlDia.transient(top)
    scrlDia.title(title)

    Label(scrlDia, text=warning, justify=LEFT).grid(row=0, column=0, sticky=N+E+W+S)

    text = Text(scrlDia)
    text.insert(END, messageList)

    # only add a scroll bar if the message is really long.
    if messageList.count("\n") > 10 :
        scrollY = Scrollbar ( scrlDia, orient=VERTICAL)#, command=frame.yview )
        scrollY.grid ( row=1, column=1, sticky=N+E+W+S )
        scrollY.config(command=text.yview)
        text.config(yscrollcommand=scrollY.set, width=20)
    else :
        text.config(width=20, height=10)

    text.grid(row=1, column=0, sticky=N+E+W+S)

    # ok button that closes the window
    okBtn = Button(scrlDia, text="That's fine.", command=scrlDia.destroy)
    okBtn.grid(row=2, column=0, sticky=N+E+W+S)

    #end scrollDialog


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            
        
        # do not shrink to fit contents
        self.pack_propagate(0)
        
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        canvas.pack_propagate(0)
        vscrollbar.config(command=canvas.yview, width=15)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior.pack_propagate(0)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        return

main()
