import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

team = int(raw_input('Enter a Team: '))
for row in c.execute('SELECT * FROM teams'):
    if row[0] == team:
        print row
raw_input('Press any key to continue...')
