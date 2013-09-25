#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import sys
import urllib2

if len(sys.argv) != 6:
	print("Usage load_t3_tasks.py <db host> <db name> <db user> <db pass> <app id>")
	sys.exit(1)

con = None

try:
    app_id = sys.argv[5]
    app_id_next = str(int(app_id) + 1)
    conn_string = "host='"+ sys.argv[1] + "' dbname='" + sys.argv[2] + "' user='" + sys.argv[3] + "' password='" + sys.argv[4] + "'" 
    con = psycopg2.connect(conn_string) 
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("DELETE FROM task WHERE app_id =  " + app_id_next)
    print "All tasks with app_id = " + app_id_next + " were deleted with success"
    cursor.execute("SELECT id FROM task WHERE app_id = " + app_id + " and state = 'completed'")
    records = cursor.fetchall()

    for i in records:
	request = "http://localhost/mb/api/" + str(i["id"]) + "/done"
	print("Task ID: " + str(i["id"]) + " Created: " + urllib2.urlopen(request).read())

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
