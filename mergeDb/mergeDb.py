import sqlite3
conn1 = sqlite3.connect('file1/scouting.db')
conn2 = sqlite3.connect('file2/scouting.db')
c1 = conn1.cursor()
c2 = conn2.cursor()

for row in c2.execute('select * from teams'):
    c1.execute('insert into teams values (?,?,?,?,?,?,?,?,?)', row)

conn1.commit()
conn1.close()
conn2.close()
