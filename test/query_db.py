#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import sys
import urllib2

if len(sys.argv) != 5:
    print("Usage query_db.py <db host> <db name> <db user> <db pass>")
    sys.exit(1)
    
con = None

try:
    app_id = 335
    table = "app"

    #NOTE: em task_run, info eh uma string
    #NOTE: em task, info eh um dicionario

    conn_string = "host='"+ sys.argv[1] + "' dbname='" + sys.argv[2] + "' user='" + sys.argv[3] + "' password='" + sys.argv[4] + "'"
    con = psycopg2.connect(conn_string)
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cursor.execute("SELECT id FROM " + table)
    
    rows = cursor.fetchall()
    for row in rows:
        print "row"
        print row
        
except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    if con:
        con.close()