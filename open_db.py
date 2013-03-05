#! /usr/bin/env python

import sqlite3

default_db = 'data/fingerlakes2013.db'

def open_db(db=default_db):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	return c, conn

