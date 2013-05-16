#! /usr/bin/env python

import sqlite3

default_db = 'Test.db'

def open_db(db=default_db):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	return c, conn

