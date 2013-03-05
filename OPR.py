#! /usr/bin/env python

# genOPR.py
#(C) Sawyer Shipp-Wiedersprecher, Russell Dawes and Kevin Hughes

import numpy as np
import sqlite3
from open_db import open_db

def main():
	teamOPR = genOPR()
	for t in teamOPR:
		print t

	raw_input('press enter to continue...')
	return

"""
Generates the Offensive Power Rating(OPR) of each team
"""
def genOPR():
    
    c = open_db()
    
    count = 0
    rowMax = 0
    teams = []
    colour = 0

    # team count
    for row in c.execute('select team from teams group by team'):
        count += 1
    teamCount = count
    # match count
    for row in c.execute('select match from teams order by match desc'):
        matchCount = row[0]
        break
    # team index
    for row in c.execute('select team from teams group by team order by team'):
        teams.append(row[0])

    # participation matrix
    P = np.zeros((matchCount*2,teamCount),np.float)
    for row in c.execute('select team,match,colour from teams order by match'):
        i = teams.index(row[0])
        if row[2] == 1:
            P[((row[1]-1)*2)+1][i] = 1
        else:
            P[(row[1]-1)*2][i] = 1
    
    #np.savetxt("pMat.csv", P, delimiter=',')

    #score vector
    S = np.zeros((matchCount*2,1),np.float)
    counter = 0
    for row in c.execute('select * from teams order by match'):
        if row[9] == 1:
            S[((row[1]-1)*2)+1] += (row[2] + (row[3]*5) + (row[4]*3) + (row[5]*2) + row[6] + row[7])
        else:
            S[(row[1]-1)*2] += (row[2] + (row[3]*5) + (row[4]*3) + (row[5]*2) + row[6] + row[7])

    # OPR calc
    opr = np.linalg.lstsq(P ,S)

    teamOPR = []
    for i, v in enumerate(teams):
        teamOPR.append([v,float(opr[0][i])])

    teamOPR.sort(key=lambda tup: tup[1], reverse=True)


    return teamOPR    
    
if __name__ == "__main__":
    main()
