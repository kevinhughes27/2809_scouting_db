import sqlite3
import matplotlib.pyplot as plt
import pylab

from open_db import open_db
from queryStat import queryStat


def main():
        c,conn = open_db()

        autoAverage(c)

        for row in c.execute('select * from auto group by team order by average desc'):
            print row

        raw_input('Press any key to continue...')
        return

def autoAverage(c):

    teams = []
    stats = []

    c.execute('drop table if exists auto')
    c.execute('''create table auto (team, average)''')

    c.execute('select team, avg(autoThree), avg(autoTwo), avg(autoOne) from teams group by team')
    result = c.fetchall()

    for row in result:
        team = row[0]
        average = (row[1]*6) + (row[2]*4) + (row[3]*2)
        i = (team, average)
        c.execute('insert into auto values (?,?)', i)

    for row in c.execute('select * from auto group by team order by average desc'):
        teams.append(str(row[0]))
        stats.append(row[1])

    return teams, stats

if __name__ == "__main__":
    main()
