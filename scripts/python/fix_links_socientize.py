#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2.extras
import sys

def replaceInfo(info):
    print "info before:"
    print info
    info[1] = info[1].replace("http://alfa.pybossa.socientize.eu", "https://localhost")
    info[1] = info[1].replace("https://alfa.pybossa.socientize.eu", "https://localhost")
    
    return info

if len(sys.argv) != 5:
    print("Usage fix_links_socientize.py <db host> <db name> <db user> <db pass>")
    sys.exit(1)

con = None

try:
    #app_id = 335
    table = "task"
    task_type = "tt4"
    
    # tt3 - task e taskrun
    # tt4 - task
    #NOTE: em task_run, info eh uma string
    #NOTE: em task, info eh um dicionario

    conn_string = "host='"+ sys.argv[1] + "' dbname='" + sys.argv[2] + "' user='" + sys.argv[3] + "' password='" + sys.argv[4] + "'" 
    con = psycopg2.connect(conn_string) 
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT id, info FROM " + table + " WHERE app_id in (SELECT id FROM app WHERE short_name like '%_" + task_type + "')")
    
    rows = cursor.fetchall()
    print(len(rows))

    for row in rows:
        newInfo = replaceInfo(row)
    
        print "newInfo[1]"
        print newInfo[1]

        print "row"	
        print row

        cursor.execute("UPDATE " + table + " SET info=%s WHERE id=%s", (newInfo[1], row['id']) )
        con.commit()    

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    if con:
        con.close()
