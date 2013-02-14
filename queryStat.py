import sqlite3
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

q = raw_input('Enter a stat to query: ')

if q == 'auto':
    for row in c.execute('select team,avg(auto) as avg_auto from teams group by team order by avg_auto desc'):
        print row

if q == 'five':
    for row in c.execute('select team,avg(five) as avg_five from teams group by team order by avg_five desc'):
        print row
    
if q == 'three':
    for row in c.execute('select team,avg(three) as avg_three from teams group by team order by avg_three desc'):
        print row

if q == 'two':
    for row in c.execute('select team,avg(two) as avg_two from teams group by team order by avg_two desc'):
        print row

if q == 'one':
    for row in c.execute('select team,avg(one) as avg_one from teams group by team order by avg_one desc'):
        print row

if q == 'climb':
    for row in c.execute('select team,avg(climb) as avg_climb from teams group by team order by avg_climb desc'):
        print row

raw_input('Press any key to continue...')
        
