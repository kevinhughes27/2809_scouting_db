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

    c.execute('select team,avg(autoThree), avg(autoTwo), avg(autoOne),avg(five),avg(three),avg(two),avg(one),avg(climb) from teams group by team')
    result = c.fetchall()

    for row in result:
        team = row[0]
        score = (row[1]*6) + (row[2]*4) + (row[3]*2) + (row[4]*5) + (row[5]*3) + (row[6]*2) + (row[7]) + (row[8])
        i = (team, score)
        c.execute('insert into rank values (?,?)', i)

if __name__ == "__main__":
    main()
