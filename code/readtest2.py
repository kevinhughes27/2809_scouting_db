import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

for row in c.execute('SELECT * FROM teams WHERE team == 1111 ORDER BY team'):
    print row
