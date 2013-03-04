import sqlite3
from rankTeams import rankTeams

conn = sqlite3.connect('scouting.db')
c = conn.cursor()

rankTeams(c)

for x in c.execute('select * from rank order by score desc'):
    print x


raw_input('Press any key to continue...')
    
