import sys
import sqlite3
from open_db import open_db

'''
Usage
python merge_db.py <db1> <db2>

merges db2 into db1
'''

def main():

	c1,conn1 = open_db(sys.argv[1])
	c2,conn2 = open_db(sys.argv[2])

	for row in c2.execute('select * from teams'):
		print 'Extracting row'
		print 'Injecting row'
		c1.execute('insert into teams values (?,?,?,?,?,?,?,?,?)', row)

	print 'done'

	print 'saving...'
	conn1.commit()
	print 'closing...'
	conn1.close()
	conn2.close()
	
if __name__ == "__main__":
    main()
