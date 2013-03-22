import sqlite3
import matplotlib.pyplot as plt
import pylab

from open_db import open_db
from autoAverage import autoAverage

c,conn = open_db()

while True:

    teams, stats = autoAverage(c)
    
    xaxis = []
    count = 0

    for t in teams:
        xaxis.append(count)
        count += 1

    fig = plt.figure('auto')
    ax = fig.add_subplot(111)
    ax.bar(xaxis, stats)
    pylab.xticks(xaxis, teams)
    fig.autofmt_xdate()
    plt.show()
    break
