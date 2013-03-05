#! /usr/bin/env python

import sqlite3
from open_db import open_db

def main():
	c,conn = open_db()

	rankTeams(c)

	for x in c.execute('select * from rank order by score desc'):
    	print x

	raw_input('Press any key to continue...')
	return

def rankTeams(c):
    c.execute('drop table if exists rank')
    c.execute('''create table rank (team, score)''')

    c.execute('select team,avg(auto),avg(five),avg(three),avg(two),avg(one),avg(climb) from teams group by team')
    result = c.fetchall()

    for row in result:
        team = row[0]
        score = (row[1]) + (row[2]*5) + (row[3]*3) + (row[4]*2) + (row[5]) + (row[6])
        i = (team, score)
        c.execute('insert into rank values (?,?)', i)
        
if __name__ == "__main__":
    main()
