import sqlite3
conn1 = sqlite3.connect('file1/scouting.db')
conn2 = sqlite3.connect('file2/scouting.db')
c1 = conn1.cursor()
c2 = conn2.cursor()

for row in c2.execute('select * from teams'):
    print 'Extracting row'
    print 'Injecting row'
    c1.execute('insert into teams values (?,?,?,?,?,?,?,?,?)', row)

print 'done'

print 'saving...'
conn1.commit()
print 'closing...'
conn1.close()
conn2.close()
