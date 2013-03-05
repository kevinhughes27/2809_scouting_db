#! /usr/bin/env python

#graphOPR.py
#by Sawyer Shipp-Wiedersprecher, Russell Dawes and Kevin Hughes

#import libraries and python scripts
import matplotlib.pyplot as plt
import pylab
from OPR import genOPR

#init variables
teamOPR = genOPR()
teams = []
OPR = []
xaxis = []
count = 0

#plot data
for row in teamOPR:
    xaxis.append(count)
    teams.append(row[0])
    OPR.append(row[1])
    count += 1

fig = plt.figure()
ax = fig.add_subplot(111)
rects1 = ax.bar(xaxis, OPR)
pylab.xticks(xaxis, teams)
fig.autofmt_xdate()

#label bar height
def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%float(height),
                ha='center', va='bottom')

autolabel(rects1)
plt.show()
    
        
