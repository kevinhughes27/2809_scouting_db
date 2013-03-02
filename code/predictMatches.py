import sqlite3
import numpy as np
from predictMatch import predictMatch

conn = sqlite3.connect('scouting.db')
c = conn.cursor()

# copy past of the remaining matches from the schedule, no title row
# get from frclinks
schedule = np.loadtxt('schedule.csv', dtype=int, delimiter=',', usecols=[2,3,4,5,6,7])
#print schedule

# copy and past of the team ranks from frc links only first 5 columns used
ranks = np.loadtxt('frcRanks.csv', dtype=int, delimiter=',', skiprows=1, usecols=[1,2,3,4,5])
#print ranks

for row in schedule:
    blueScore, redScore = predictMatch(c,row[0],row[1],row[2],row[3],row[4],row[5])

    if(blueScore > redScore):
        print 'Match: ', row, ' blue wins', int(blueScore), 'to', int(redScore)
        idx = np.where(ranks==row[0])[0]
        ranks[idx,1] += 2

        idx = np.where(ranks==row[1])[0]
        ranks[idx,1] += 2

        idx = np.where(ranks==row[2])[0]
        ranks[idx,1] += 2

    if(redScore > blueScore):
        print 'Match: ', row, ' red wins', int(redScore), 'to', int(blueScore)
        idx = np.where(ranks==row[3])[0]
        ranks[idx,1] += 2

        idx = np.where(ranks==row[4])[0]
        ranks[idx,1] += 2

        idx = np.where(ranks==row[5])[0]
        ranks[idx,1] += 2

#print ranks
ranks = ranks[np.lexsort((ranks[:,0], ranks[:,1]))]
ranks = np.flipud(ranks)
#print ranks
np.savetxt('newRanks.csv', ranks, fmt='%d', delimiter=',')
raw_input('Press Enter to Continue...')
