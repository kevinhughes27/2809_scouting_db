import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

match = int(raw_input('Enter a Match: '))
for row in c.execute('SELECT * FROM teams'):
    if row[1] == match:
        print row
raw_input('Press any key to continue...')
