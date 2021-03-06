#! /usr/bin/env python

import sqlite3
import matplotlib.pyplot as plt
import pylab
from rankTeams import rankTeams
from open_db import open_db

c,conn = open_db()

rankTeams(c)

xaxis = []
count = 0
stats = []
teams = []

for t in c.execute('select team from rank'):
    xaxis.append(count)
    count += 1

for row in c.execute('select * from rank order by score desc'):

    stats.append(row[1])
    teams.append(row[0])

fig = plt.figure('ranking')
ax = fig.add_subplot(111)
ax.bar(xaxis, stats)
pylab.xticks(xaxis, teams)
fig.autofmt_xdate()
plt.show()
