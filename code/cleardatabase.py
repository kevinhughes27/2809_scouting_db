import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()
c.execute('''DROP TABLE if exists teams''')
