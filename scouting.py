#Command-line database V INDEV
#C Sawyer Shipp-Wiedersprecher, Russell Dawes and Kevin Hughes

import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

while True:
    cmd = raw_input('Enter a Command: ')

    if cmd == 'input':
        while num < 7:
            
            try:
                team = int(raw_input('Team: '))
                match = int(raw_input('match: '))
                auto3 = int(raw_input('Autonomous Three Pointers: '))
                auto2 = int(raw_input('Autonomous Two Pointers: '))
                auto1 = int(raw_input('Autonomous One Pointers: '))
                five = int(raw_input('Five Pointers: '))
                three = int(raw_input('Three pointers: '))
                two = int(raw_input('Two pointers: '))
                one = int(raw_input('One Pointers: '))
                climb = int(raw_input('climb score: '))
                while climb != 10 and climb != 20 and climb != 30 and climb != 0:
                    print 'Invalid Input, climb score can only be 0, 10, 20 or 30'
                    climb = int(raw_input('climb score: '))
                row = (team,match,auto1,auto2,auto3,five,three,two,one,climb)
                c.execute('INSERT INTO teams VALUES (?,?,?,?,?,?,?,?,?,?)', row)
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
                    (Team, Match, AutoThree, AutoTwo, AutoOne,
                    FivePointers, ThreePointers, TwoPointers, OnePointers, ClimbScore)''')
        
    else:
        print 'unrecognized command'
