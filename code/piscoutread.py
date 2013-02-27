import Tkinter
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from PIL import Image, ImageTk
import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

photoWindow=None
photoWindowFrame = None
photoTeamNoEntry = None
teamPhotoCanvas = None
TIW_WIDTH = 1000
TIW_HEIGHT = 600
TIW_PIC_ROW = 0
TIW_BUTTONS_ROW = 1
TIW_STATS_ROW = 3
TIW_PIT_ROW = 2
TIW_MATCH_ROW = 4


'''class VerticalScrolledFrame(Frame):
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

def photoWindowClose() :
    #photosBtn.config(state=ACTIVE)
    photoWindow.destroy()
'''
def getPicture():

    OpenPhoto = tkFileDialog.askdirectory(parent=top, initialdir='C:\Documents and Settings\CCSS\My Documents\GitHub\2809_scouting_db\pictures' ,title=\
                                        "Which photo is it?")
    photo = str(OpenPhoto.get())
    im = Image.open(photo)
    im.show()



teamNumber = int(raw_input('Enter a team number: '))
for row in c.execute('SELECT * FROM pitScouting'):
    if row[0] == teamNumber:
        print row
        top = Tk()
        getPicture()



raw_input('press any key to continue...')


