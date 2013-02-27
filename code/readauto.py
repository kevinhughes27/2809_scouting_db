import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM teams ORDER BY auto'):
    print row
