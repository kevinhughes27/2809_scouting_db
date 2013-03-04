import sqlite3
import matplotlib.pyplot as plt
import pylab

from queryStat import queryStat

conn = sqlite3.connect('scouting.db')
c = conn.cursor()

while True:
    q = raw_input('Enter a stat to query: ')

    try:
        teams, stats = queryStat(q,c)
    except:
        print 'Invalid stat'
        break

    xaxis = []
    count = 0

    for t in teams:
        xaxis.append(count)
        count += 1

    fig = plt.figure(q)
    ax = fig.add_subplot(111)
    ax.bar(xaxis, stats)
    pylab.xticks(xaxis, teams)
    fig.autofmt_xdate()
    plt.show()
    break
