#! /usr/bin/env python

import sqlite3
from open_db import open_db

def main():
	c,conn = open_db()
	q = raw_input('Enter a stat to query: ')
	
	teams, stats = queryStat(q,c)

	for i, v in enumerate(teams):
		print v, stats[i]

	raw_input('Press enter to continue...')
	return

def queryStat(q,c):

    teams = []
    stats = []

    for row in c.execute('select team,avg('+ q +') as avg_'+ q +' from teams group by team order by avg_'+ q +' desc'):
        teams.append(str(row[0]))
        stats.append(row[1])
            
    return teams, stats
    
if __name__ == "__main__":
    main()
