from Tkinter import *
import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

team = int(raw_input('Enter a Team: '))

#print '\n', team, '\n'
        
#print '\n', team2, '\n'

def main():
    top = Tk()

    top.title("queryTeam")
    top.resizable(1, 1)
    top.maxsize(2000, 2000)

    Team1Lbl = Label(top, text=team)
    Team1Lbl.grid(row=0, column=3, sticky=N+E+W+S)

    Column1 = Label(top, text="Match") 
    Column1.grid(row=1, column=0, sticky=N+E+W+S)
    
    Column2 = Label(top, text="Auto") 
    Column2.grid(row=1, column=1, sticky=N+E+W+S)

    Column3 = Label(top, text="Five") 
    Column3.grid(row=1, column=2, sticky=N+E+W+S)

    Column4 = Label(top, text="Three") 
    Column4.grid(row=1, column=3, sticky=N+E+W+S)

    Column5 = Label(top, text="Two") 
    Column5.grid(row=1, column=4, sticky=N+E+W+S)

    Column6 = Label(top, text="one") 
    Column6.grid(row=1, column=5, sticky=N+E+W+S)

    Column7= Label(top, text="climb") 
    Column7.grid(row=1, column=6, sticky=N+E+W+S)

    Column8 = Label(top, text="notes") 
    Column8.grid(row=1, column=7, sticky=N+E+W+S)

    #team1 = Label(top, text=Team1)
    #team1.grid(row=2, column=0)

    count = 1

    for row in c.execute('SELECT * FROM teams'):
        if row[0] == team:
            count += 1
            match1 = Label(top, text=row[1])
            match1.grid(row=count, column=0, sticky=N+E+W+S)

            auto1 = Label(top, text=row[2])
            auto1.grid(row=count, column=1, sticky=N+E+W+S)

            five1 = Label(top, text=row[3])
            five1.grid(row=count, column=2, sticky=N+E+W+S)

            three1 = Label(top, text=row[4])
            three1.grid(row=count, column=3, sticky=N+E+W+S)

            two1 = Label(top, text=row[5])
            two1.grid(row=count, column=4, sticky=N+E+W+S)

            one1 = Label(top, text=row[6])
            one1.grid(row=count, column=5, sticky=N+E+W+S)

            climb1 = Label(top, text=row[7])
            climb1.grid(row=count, column=6, sticky=N+E+W+S)

    

    space = Label(top, text="       ")
    space.grid(row=2, column=8, sticky=N+E+W+S)

    #space2 = Label(top, text="      ")
    #space2.grid(row=2, column=1)
    
    #otherteam = Label(top, text=row2)
    #otherteam.grid(row=2, column=2)

    top.focus_set()
    top.mainloop()

main()
