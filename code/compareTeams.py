from Tkinter import *
import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

team = int(raw_input('Enter Team 1: '))
team2 = int(raw_input('Enter Team 2: '))
team3 = int(raw_input('Enter Team 3: '))
team4 = int(raw_input('Enter Team 4: '))
team5 = int(raw_input('Enter Team 5: '))

#print '\n', team, '\n'
        
#print '\n', team2, '\n'

def main():
    top = Tk()

    top.title("Compare Teams")
    top.resizable(1, 1)
    top.maxsize(2000, 2000)

    Team1Lbl = Label(top, text=team)
    Team1Lbl.grid(row=0, column=3)

    Column1 = Label(top, text="Match") 
    Column1.grid(row=1, column=0)
    
    Column2 = Label(top, text="Auto") 
    Column2.grid(row=1, column=1)

    Column3 = Label(top, text="Five") 
    Column3.grid(row=1, column=2)

    Column4 = Label(top, text="Three") 
    Column4.grid(row=1, column=3)

    Column5 = Label(top, text="Two") 
    Column5.grid(row=1, column=4)

    Column6 = Label(top, text="one") 
    Column6.grid(row=1, column=5)

    Column7= Label(top, text="climb") 
    Column7.grid(row=1, column=6)

    Column8 = Label(top, text="notes") 
    Column8.grid(row=1, column=7)

    Column9 = Label(top, text="Match") 
    Column9.grid(row=1, column=9)
    
    Column10 = Label(top, text="Auto") 
    Column10.grid(row=1, column=10)

    Column11 = Label(top, text="Five") 
    Column11.grid(row=1, column=11)

    Column12 = Label(top, text="Three") 
    Column12.grid(row=1, column=12)

    Column13 = Label(top, text="Two") 
    Column13.grid(row=1, column=13)

    Column14 = Label(top, text="one") 
    Column14.grid(row=1, column=14)

    Column15 = Label(top, text="climb") 
    Column15.grid(row=1, column=15)

    Column15 = Label(top, text="notes") 
    Column15.grid(row=1, column=16)

    Column16 = Label(top, text="Match") 
    Column16.grid(row=1, column=18)
    
    Column17 = Label(top, text="Auto") 
    Column17.grid(row=1, column=19)

    Column18 = Label(top, text="Five") 
    Column18.grid(row=1, column=20)

    Column19 = Label(top, text="Three") 
    Column19.grid(row=1, column=21)

    Column20 = Label(top, text="Two") 
    Column20.grid(row=1, column=22)

    Column21 = Label(top, text="one") 
    Column21.grid(row=1, column=23)

    Column22= Label(top, text="climb") 
    Column22.grid(row=1, column=24)

    Column23 = Label(top, text="notes") 
    Column23.grid(row=1, column=25)

    Column24 = Label(top, text="Match") 
    Column24.grid(row=1, column=27)
    
    Column25 = Label(top, text="Auto") 
    Column25.grid(row=1, column=28)

    Column26 = Label(top, text="Five") 
    Column26.grid(row=1, column=29)

    Column27 = Label(top, text="Three") 
    Column27.grid(row=1, column=30)

    Column28 = Label(top, text="Two") 
    Column28.grid(row=1, column=31)

    Column29 = Label(top, text="one") 
    Column29.grid(row=1, column=32)

    Column30 = Label(top, text="climb") 
    Column30.grid(row=1, column=33)

    Column31 = Label(top, text="notes") 
    Column31.grid(row=1, column=34)

    Column32 = Label(top, text="Match") 
    Column32.grid(row=1, column=36)
    
    Column33 = Label(top, text="Auto") 
    Column33.grid(row=1, column=37)

    Column34 = Label(top, text="Five") 
    Column34.grid(row=1, column=38)

    Column35 = Label(top, text="Three") 
    Column35.grid(row=1, column=39)

    Column36 = Label(top, text="Two") 
    Column36.grid(row=1, column=40)

    Column37 = Label(top, text="one") 
    Column37.grid(row=1, column=41)

    Column38 = Label(top, text="climb") 
    Column38.grid(row=1, column=42)

    Column39 = Label(top, text="notes") 
    Column39.grid(row=1, column=43)

    #team1 = Label(top, text=Team1)
    #team1.grid(row=2, column=0)

    count = 1

    for row in c.execute('SELECT * FROM teams'):
        if row[0] == team:
            count += 1
            match1 = Label(top, text=row[1])
            match1.grid(row=count, column=0)

            auto1 = Label(top, text=row[2])
            auto1.grid(row=count, column=1)

            five1 = Label(top, text=row[3])
            five1.grid(row=count, column=2)

            three1 = Label(top, text=row[4])
            three1.grid(row=count, column=3)

            two1 = Label(top, text=row[5])
            two1.grid(row=count, column=4)

            one1 = Label(top, text=row[6])
            one1.grid(row=count, column=5)

            climb1 = Label(top, text=row[7])
            climb1.grid(row=count, column=6)
            
    count = 1

    space = Label(top, text="       ")
    space.grid(row=2, column=8)

    space2 = Label(top, text="       ")
    space2.grid(row=2, column=17)

    space3 = Label(top, text="       ")
    space3.grid(row=2, column=26)

    space4 = Label(top, text="       ")
    space4.grid(row=2, column=35)


    Team2Lbl = Label(top, text=team2)
    Team2Lbl.grid(row=0, column=12)

    Team3Lbl = Label(top, text=team3)
    Team3Lbl.grid(row=0, column=21)

    Team4Lbl = Label(top, text=team4)
    Team4Lbl.grid(row=0, column=30)

    Team5Lbl = Label(top, text=team5)
    Team5Lbl.grid(row=0, column=39)

    
                  
    for row in c.execute('select * from teams'):
        if row[0] == team2:
            count += 1
            match2 = Label(top, text=row[1])
            match2.grid(row=count, column=9)

            auto2 = Label(top, text=row[2])
            auto2.grid(row=count, column=10)

            five2 = Label(top, text=row[3])
            five2.grid(row=count, column=11)

            three2 = Label(top, text=row[4])
            three2.grid(row=count, column=12)

            two2 = Label(top, text=row[5])
            two2.grid(row=count, column=13)

            one2 = Label(top, text=row[6])
            one2.grid(row=count, column=14)

            climb2 = Label(top, text=row[7])
            climb2.grid(row=count, column=15)

    count = 1
    
    for row in c.execute('select * from teams'):
        if row[0] == team3:
            count += 1
            match3 = Label(top, text=row[1])
            match3.grid(row=count, column=18)

            auto3 = Label(top, text=row[2])
            auto3.grid(row=count, column=19)

            five3 = Label(top, text=row[3])
            five3.grid(row=count, column=20)

            three3 = Label(top, text=row[4])
            three3.grid(row=count, column=21)

            two3 = Label(top, text=row[5])
            two3.grid(row=count, column=22)

            one3 = Label(top, text=row[6])
            one3.grid(row=count, column=23)

            climb3 = Label(top, text=row[7])
            climb3.grid(row=count, column=24)

    count = 1

    for row in c.execute('select * from teams'):
        if row[0] == team4:
            count += 1
            match4 = Label(top, text=row[1])
            match4.grid(row=count, column=27)

            auto4 = Label(top, text=row[2])
            auto4.grid(row=count, column=28)

            five4 = Label(top, text=row[3])
            five4.grid(row=count, column=29)

            three4 = Label(top, text=row[4])
            three4.grid(row=count, column=30)

            two4 = Label(top, text=row[5])
            two4.grid(row=count, column=31)

            one4 = Label(top, text=row[6])
            one4.grid(row=count, column=32)

            climb4 = Label(top, text=row[7])
            climb4.grid(row=count, column=33)

    count = 1

    for row in c.execute('select * from teams'):
        if row[0] == team5:
            count += 1
            match5 = Label(top, text=row[1])
            match5.grid(row=count, column=36)

            auto5 = Label(top, text=row[2])
            auto5.grid(row=count, column=37)

            five5 = Label(top, text=row[3])
            five5.grid(row=count, column=38)

            three5 = Label(top, text=row[4])
            three5.grid(row=count, column=39)

            two5 = Label(top, text=row[5])
            two5.grid(row=count, column=40)

            one5 = Label(top, text=row[6])
            one5.grid(row=count, column=41)

            climb5 = Label(top, text=row[7])
            climb5.grid(row=count, column=42)
    
    #otherteam = Label(top, text=row2)
    #otherteam.grid(row=2, column=2)

    top.focus_set()
    top.mainloop()

main()
