import sqlite3
from predictMatch import predictMatch


conn = sqlite3.connect('scouting.db')
c = conn.cursor()

p1 = int(raw_input('Enter participant red 1: '))
p2 = int(raw_input('Enter participant red 2: '))
p3 = int(raw_input('Enter participant red 3: '))
p4 = int(raw_input('Enter participant blue 1: '))
p5 = int(raw_input('Enter participant blue 2: '))
p6 = int(raw_input('Enter participant blue 3: '))

redscore, bluscore = predictMatch(c,p1,p2,p3,p4,p5,p6)


print 'Predicted result = red: ',redscore, '   Blue: ', bluscore 


raw_input('Press any key to continue...')
    
