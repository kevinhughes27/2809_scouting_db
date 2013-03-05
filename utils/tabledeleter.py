import sqlite3
from open_db import open_db

c, conn = open_db()

c.execute('DROP TABLE IF EXISTS pitScouting')
conn.commit
conn.close
