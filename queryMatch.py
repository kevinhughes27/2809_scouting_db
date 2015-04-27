#! /usr/bin/env python

import sqlite3
from open_db import open_db

def main():
    c = open_db()
    match = int(raw_input('Enter a Match: '))

    data = queryMatch(match,c)

    for d in data:
        print d

    raw_input('Press any key to continue...')
    return

def queryMatch(match,c):

    data = []

    for row in c.execute('SELECT * FROM teams'):
        if row[1] == match:
            data.append(row)

    return data

if __name__ == "__main__":
    main()
