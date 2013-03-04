#! /usr/bin/env python
# -*- python -*-

import sys

py2 = py30 = py31 = False
version = sys.hexversion
if version >= 0x020600F0 and version < 0x03000000 :
    py2 = True    # Python 2.6 or 2.7
    from Tkinter import *
    import ttk
elif version >= 0x03000000 and version < 0x03010000 :
    py30 = True
    from tkinter import *
    import ttk
elif version >= 0x03010000:
    py31 = True
    from tkinter import *
    import tkinter.ttk as ttk
else:
    print ("""
    You do not have a version of python supporting ttk widgets..
    You need a version >= 2.6 to execute PAGE modules.
    """)
    sys.exit()



def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    root.title('New_Toplevel_1')
    root.geometry('1167x759+499+271')
    w = New_Toplevel_1 (root)
    init()
    root.mainloop()

w = None
def create_New_Toplevel_1 (root):
    '''Starting point when module is imported by another program.'''
    global w, w_win
    if w: # So we have only one instance of window.
        return
    w = Toplevel (root)
    w.title('New_Toplevel_1')
    w.geometry('1167x759+499+271')
    w_win = New_Toplevel_1 (w)
    init()
    return w_win

def destroy_New_Toplevel_1 ():
    global w
    w.destroy()
    w = None




def init():
    pass




