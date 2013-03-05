#! /usr/bin/env python

from Tkinter import *
import sqlite3
from open_db import open_db

def main():
    
    c,conn = open_db()

    team = int(raw_input('Enter Team 1: '))
    team2 = int(raw_input('Enter Team 2: '))
    team3 = int(raw_input('Enter Team 3: '))
    team4 = int(raw_input('Enter Team 4: '))
    team5 = int(raw_input('Enter Team 5: '))
		
    top = Tk()

    top.title("Compare Teams")
    top.resizable(1, 1)
    top.maxsize(4000, 4000)

    Team1Lbl = Label(top, text=team)
    Team1Lbl.grid(row=0, column=3)

    ExtraRow = Label(top, text="    ")
    ExtraRow.grid(row=10, column=0)

    Column1 = Label(top, text="Match") 
    Column1.grid(row=1, column=0)
    
    Column2 = Label(top, text="Auto Three") 
    Column2.grid(row=1, column=1)

    Column3 = Label(top, text="Auto Two") 
    Column3.grid(row=1, column=2)

    Column4 = Label(top, text="Auto One") 
    Column4.grid(row=1, column=3)

    Column5 = Label(top, text="Five") 
    Column5.grid(row=1, column=4)

    Column6 = Label(top, text="Three") 
    Column6.grid(row=1, column=5)

    Column7 = Label(top, text="Two") 
    Column7.grid(row=1, column=6)

    Column8 = Label(top, text="one") 
    Column8.grid(row=1, column=7)

    Column9= Label(top, text="climb") 
    Column9.grid(row=1, column=8)

    Column10 = Label(top, text="notes") 
    Column10.grid(row=1, column=9)

    Column11 = Label(top, text="Match") 
    Column11.grid(row=1, column=11)
    
    Column12 = Label(top, text="Auto Three") 
    Column12.grid(row=1, column=12)

    Column13 = Label(top, text="Auto Two") 
    Column13.grid(row=1, column=13)

    Column14 = Label(top, text="Auto One") 
    Column14.grid(row=1, column=14)

    Column15 = Label(top, text="Five") 
    Column15.grid(row=1, column=15)

    Column16 = Label(top, text="Three") 
    Column16.grid(row=1, column=16)

    Column17 = Label(top, text="Two") 
    Column17.grid(row=1, column=17)

    Column18 = Label(top, text="one") 
    Column18.grid(row=1, column=18)

    Column19 = Label(top, text="climb") 
    Column19.grid(row=1, column=19)

    Column20 = Label(top, text="notes") 
    Column20.grid(row=1, column=20)

    Column21 = Label(top, text="Match") 
    Column21.grid(row=1, column=22)
    
    Column22 = Label(top, text="Auto Three") 
    Column22.grid(row=1, column=23)

    Column23 = Label(top, text="Auto Two") 
    Column23.grid(row=1, column=24)

    Column24 = Label(top, text="Auto One") 
    Column24.grid(row=1, column=25)

    Column25 = Label(top, text="Five") 
    Column25.grid(row=1, column=26)

    Column26 = Label(top, text="Three") 
    Column26.grid(row=1, column=27)

    Column27 = Label(top, text="Two") 
    Column27.grid(row=1, column=28)

    Column28 = Label(top, text="one") 
    Column28.grid(row=1, column=29)

    Column29= Label(top, text="climb") 
    Column29.grid(row=1, column=30)

    Column30 = Label(top, text="notes") 
    Column30.grid(row=1, column=31)

    Column31 = Label(top, text="Match") 
    Column31.grid(row=12, column=0)
    
    Column32 = Label(top, text="Auto Three") 
    Column32.grid(row=12, column=1)

    Column33 = Label(top, text="Auto Two") 
    Column33.grid(row=12, column=2)

    Column34 = Label(top, text="Auto One") 
    Column34.grid(row=12, column=3)
    
    Column35 = Label(top, text="Five") 
    Column35.grid(row=12, column=4)

    Column36 = Label(top, text="Three") 
    Column36.grid(row=12, column=5)

    Column37 = Label(top, text="Two") 
    Column37.grid(row=12, column=6)

    Column38 = Label(top, text="one") 
    Column38.grid(row=12, column=7)

    Column39 = Label(top, text="climb") 
    Column39.grid(row=12, column=8)

    Column40 = Label(top, text="notes") 
    Column40.grid(row=12, column=9)

    Column41 = Label(top, text="Match") 
    Column41.grid(row=12, column=22)
    
    Column42 = Label(top, text="Auto Three") 
    Column42.grid(row=12, column=23)

    Column43 = Label(top, text="Auto Two") 
    Column43.grid(row=12, column=24)
    
    Column44 = Label(top, text="Auto One") 
    Column44.grid(row=12, column=25)
    
    Column45 = Label(top, text="Five") 
    Column45.grid(row=12, column=26)

    Column46 = Label(top, text="Three") 
    Column46.grid(row=12, column=27)

    Column47 = Label(top, text="Two") 
    Column47.grid(row=12, column=28)

    Column48 = Label(top, text="one") 
    Column48.grid(row=12, column=29)

    Column49 = Label(top, text="climb") 
    Column49.grid(row=12, column=30)

    Column50 = Label(top, text="notes") 
    Column50.grid(row=12, column=31)

    #team1 = Label(top, text=Team1)
    #team1.grid(row=2, column=0)

    count = 1

    for row in c.execute('SELECT * FROM teams'):
        if row[0] == team:
            count += 1
            match1 = Label(top, text=row[1])
            match1.grid(row=count, column=0)

            autoThree1 = Label(top, text=row[2])
            autoThree1.grid(row=count, column=1)

            autoTwo1 = Label(top, text=row[3])
            autoTwo1.grid(row=count, column=2)

            autoOne1 = Label(top, text=row[4])
            autoOne1.grid(row=count, column=3)

            
            five1 = Label(top, text=row[5])
            five1.grid(row=count, column=4)

            three1 = Label(top, text=row[6])
            three1.grid(row=count, column=5)

            two1 = Label(top, text=row[7])
            two1.grid(row=count, column=6)

            one1 = Label(top, text=row[8])
            one1.grid(row=count, column=7)

            climb1 = Label(top, text=row[9])
            climb1.grid(row=count, column=8)
            
    count = 1

    space = Label(top, text="       ")
    space.grid(row=2, column=10)

    space2 = Label(top, text="       ")
    space2.grid(row=2, column=21)

    space3 = Label(top, text="       ")
    space3.grid(row=2, column=32)

    space4 = Label(top, text="       ")
    space4.grid(row=2, column=43)


    Team2Lbl = Label(top, text=team2)
    Team2Lbl.grid(row=0, column=14)

    Team3Lbl = Label(top, text=team3)
    Team3Lbl.grid(row=0, column=25)

    Team4Lbl = Label(top, text=team4)
    Team4Lbl.grid(row=11, column=3)

    Team5Lbl = Label(top, text=team5)
    Team5Lbl.grid(row=11, column=25)

    
                  
    for row in c.execute('select * from teams'):
        if row[0] == team2:
            count += 1
            match2 = Label(top, text=row[1])
            match2.grid(row=count, column=9)

            autoThree2 = Label(top, text=row[2])
            autoThree2.grid(row=count, column=10)

            autoTwo2 = Label(top, text=row[3])
            autoTwo2.grid(row=count, column=11)

            autoOne2 = Label(top, text=row[4])
            autoOne2.grid(row=count, column=12)

            five2 = Label(top, text=row[5])
            five2.grid(row=count, column=13)

            three2 = Label(top, text=row[6])
            three2.grid(row=count, column=14)

            two2 = Label(top, text=row[7])
            two2.grid(row=count, column=15)

            one2 = Label(top, text=row[8])
            one2.grid(row=count, column=16)

            climb2 = Label(top, text=row[9])
            climb2.grid(row=count, column=17)

    count = 1
    
    for row in c.execute('select * from teams'):
        if row[0] == team3:
            count += 1
            match3 = Label(top, text=row[1])
            match3.grid(row=count, column=18)

            autoThree3 = Label(top, text=row[2])
            autoThree3.grid(row=count, column=19)

            autoTwo3 = Label(top, text=row[3])
            autoTwo3.grid(row=count, column=20)

            autoOne3 = Label(top, text=row[4])
            autoOne3.grid(row=count, column=21)

            five3 = Label(top, text=row[5])
            five3.grid(row=count, column=22)

            three3 = Label(top, text=row[6])
            three3.grid(row=count, column=23)

            two3 = Label(top, text=row[7])
            two3.grid(row=count, column=24)

            one3 = Label(top, text=row[8])
            one3.grid(row=count, column=25)

            climb3 = Label(top, text=row[9])
            climb3.grid(row=count, column=26)

    count = 12

    for row in c.execute('select * from teams'):
        if row[0] == team4:
            count += 1
            match4 = Label(top, text=row[1])
            match4.grid(row=count, column=0)

            autoThree4 = Label(top, text=row[2])
            autoThree4.grid(row=count, column=1)

            autoTwo4 = Label(top, text=row[3])
            autoTwo4.grid(row=count, column=2)

            autoOne4 = Label(top, text=row[4])
            autoOne4.grid(row=count, column=3)

            five4 = Label(top, text=row[5])
            five4.grid(row=count, column=4)

            three4 = Label(top, text=row[6])
            three4.grid(row=count, column=5)

            two4 = Label(top, text=row[7])
            two4.grid(row=count, column=6)

            one4 = Label(top, text=row[8])
            one4.grid(row=count, column=7)

            climb4 = Label(top, text=row[9])
            climb4.grid(row=count, column=8)

    count = 12

    for row in c.execute('select * from teams'):
        if row[0] == team5:
            count += 1
            match5 = Label(top, text=row[1])
            match5.grid(row=count, column=22)

            autoThree5 = Label(top, text=row[2])
            autoThree5.grid(row=count, column=23)

            autoTwo5 = Label(top, text=row[3])
            autoTwo5.grid(row=count, column=24)

            autoOne5 = Label(top, text=row[4])
            autoOne5.grid(row=count, column=25)

            five5 = Label(top, text=row[5])
            five5.grid(row=count, column=26)

            three5 = Label(top, text=row[6])
            three5.grid(row=count, column=27)

            two5 = Label(top, text=row[7])
            two5.grid(row=count, column=28)

            one5 = Label(top, text=row[8])
            one5.grid(row=count, column=29)

            climb5 = Label(top, text=row[9])
            climb5.grid(row=count, column=30)

    top.focus_set()
    top.mainloop()

if __name__ == "__main__":
    main()
