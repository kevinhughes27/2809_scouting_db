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
    import tkMessageBox
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
    root.geometry('600x450+513+198')
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
    w.geometry('600x450+513+198')
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

        self.Title = Label (master)
        self.Title.place(relx=0.38,rely=-0.02,height=51,width=111)
        self.Title.configure(text='''KBotics Scouting''')

        self.version = Label (master)
        self.version.place(relx=0.42,rely=0.07,height=21,width=71)
        self.version.configure(text='''version 0.1''')

        self.copyright = Label (master)
        self.copyright.place(relx=0.17,rely=0.11,height=21,width=371)
        self.copyright.configure(text='''(C) Russell Dawes, Sawyer Ship-Wiedersprecher, and Kevin Hughes''')

        self.Match = Label (master)
        self.Match.place(relx=0.35,rely=0.22,height=21,width=50)
        self.Match.configure(text='''Match #''')

        self.MatchEntry = Entry (master)
        self.MatchEntry.place(relx=0.45,rely=0.22,relheight=0.04,relwidth=0.21)
        self.MatchEntry.configure(background="white")

        self.RedScore = Label (master)
        self.RedScore.place(relx=0.1,rely=0.31,height=21,width=71)
        self.RedScore.configure(text='''Red Score''')

        self.BlueScore = Label (master)
        self.BlueScore.place(relx=0.77,rely=0.31,height=21,width=71)
        self.BlueScore.configure(text='''Blue Score''')

        self.RedEntry = Entry (master)
        self.RedEntry.place(relx=0.07,rely=0.38,relheight=0.04,relwidth=0.21)
        self.RedEntry.configure(background="white")

        self.BlueEntry = Entry (master)
        self.BlueEntry.place(relx=0.73,rely=0.38,relheight=0.04,relwidth=0.21)
        self.BlueEntry.configure(background="white")

        self.TeamText1 = Label (master)
        self.TeamText1.place(relx=0.1,rely=0.51,height=21,width=36)
        self.TeamText1.configure(text='''Team''')

        self.hastag1 = Label (master)
        self.hastag1.place(relx=0.05,rely=0.58,height=21,width=13)
        self.hastag1.configure(text='''#''')

        self.RedEntry1 = Entry (master)
        self.RedEntry1.place(relx=0.08,rely=0.58,relheight=0.04,relwidth=0.09)
        self.RedEntry1.configure(background="white")

        self.hashtag2 = Label (master)
        self.hashtag2.place(relx=0.18,rely=0.58,height=21,width=13)
        self.hashtag2.configure(text='''#''')

        self.RedEntry2 = Entry (master)
        self.RedEntry2.place(relx=0.22,rely=0.58,relheight=0.04,relwidth=0.09)
        self.RedEntry2.configure(background="white")

        self.hashtag3 = Label (master)
        self.hashtag3.place(relx=0.32,rely=0.58,height=21,width=13)
        self.hashtag3.configure(text='''#''')

        self.RedEntry3 = Entry (master)
        self.RedEntry3.place(relx=0.35,rely=0.58,relheight=0.04,relwidth=0.09)
        self.RedEntry3.configure(background="white")

        self.TeamText2 = Label (master)
        self.TeamText2.place(relx=0.23,rely=0.51,height=21,width=36)
        self.TeamText2.configure(text='''Team''')

        self.TeamText3 = Label (master)
        self.TeamText3.place(relx=0.37,rely=0.51,height=21,width=36)
        self.TeamText3.configure(text='''Team''')

        self.TeamText4 = Label (master)
        self.TeamText4.place(relx=0.62,rely=0.51,height=21,width=36)
        self.TeamText4.configure(text='''Team''')

        self.TeamText5 = Label (master)
        self.TeamText5.place(relx=0.72,rely=0.51,height=21,width=56)
        self.TeamText5.configure(text='''Team''')

        self.TeamText6 = Label (master)
        self.TeamText6.place(relx=0.85,rely=0.51,height=21,width=36)
        self.TeamText6.configure(text='''Team''')

        self.hashtag4 = Label (master)
        self.hashtag4.place(relx=0.57,rely=0.58,height=21,width=13)
        self.hashtag4.configure(text='''#''')

        self.BlueEntry1 = Entry (master)
        self.BlueEntry1.place(relx=0.6,rely=0.58,relheight=0.04,relwidth=0.09)
        self.BlueEntry1.configure(background="white")

        self.hashtag5 = Label (master)
        self.hashtag5.place(relx=0.7,rely=0.58,height=21,width=13)
        self.hashtag5.configure(text='''#''')

        self.BlueEntry2 = Entry (master)
        self.BlueEntry2.place(relx=0.73,rely=0.58,relheight=0.04,relwidth=0.09)
        self.BlueEntry2.configure(background="white")

        self.hashtag6 = Label (master)
        self.hashtag6.place(relx=0.83,rely=0.58,height=21,width=13)
        self.hashtag6.configure(text='''#''')

        self.BlueEntry3 = Entry (master)
        self.BlueEntry3.place(relx=0.87,rely=0.58,relheight=0.04,relwidth=0.09)
        self.BlueEntry3.configure(background="white")

        self.Submit = Button (master, command=callback)
        self.Submit.place(relx=0.38,rely=0.87,height=54,width=147)
        self.Submit.configure(pady="0")
        self.Submit.configure(text='''Submit''')

        self.PointsText1 = Label (master)
        self.PointsText1.place(relx=0.02,rely=0.67,height=11,width=31)
        self.PointsText1.configure(text='''Points''')

        self.RedPoints1 = Entry (master)
        self.RedPoints1.place(relx=0.08,rely=0.67,relheight=0.04,relwidth=0.09)
        self.RedPoints1.configure(background="white")

        self.RedPoints2 = Entry (master)
        self.RedPoints2.place(relx=0.22,rely=0.67,relheight=0.04,relwidth=0.09)
        self.RedPoints2.configure(background="white")

        self.RedPoints3 = Entry (master)
        self.RedPoints3.place(relx=0.35,rely=0.67,relheight=0.04,relwidth=0.09)
        self.RedPoints3.configure(background="white")

        self.ShotsText1 = Label (master)
        self.ShotsText1.place(relx=0.02,rely=0.73,height=21,width=31)
        self.ShotsText1.configure(text='''Shots''')

        self.RedShots1 = Entry (master)
        self.RedShots1.place(relx=0.08,rely=0.73,relheight=0.04,relwidth=0.09)
        self.RedShots1.configure(background="white")

        self.RedShots2 = Entry (master)
        self.RedShots2.place(relx=0.22,rely=0.73,relheight=0.04,relwidth=0.09)
        self.RedShots2.configure(background="white")

        self.RedShots3 = Entry (master)
        self.RedShots3.place(relx=0.35,rely=0.73,relheight=0.04,relwidth=0.09)
        self.RedShots3.configure(background="white")

        self.HeightText1 = Label (master)
        self.HeightText1.place(relx=0.0,rely=0.8,height=21,width=42)
        self.HeightText1.configure(text='''Height''')

        self.RedHeight1 = Entry (master)
        self.RedHeight1.place(relx=0.08,rely=0.8,relheight=0.04,relwidth=0.09)
        self.RedHeight1.configure(background="white")

        self.RedHeight2 = Entry (master)
        self.RedHeight2.place(relx=0.22,rely=0.8,relheight=0.04,relwidth=0.09)
        self.RedHeight2.configure(background="white")

        self.RedHeight3 = Entry (master)
        self.RedHeight3.place(relx=0.35,rely=0.8,relheight=0.04,relwidth=0.09)
        self.RedHeight3.configure(background="white")

        self.PointsText2 = Label (master)
        self.PointsText2.place(relx=0.53,rely=0.67,height=21,width=39)
        self.PointsText2.configure(text='''Points''')

        self.BluePoints1 = Entry (master)
        self.BluePoints1.place(relx=0.6,rely=0.67,relheight=0.04,relwidth=0.09)
        self.BluePoints1.configure(background="white")

        self.BluePoints2 = Entry (master)
        self.BluePoints2.place(relx=0.73,rely=0.67,relheight=0.04,relwidth=0.09)

        self.BluePoints2.configure(background="white")

        self.BluePoints3 = Entry (master)
        self.BluePoints3.place(relx=0.87,rely=0.67,relheight=0.04,relwidth=0.09)
        self.BluePoints3.configure(background="white")

        self.ShotsText2 = Label (master)
        self.ShotsText2.place(relx=0.53,rely=0.73,height=21,width=35)
        self.ShotsText2.configure(text='''Shots''')

        self.BlueShots1 = Entry (master)
        self.BlueShots1.place(relx=0.6,rely=0.73,relheight=0.04,relwidth=0.09)
        self.BlueShots1.configure(background="white")

        self.BlueShots2 = Entry (master)
        self.BlueShots2.place(relx=0.73,rely=0.73,relheight=0.04,relwidth=0.09)
        self.BlueShots2.configure(background="white")

        self.BlueShots3 = Entry (master)
        self.BlueShots3.place(relx=0.87,rely=0.73,relheight=0.04,relwidth=0.09)
        self.BlueShots3.configure(background="white")

        self.HeightText2 = Label (master)
        self.HeightText2.place(relx=0.52,rely=0.8,height=21,width=42)
        self.HeightText2.configure(text='''Height''')

        self.BlueHeight1 = Entry (master)
        self.BlueHeight1.place(relx=0.6,rely=0.8,relheight=0.04,relwidth=0.09)
        self.BlueHeight1.configure(background="white")

        self.BlueHeight2 = Entry (master)
        self.BlueHeight2.place(relx=0.73,rely=0.8,relheight=0.04,relwidth=0.09)
        self.BlueHeight2.configure(background="white")

        self.BlueHeight3 = Entry (master)
        self.BlueHeight3.place(relx=0.87,rely=0.8,relheight=0.04,relwidth=0.09)
        self.BlueHeight3.configure(background="white")