class New_Toplevel_1:
    def __init__(self, master=None):
        # Set background of toplevel window to match
        # current style
        style = ttk.Style()
        theme = style.theme_use()
        default = style.lookup(theme, 'background')
        master.configure(background=default)

        self.Canvas1 = Canvas (master)
        self.Canvas1.place(relx=0.48,rely=0.16,relheight=1.03,relwidth=0.52)
        self.Canvas1.configure(background="Blue")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(relief="ridge")

        self.Canvas2 = Canvas (master)
        self.Canvas2.place(relx=-0.04,rely=-0.01,relheight=1.04,relwidth=0.53)
        self.Canvas2.configure(background="Red")
        self.Canvas2.configure(borderwidth="2")
        self.Canvas2.configure(relief="ridge")

        self.Canvas3 = Canvas (master)
        self.Canvas3.place(relx=0.0,rely=0.0,relheight=0.17,relwidth=1.02)
        self.Canvas3.configure(background="Black")
        self.Canvas3.configure(borderwidth="2")
        self.Canvas3.configure(relief="ridge")

        self.Title = Label (master)
        self.Title.place(relx=0.44,rely=0.01,height=51,width=111)
        self.Title.configure(activebackground="#ffffff")
        self.Title.configure(activeforeground="#000000")
        self.Title.configure(background="#000000")
        font11 = "-family Arial -size 10 -weight normal -slant roman -underline 0 -overstrike 0"
        self.Title.configure(font=font11)
        self.Title.configure(foreground="#ffffff")
        self.Title.configure(text='''KBotics Scouting''')

        self.version = Label (master)
        self.version.place(relx=0.45,rely=0.05,height=21,width=91)
        self.version.configure(activebackground="#000000")
        self.version.configure(activeforeground="#ffffff")
        self.version.configure(background="#000000")
        self.version.configure(foreground="#ffffff")
        self.version.configure(text='''version BETA 0.2''')

        self.copyright = Label (master)
        self.copyright.place(relx=0.33,rely=0.08,height=21,width=371)
        self.copyright.configure(background="#000000")
        self.copyright.configure(foreground="#ffffff")
        self.copyright.configure(text='''(C) Russell Dawes, Sawyer Ship-Wiedersprecher, and Kevin Hughes''')

        self.Match = Label (master)
        self.Match.place(relx=0.47,rely=0.11,height=21,width=50)
        self.Match.configure(background="#000000")
        self.Match.configure(foreground="#ffffff")
        self.Match.configure(text='''Match #''')

        self.MatchEntry = Entry (master)
        self.MatchEntry.place(relx=0.44,rely=0.14,relheight=0.03,relwidth=0.11)
        self.MatchEntry.configure(background="white")

        self.RedTeam = Label (master)
        self.RedTeam.place(relx=0.18,rely=0.13,height=21,width=71)
        self.RedTeam.configure(background="#000000")
        self.RedTeam.configure(foreground="#ffffff")
        self.RedTeam.configure(text='''Red Team''')

        self.BlueTeam = Label (master)
        self.BlueTeam.place(relx=0.76,rely=0.13,height=21,width=71)
        self.BlueTeam.configure(background="#000000")
        self.BlueTeam.configure(foreground="#ffffff")
        self.BlueTeam.configure(text='''Blue Team''')

        self.TeamText1 = Label (master)
        self.TeamText1.place(relx=0.03,rely=0.2,height=21,width=36)
        self.TeamText1.configure(activebackground="#000000")
        self.TeamText1.configure(background="#ff0000")
        self.TeamText1.configure(text='''Team''')

        self.hastag1 = Label (master)
        self.hastag1.place(relx=0.06,rely=0.2,height=21,width=13)
        self.hastag1.configure(background="#ff0000")
        self.hastag1.configure(text='''#''')

        self.RedEntry1 = Entry (master)
        self.RedEntry1.place(relx=0.08,rely=0.2,relheight=0.03,relwidth=0.05)
        self.RedEntry1.configure(background="white")

        self.hashtag2 = Label (master)
        self.hashtag2.place(relx=0.17,rely=0.2,height=21,width=13)
        self.hashtag2.configure(background="#ff0000")
        self.hashtag2.configure(text='''#''')

        self.RedEntry2 = Entry (master)
        self.RedEntry2.place(relx=0.19,rely=0.2,relheight=0.03,relwidth=0.05)
        self.RedEntry2.configure(background="white")

        self.hashtag3 = Label (master)
        self.hashtag3.place(relx=0.29,rely=0.2,height=21,width=13)
        self.hashtag3.configure(background="#ff0000")
        self.hashtag3.configure(text='''#''')

        self.RedEntry3 = Entry (master)
        self.RedEntry3.place(relx=0.31,rely=0.2,relheight=0.03,relwidth=0.05)
        self.RedEntry3.configure(background="white")

        self.TeamText2 = Label (master)
        self.TeamText2.place(relx=0.14,rely=0.2,height=21,width=36)
        self.TeamText2.configure(background="#ff0000")
        self.TeamText2.configure(text='''Team''')

        self.TeamText3 = Label (master)
        self.TeamText3.place(relx=0.26,rely=0.2,height=21,width=36)
        self.TeamText3.configure(background="#ff0000")
        self.TeamText3.configure(text='''Team''')

        self.TeamText4 = Label (master)
        self.TeamText4.place(relx=0.64,rely=0.2,height=21,width=36)
        self.TeamText4.configure(background="#0000ff")
        self.TeamText4.configure(text='''Team''')

        self.TeamText5 = Label (master)
        self.TeamText5.place(relx=0.75,rely=0.2,height=21,width=36)
        self.TeamText5.configure(background="#0000ff")
        self.TeamText5.configure(text='''Team''')

        self.TeamText6 = Label (master)
        self.TeamText6.place(relx=0.87,rely=0.2,height=21,width=36)
        self.TeamText6.configure(background="#0000ff")
        self.TeamText6.configure(text='''Team''')

        self.hashtag4 = Label (master)
        self.hashtag4.place(relx=0.67,rely=0.2,height=21,width=13)
        self.hashtag4.configure(background="#0000ff")
        self.hashtag4.configure(text='''#''')

        self.BlueEntry1 = Entry (master)
        self.BlueEntry1.place(relx=0.69,rely=0.2,relheight=0.03,relwidth=0.05)
        self.BlueEntry1.configure(background="white")

        self.hashtag5 = Label (master)
        self.hashtag5.place(relx=0.79,rely=0.2,height=21,width=13)
        self.hashtag5.configure(background="#0000ff")
        self.hashtag5.configure(text='''#''')

        self.BlueEntry2 = Entry (master)
        self.BlueEntry2.place(relx=0.81,rely=0.2,relheight=0.03,relwidth=0.05)
        self.BlueEntry2.configure(background="white")

        self.hashtag6 = Label (master)
        self.hashtag6.place(relx=0.9,rely=0.2,height=21,width=13)
        self.hashtag6.configure(background="#0000ff")
        self.hashtag6.configure(text='''#''')

        self.BlueEntry3 = Entry (master)
        self.BlueEntry3.place(relx=0.91,rely=0.2,relheight=0.03,relwidth=0.05)
        self.BlueEntry3.configure(background="white")

        self.Submit = Button (master)
        self.Submit.place(relx=0.0,rely=0.91,height=74,width=1177)
        self.Submit.configure(pady="0")
        self.Submit.configure(text='''Submit''')

        self.PointsText1 = Label (master)
        self.PointsText1.place(relx=0.03,rely=0.24,height=11,width=31)
        self.PointsText1.configure(background="#ff0000")
        self.PointsText1.configure(text='''Auto''')

        self.RedAuto1 = Entry (master)
        self.RedAuto1.place(relx=0.08,rely=0.24,relheight=0.03,relwidth=0.05)
        self.RedAuto1.configure(background="white")

        self.RedAuto2 = Entry (master)
        self.RedAuto2.place(relx=0.19,rely=0.24,relheight=0.03,relwidth=0.05)
        self.RedAuto2.configure(background="white")

        self.RedAuto3 = Entry (master)
        self.RedAuto3.place(relx=0.31,rely=0.24,relheight=0.03,relwidth=0.05)
        self.RedAuto3.configure(background="white")

        self.ShotsText1 = Label (master)
        self.ShotsText1.place(relx=0.01,rely=0.28,height=21,width=71)
        self.ShotsText1.configure(background="#ff0000")
        self.ShotsText1.configure(text='''3 pointers''')

        self.Red3Points1 = Entry (master)
        self.Red3Points1.place(relx=0.08,rely=0.28,relheight=0.03,relwidth=0.05)

        self.Red3Points1.configure(background="white")

        self.Red3Points2 = Entry (master)
        self.Red3Points2.place(relx=0.19,rely=0.28,relheight=0.03,relwidth=0.05)

        self.Red3Points2.configure(background="white")

        self.Red3Points3 = Entry (master)
        self.Red3Points3.place(relx=0.31,rely=0.28,relheight=0.03,relwidth=0.05)

        self.Red3Points3.configure(background="white")

        self.HeightText1 = Label (master)
        self.HeightText1.place(relx=0.01,rely=0.32,height=21,width=58)
        self.HeightText1.configure(background="#ff0000")
        self.HeightText1.configure(text='''2 pointers''')

        self.Red2Points1 = Entry (master)
        self.Red2Points1.place(relx=0.08,rely=0.32,relheight=0.03,relwidth=0.05)

        self.Red2Points1.configure(background="white")

        self.Red2Points2 = Entry (master)
        self.Red2Points2.place(relx=0.19,rely=0.32,relheight=0.03,relwidth=0.05)

        self.Red2Points2.configure(background="white")

        self.Red2Points3 = Entry (master)
        self.Red2Points3.place(relx=0.31,rely=0.32,relheight=0.03,relwidth=0.05)

        self.Red2Points3.configure(background="white")

        self.PointsText2 = Label (master)
        self.PointsText2.place(relx=0.65,rely=0.24,height=21,width=32)
        self.PointsText2.configure(background="#0000ff")
        self.PointsText2.configure(text='''Auto''')

        self.BlueAuto1 = Entry (master)
        self.BlueAuto1.place(relx=0.69,rely=0.24,relheight=0.03,relwidth=0.05)
        self.BlueAuto1.configure(background="white")

        self.BlueAuto2 = Entry (master)
        self.BlueAuto2.place(relx=0.81,rely=0.24,relheight=0.03,relwidth=0.05)
        self.BlueAuto2.configure(background="white")

        self.BlueAuto3 = Entry (master)
        self.BlueAuto3.place(relx=0.91,rely=0.24,relheight=0.03,relwidth=0.05)
        self.BlueAuto3.configure(background="white")

        self.ShotsText2 = Label (master)
        self.ShotsText2.place(relx=0.63,rely=0.28,height=21,width=58)
        self.ShotsText2.configure(background="#0000ff")
        self.ShotsText2.configure(text='''3 pointers''')

        self.Blue3Points1 = Entry (master)
        self.Blue3Points1.place(relx=0.69,rely=0.28,relheight=0.03
                ,relwidth=0.05)
        self.Blue3Points1.configure(background="white")

        self.Blue3Points2 = Entry (master)
        self.Blue3Points2.place(relx=0.81,rely=0.28,relheight=0.03
                ,relwidth=0.05)
        self.Blue3Points2.configure(background="white")

        self.Blue3Points3 = Entry (master)
        self.Blue3Points3.place(relx=0.91,rely=0.28,relheight=0.03
                ,relwidth=0.05)
        self.Blue3Points3.configure(background="white")

        self.HeightText2 = Label (master)
        self.HeightText2.place(relx=0.63,rely=0.32,height=21,width=58)
        self.HeightText2.configure(background="#0000ff")
        self.HeightText2.configure(text='''2 pointers''')

        self.Blue2Points1 = Entry (master)
        self.Blue2Points1.place(relx=0.69,rely=0.32,relheight=0.03
                ,relwidth=0.05)
        self.Blue2Points1.configure(background="white")

        self.Blue2Points2 = Entry (master)
        self.Blue2Points2.place(relx=0.81,rely=0.32,relheight=0.03
                ,relwidth=0.05)
        self.Blue2Points2.configure(background="white")

        self.Blue2Points3 = Entry (master)
        self.Blue2Points3.place(relx=0.91,rely=0.32,relheight=0.03
                ,relwidth=0.05)
        self.Blue2Points3.configure(background="white")

        self.Label1 = Label (master)
        self.Label1.place(relx=0.01,rely=0.36,height=21,width=58)
        self.Label1.configure(background="#ff0000")
        self.Label1.configure(text='''1 pointers''')

        self.Red1Points1 = Entry (master)
        self.Red1Points1.place(relx=0.08,rely=0.36,relheight=0.03,relwidth=0.05)

        self.Red1Points1.configure(background="white")

        self.Red1Points2 = Entry (master)
        self.Red1Points2.place(relx=0.19,rely=0.36,relheight=0.03,relwidth=0.05)

        self.Red1Points2.configure(background="white")

        self.Red1Points3 = Entry (master)
        self.Red1Points3.place(relx=0.31,rely=0.36,relheight=0.03,relwidth=0.05)

        self.Red1Points3.configure(background="white")

        self.Label2 = Label (master)
        self.Label2.place(relx=0.63,rely=0.36,height=21,width=58)
        self.Label2.configure(background="#0000ff")
        self.Label2.configure(text='''1 pointers''')

        self.Blue1Points1 = Entry (master)
        self.Blue1Points1.place(relx=0.69,rely=0.36,relheight=0.03
                ,relwidth=0.05)
        self.Blue1Points1.configure(background="white")

        self.Blue1Points2 = Entry (master)
        self.Blue1Points2.place(relx=0.81,rely=0.36,relheight=0.03
                ,relwidth=0.05)
        self.Blue1Points2.configure(background="white")

        self.Blue1Points3 = Entry (master)
        self.Blue1Points3.place(relx=0.91,rely=0.36,relheight=0.03
                ,relwidth=0.05)
        self.Blue1Points3.configure(background="white")

        self.Label3 = Label (master)
        self.Label3.place(relx=0.01,rely=0.4,height=21,width=75)
        self.Label3.configure(background="#ff0000")
        self.Label3.configure(text='''Climb height''')

        self.Label4 = Label (master)
        self.Label4.place(relx=0.63,rely=0.4,height=21,width=75)
        self.Label4.configure(background="#0000ff")
        self.Label4.configure(text='''Climb height''')


        self.RedNote1 = Entry (master)
        self.RedNote1.place(relx=0.03,rely=0.55,relheight=0.35,relwidth=0.11)
        self.RedNote1.configure(background="white")
        self.RedNote1.configure(text='''Notes''')

        self.RedNote2 = Entry (master)
        self.RedNote2.place(relx=0.15,rely=0.55,relheight=0.35,relwidth=0.11)
        self.RedNote2.configure(background="white")
        self.RedNote2.configure(text='''Notes''')

        self.RedNote3 = Entry (master)
        self.RedNote3.place(relx=0.27,rely=0.55,relheight=0.35,relwidth=0.11)
        self.RedNote3.configure(background="white")
        self.RedNote3.configure(text='''Notes''')

        self.BlueNote1 = Entry (master)
        self.BlueNote1.place(relx=0.62,rely=0.55,relheight=0.35,relwidth=0.11)
        self.BlueNote1.configure(background="white")
        self.BlueNote1.configure(text='''Notes''')

        self.BlueNote2 = Entry (master, text ="Notes")
        self.BlueNote2.place(relx=0.74,rely=0.55,relheight=0.35,relwidth=0.11)
        self.BlueNote2.configure(background="white")

        self.BlueNote3 = Entry (master, text ="Notes")
        self.BlueNote3.place(relx=0.86,rely=0.55,relheight=0.35,relwidth=0.11)
        self.BlueNote3.configure(background="white")


        self.Label6 = Label (master)
        self.Label6.place(relx=0.17,rely=0.47,height=21,width=88)
        self.Label6.configure(background="#ff0000")
        self.Label6.configure(text='''Red Total Score''')

        self.RedScore1 = Entry (master)
        self.RedScore1.place(relx=0.15,rely=0.5,relheight=0.03,relwidth=0.11)
        self.RedScore1.configure(background="white")

        self.Label7 = Label (master)
        self.Label7.place(relx=0.75,rely=0.47,height=21,width=91)
        self.Label7.configure(background="#0000ff")
        self.Label7.configure(text='''Blue Total Score''')

        self.BlueScore1 = Entry (master)
        self.BlueScore1.place(relx=0.74,rely=0.5,relheight=0.03,relwidth=0.11)
        self.BlueScore1.configure(background="white")

        self.RedClimbHeight1 = Entry (master)
        self.RedClimbHeight1.place(relx=0.08,rely=0.4,relheight=0.03
                ,relwidth=0.05)
        self.RedClimbHeight1.configure(background="white")

        self.RedClimbHeight2 = Entry (master)
        self.RedClimbHeight2.place(relx=0.19,rely=0.4,relheight=0.03
                ,relwidth=0.05)
        self.RedClimbHeight2.configure(background="white")

        self.RedClimbHeight3 = Entry (master)
        self.RedClimbHeight3.place(relx=0.31,rely=0.4,relheight=0.03
                ,relwidth=0.05)
        self.RedClimbHeight3.configure(background="white")

        self.BlueClimbHeight1 = Entry (master)
        self.BlueClimbHeight1.place(relx=0.69,rely=0.4,relheight=0.03
                ,relwidth=0.05)
        self.BlueClimbHeight1.configure(background="white")

        self.BlueClimbHeight2 = Entry (master)
        self.BlueClimbHeight2.place(relx=0.81,rely=0.4,relheight=0.03
                ,relwidth=0.05)
        self.BlueClimbHeight2.configure(background="white")

        self.BlueClimbHeight3 = Entry (master)
        self.BlueClimbHeight3.place(relx=0.91,rely=0.4,relheight=0.03
                ,relwidth=0.05)
        self.BlueClimbHeight3.configure(background="white")



        self.menubar = Menu(master,font="{MS Sans Serif} 10",bg='#d9d9d9',fg='#000000')
        master.configure(menu = self.menubar)










