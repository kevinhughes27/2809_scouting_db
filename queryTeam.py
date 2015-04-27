#! /usr/bin/env python

from Tkinter import *
import sqlite3
from open_db import open_db


def main():
    c, conn = open_db()
    team = int(raw_input('Enter a Team: '))

    top = Tk()

    top.title("queryTeam")
    top.resizable(1, 1)
    top.maxsize(2000, 2000)

    Team1Lbl = Label(top, text=team)
    Team1Lbl.grid(row=0, column=3, sticky=N+E+W+S)

    Column1 = Label(top, text="Match")
    Column1.grid(row=1, column=0, sticky=N+E+W+S)

    Column2 = Label(top, text="AutoThree")
    Column2.grid(row=1, column=1, sticky=N+E+W+S)

    Column2 = Label(top, text="AutoTwo")
    Column2.grid(row=1, column=2, sticky=N+E+W+S)

    Column2 = Label(top, text="AutoOne")
    Column2.grid(row=1, column=3, sticky=N+E+W+S)

    Column3 = Label(top, text="Five")
    Column3.grid(row=1, column=4, sticky=N+E+W+S)

    Column4 = Label(top, text="Three")
    Column4.grid(row=1, column=5, sticky=N+E+W+S)

    Column5 = Label(top, text="Two")
    Column5.grid(row=1, column=6, sticky=N+E+W+S)

    Column6 = Label(top, text="one")
    Column6.grid(row=1, column=7, sticky=N+E+W+S)

    Column7= Label(top, text="climb")
    Column7.grid(row=1, column=8, sticky=N+E+W+S)

    Column8 = Label(top, text="notes")
    Column8.grid(row=1, column=9, sticky=N+E+W+S)

    count = 1

    for row in c.execute('select * from teams'):
        if row[0] == team:
            count += 1
            match1 = Label(top, text=row[1])
            match1.grid(row=count, column=0, sticky=N+E+W+S)

            autoThree1 = Label(top, text=row[2])
            autoThree1.grid(row=count, column=1, sticky=N+E+W+S)

            autoTwo1 = Label(top, text=row[3])
            autoTwo1.grid(row=count, column=2, sticky=N+E+W+S)

            autoOne1 = Label(top, text=row[4])
            autoOne1.grid(row=count, column=3, sticky=N+E+W+S)

            five1 = Label(top, text=row[5])
            five1.grid(row=count, column=4, sticky=N+E+W+S)

            three1 = Label(top, text=row[6])
            three1.grid(row=count, column=5, sticky=N+E+W+S)

            two1 = Label(top, text=row[7])
            two1.grid(row=count, column=6, sticky=N+E+W+S)

            one1 = Label(top, text=row[8])
            one1.grid(row=count, column=7, sticky=N+E+W+S)

            climb1 = Label(top, text=row[9])
            climb1.grid(row=count, column=8, sticky=N+E+W+S)

    top.focus_set()
    top.mainloop()

def main_cmd():
    c, conn = open_db()
    team = int(raw_input('Enter a Team: '))

    for row in c.execute('SELECT * FROM teams'):
        if row[0] == team:
            print row

    raw_input('Press any key to continue...')
    return

if __name__ == "__main__":
    main()
