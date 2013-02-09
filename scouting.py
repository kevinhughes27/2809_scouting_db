#Command-line database V INDEV
#C Sawyer Shipp-Wiedersprecher, Russell Dawes and Kevin Hughes

import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

while True:
    cmd = raw_input('Enter a Command: ')

    if cmd == 'input':
        line = 1
        expectedScore = 0
        while line < 7:
            try:
                team = int(raw_input('Team: '))
                match = int(raw_input('match: '))
                autoScore = int(raw_input('Autonomous Score: '))
                five = int(raw_input('Five Pointers: '))
                three = int(raw_input('Three pointers: '))
                two = int(raw_input('Two pointers: '))
                one = int(raw_input('One Pointers: '))
                climb = int(raw_input('climb score: '))
                while climb != 10 and climb != 20 and climb != 30 and climb != 0:
                    print 'Invalid Input, climb score can only be 0, 10, 20 or 30'
                    climb = int(raw_input('climb score: '))
                notes = str(raw_input('notes: '))
                if line == 3:
                    redScore = int(raw_input('Red Team total: '))
                    expectedScore = 0
                if line == 6:
                    bluScore = int(raw_input('Blu Team Score: '))
                    if expectedScore == bluScore:
                        expectedScore = 0
                    else:
                        print 'User Error: Score inputs do not match'
                row = (team,match,autoScore,five,three,two,one,climb,notes)
                expectedScore = expectedScore + autoScore + (five*5) + (three*3) + (two*2) + one + climb
                c.execute('INSERT INTO teams VALUES (?,?,?,?,?,?,?,?,?)', row)
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
                    (team, match, auto, five, three,
                    two, one, climb, notes)''')
        
    else:
        print 'unrecognized command'
