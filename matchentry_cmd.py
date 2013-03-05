#! /usr/bin/env python

#Command-line database V INDEV
#C Sawyer Shipp-Wiedersprecher, Russell Dawes and Kevin Hughes

import sqlite3
from open_db import open_db

def main():

	c,conn = open_db()

	while True:
		cmd = raw_input('Enter a Command: ')

		if cmd == 'input':
		    line = 1
		    expectedScore = 0
		    while line < 7:
		        try:
		            team = int(raw_input('Team: '))
		            match = int(raw_input('match: '))
		            colour = int(raw_input('Alliance Color: (0 for Red 1 For Blue)'))
		            autoThree = int(raw_input('Autonomous Three Pointers: '))
		            autoTwo = int(raw_input('Autonomous Two Pointers: '))
		            autoOne = int(raw_input('Autonomous One Pointers: '))
		            five = int(raw_input('Five Pointers: '))
		            three = int(raw_input('Three pointers: '))
		            two = int(raw_input('Two pointers: '))
		            one = int(raw_input('One Pointers: '))
		            climb = int(raw_input('climb score: '))
		            while climb != 10 and climb != 20 and climb != 30 and climb != 0:
		                print 'Invalid Input, climb score can only be 0, 10, 20 or 30'
		                climb = int(raw_input('climb score: '))
		            notes = str(raw_input('notes: '))
		            expectedScore = expectedScore + (autoThree*6) + (autoTwo*4) + (autoOne*2) + (five*5) + (three*3) + (two*2) + one + climb
		            if line == 3:
		                redScore = int(raw_input('Red Team total: '))
		                if expectedScore != redScore:
		                    print 'User Error: Score inputs do not match!'
		                expectedScore = 0
		            if line == 6:
		                bluScore = int(raw_input('Blue Team Score: '))
		                if expectedScore != bluScore:
		                    print 'User Error: Score inputs do not match'
		                expectedScore = 0
		            row = (team,match,autoThree,autoTwo,autoOne,five,three,two,one,climb,notes,colour)
		            c.execute('INSERT INTO teams VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', row)
		            line += 1 
		        except ValueError:
		            print 'invalid number'

		elif cmd == 'output':
		    for row in c.execute('SELECT * FROM teams ORDER BY team'):
		        print row

		elif cmd == 'save':
		    conn.commit()
		    conn.close()
		    break

		elif cmd == 'clear':
		    c.execute('DROP TABLE if exists teams')
		    c.execute('''CREATE TABLE teams
		                (team, match, autoThree, autoTwo, autoOne, five, three,
		                two, one, climb, notes, colour)''')
		    
		else:
		    print 'unrecognized command'
    return
    
if __name__ == "__main__":
    main()
