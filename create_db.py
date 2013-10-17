#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys

if len(sys.argv) != 5:
	print("Usage create_db.py <db host> <db name> <db user> <db pass>")
	sys.exit(1)

con = None

try:
    
    conn_string = "host='"+ sys.argv[1] + "' dbname='" + sys.argv[2] + "' user='" + sys.argv[3] + "' password='" + sys.argv[4] + "'" 
    con = psycopg2.connect(conn_string) 
    cursor = con.cursor()
    cursor.execute(open("tt4dbcreate.sql", "r").read())
    con.commit()

    cursor.execute(open("factsTableCreate.sql", "r").read())
    con.commit()

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1) 

finally:
    
    if con:
        con.close()
