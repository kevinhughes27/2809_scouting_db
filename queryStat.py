import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

q = raw_input('Enter a stat to query: ')

if q == 'AutoThree':
    for row in c.execute('select team,avg(AutoThree) as avg_three from teams group by team'):
        print row

if q == 'AutoTwo':
    for row in c.execute('select team,avg(AutoTwo) as avg_three from teams group by team'):
        print row
        
if q == 'AutoOne':
    for row in c.execute('select team,avg(AutoOne) as avg_three from teams group by team'):
        print row

if q == 'FivePointers':
    for row in c.execute('select team,avg(FivePointers) as avg_three from teams group by team'):
        print row
    
if q == 'ThreePointers':
    for row in c.execute('select team,avg(ThreePointers) as avg_three from teams group by team'):
        print row

if q == 'TwoPointers':
    for row in c.execute('select team,avg(TwoPointers) as avg_three from teams group by team'):
        print row

if q == 'OnePointers':
    for row in c.execute('select team,avg(OnePointers) as avg_three from teams group by team'):
        print row

if q == 'ClimbScore':
    for row in c.execute('select team,avg(ClimbScore) as avg_three from teams group by team'):
        print row
        