def callback():
    Matchnumber = w.MatchEntry.get()
    RedTeam1 = w.RedEntry1.get()
    RedTeam2 = w.RedEntry2.get()
    RedTeam3 = w.RedEntry3.get()
    BlueTeam1 = w.BlueEntry1.get()
    BlueTeam2 = w.BlueEntry2.get()
    BlueTeam3 = w.BlueEntry3.get()
    RedAuto1 = w.RedAuto1.get()
    RedAuto2 = w.RedAuto2.get()
    RedAuto3 = w.RedAuto3.get()
    BlueAuto1 = w.BlueAuto1.get()
    BlueAuto2 = w.BlueAuto2.get()
    BlueAuto3 = w.BlueAuto3.get()
    Red3Points1 = w.Red3Points1.get()
    Red3Points2 = w.Red3Points2.get()
    Red3Points3 = w.Red3Points3.get()
    Blue3Points1 = w.Blue3Points1.get()
    Blue3Points2 = w.Blue3Points2.get()
    Blue3Points3 = w.Blue3Points3.get()
    Red2Points1 = w.Red2Points1.get()
    Red2Points2 = w.Red2Points2.get()
    Red2Points3 = w.Red2Points3.get()
    Blue2Points1 = w.Blue2Points1.get()
    Blue2Points2 = w.Blue2Points2.get()
    Blue2Points3 = w.Blue2Points3.get()
    Red1Points1 = w.Red1Points1.get()
    Red1Points2 = w.Red1Points2.get()
    Red1Points3 = w.Red1Points3.get()
    Blue1Points1 = w.Blue1Points1.get()
    Blue1Points2 = w.Blue1Points2.get()
    Blue1Points3 = w.Blue1Points3.get()
    RedClimbHeight1 = w.RedClimbHeight1.get()
    RedClimbHeight2 = w.RedClimbHeight2.get()
    RedClimbHeight3 = w.RedClimbHeight3.get()
    BlueClimbHeight1 = w.BlueClimbHeight1.get()
    BlueClimbHeight2 = w.BlueClimbHeight2.get()
    BlueClimbHeight3 = w.BlueClimbHeight3.get()
    RedScore = w.RedScore1.get()
    BlueScore = w.BlueScore1.get()
    RedNote1 = w.RedNote1.get()
    RedNote2 = w.RedNote2.get()
    RedNote3 = w.RedNote3.get()
    BlueNote1 = w.BlueNote1.get()
    BlueNote2 = w.BlueNote2.get()
    BlueNote3 = w.BlueNote3.get()

    print Matchnumber, RedTeam1, RedTeam2, RedTeam3, BlueTeam1, BlueTeam2, BlueTeam3, RedAuto1, RedAuto2, RedAuto3, BlueAuto1, BlueAuto2, BlueAuto3
    print Red3Points1, Red3Points2, Red3Points3, Blue3Points1, Blue3Points2, Blue3Points3, Red2Points1, Red2Points2, Red2Points3, Blue2Points1, Blue2Points2, Blue2Points3
    print Red1Points1, Red1Points2, Red1Points3, Blue1Points1, Blue1Points2, Blue1Points3,
    print RedClimbHeight1, RedClimbHeight2, RedClimbHeight3, BlueClimbHeight1, BlueClimbHeight2, BlueClimbHeight3, RedScore, BlueScore
    print RedNote1, RedNote2, RedNote3, BlueNote1, BlueNote2, BlueNote3







if __name__ == '__main__':
    vp_start_gui()
