import sqlite3

def queryStat(q,c):

    teams = []
    stats = []

    for row in c.execute('select team,avg('+ q +') as avg_'+ q +' from teams group by team order by avg_'+ q +' desc'):
        teams.append(str(row[0]))
        stats.append(row[1])
            
    return teams, stats
    
        