def callback():
    a = w.MatchEntry.get()
    b = w.RedEntry.get()
    c = w.RedEntry1.get()
    d = w.RedEntry2.get()
    e = w.RedEntry3.get()
    f = w.BlueEntry.get()
    g = w.BlueEntry1.get()
    h = w.BlueEntry2.get()
    i = w.BlueEntry3.get()
    j = w.RedPoints1.get()
    k = w.BluePoints1.get()
    l = w.RedPoints2.get()
    m = w.BluePoints2.get()
    n = w.RedPoints3.get()
    o = w.BluePoints3.get()
    p = w.RedShots1.get()
    q = w.BlueShots1.get()
    r = w.RedShots2.get()
    s = w.BlueShots2.get()
    t = w.RedShots3.get()
    u = w.BlueShots3.get()
    v = w.RedHeight1.get()
    W = w.BlueHeight1.get()
    x = w.RedHeight2.get()
    y = w.BlueHeight2.get()
    z = w.RedHeight3.get()
    aa = w.BlueHeight3.get()
    
    print a, "\n", b, " ", f, "\n", c, d, e, "  ", g, h, i, "\n", j, l, n, "    ", k, m, o, "\n", p, r, t, "    ", q, s, u, "\n", v, x, z, "    ", W, y, aa 




if __name__ == '__main__':
    vp_start_gui()


