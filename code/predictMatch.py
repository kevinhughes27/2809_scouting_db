from rankTeams import rankTeams

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
