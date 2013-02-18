import sqlite3
from queryStat import queryStat

conn = sqlite3.connect('scouting.db')
c = conn.cursor()

q = raw_input('Enter a stat to query: ')

teams, stats = queryStat(q,c)

for i, v in enumerate(teams):
    print v, stats[i]

raw_input('Press enter to continue...')
    
    
