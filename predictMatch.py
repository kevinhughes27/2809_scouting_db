#! /usr/bin/env python

import sys
import sqlite3
import numpy as np

from open_db import open_db
from rankTeams import rankTeams

'''
Usage
python predictMatch.py - will ask you which teams are playing and provide the expected result

python predictMatch.py <schedule.csv> <frc_ranks.csv> - will predict the matches in the schedule file and update the frc ranks in a new file named newRanks.csv
'''

def main():
	c,conn = open_db()

	if(len(sys.argv) == 1):
		p1 = int(raw_input('Enter participant red 1: '))
		p2 = int(raw_input('Enter participant red 2: '))
		p3 = int(raw_input('Enter participant red 3: '))
		p4 = int(raw_input('Enter participant blue 1: '))
		p5 = int(raw_input('Enter participant blue 2: '))
		p6 = int(raw_input('Enter participant blue 3: '))

		redscore, bluscore = predictMatch(c,p1,p2,p3,p4,p5,p6)

		print 'Predicted result = red: ',redscore, '   Blue: ', bluscore 

		raw_input('Press any key to continue...')
		return
	
	elif (len(sys.argv) == 3):
		schedule_csv = sys.argv[1]
		frc_ranks_csv = sys.argv[2]
		
		# copy past of the remaining matches from the schedule, no title row
		# get from frclinks
		schedule = np.loadtxt(schedule_csv, dtype=int, delimiter=',', usecols=[2,3,4,5,6,7])
		#print schedule

		# copy and past of the team ranks from frc links only first 5 columns used
		ranks = np.loadtxt(frc_ranks_csv, dtype=int, delimiter=',', skiprows=1, usecols=[1,2,3,4,5])
		#print ranks
		
		for row in schedule:
			redScore, blueScore = predictMatch(c,row[0],row[1],row[2],row[3],row[4],row[5])

			if(redScore > blueScore):
				print 'Match: ', row, ' red wins', int(redScore), 'to', int(blueScore)
				idx = np.where(ranks==row[0])[0]
				ranks[idx,1] += 2

				idx = np.where(ranks==row[1])[0]
				ranks[idx,1] += 2

				idx = np.where(ranks==row[2])[0]
				ranks[idx,1] += 2

			if(blueScore > redScore):
				print 'Match: ', row, ' blue wins', int(blueScore), 'to', int(redScore)
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
		return
	
def predictMatch(c,p1,p2,p3,p4,p5,p6):
    teams = []
    score = []

    rankTeams(c)

    for row in c.execute('select * from rank order by team'):
        teams.append(row[0])
        score.append(row[1])

    i1 = teams.index(p1)
    i2 = teams.index(p2)
    i3 = teams.index(p3)
    i4 = teams.index(p4)
    i5 = teams.index(p5)
    i6 = teams.index(p6)

    redScore = score[i1] + score[i2] + score[i3]
    blueScore = score[i4] + score[i5] + score[i6]

    return redScore, blueScore
    
if __name__ == "__main__":
    main()
