from Tkinter import *
import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

team = int(raw_input('Enter a Team: '))
team2 = int(raw_input('Enter a Team to compare: '))

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

    

    space = Label(top, text="       ")
    space.grid(row=2, column=8)

    #space2 = Label(top, text="      ")
    #space2.grid(row=2, column=1)

    Team2Lbl = Label(top, text=team2)
    Team2Lbl.grid(row=0, column=12)

    count = 1
                  
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
    
    #otherteam = Label(top, text=row2)
    #otherteam.grid(row=2, column=2)

    top.focus_set()
    top.mainloop()

main()
