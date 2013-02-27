import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

team = int(raw_input('Enter a Team: '))
team2 = int(raw_input('Enter a Team to compare: '))

print '\n', team, '\n'

for row in c.execute('SELECT * FROM teams'):
    if row[0] == team:
        print row

print '\n', team2, '\n'

for row in c.execute('select * from teams'):
    if row[0] == team2:
        print row


raw_input('\nPress any key to continue...')
