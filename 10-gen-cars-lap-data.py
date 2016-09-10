#!/usr/bin/env python

####################################################
# 10-gen-cars-lap-data.py

# This script looks at the generated data and generates output jsons

import MySQLdb 
import json
import sys
import time
import math

configfilename = "config.json"

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

# open configfilename and read
configfile = open(configfilename, 'r')
configfilejson = configfile.read()
configfile.close()

# parse configfilejson
json_data = json.loads(configfilejson)

SQL_Host = json_data['SQL_Host']
SQL_User = json_data['SQL_User']
SQL_Passwd = json_data['SQL_Passwd']
SQL_DB = json_data['SQL_DB']

# connect to database 
try:
   db = MySQLdb.connect(host=SQL_Host,     # your host, usually localhost
                     user=SQL_User,     # your username
                     passwd=SQL_Passwd, # your password
                     db=SQL_DB)         # name of the data base
   cursor = db.cursor() 
   # cursor = db.cursor(mdb.cursors.DictCursor) to refer to results of fetch by name rater than index
except:
   print "TEST=> ERROR Connecting to database"
   sys.exit()

#######################################################################################
def SendToSQL(SQLcmd):
   status = 0
   try:
      cursor.execute(SQLcmd)
      db.commit()
   except:
      print "ERROR executing SQL command : ", SQLcmd
      # Rollback in case there is any error
      db.rollback()
      status = -1
   return status

#######################################################################################

cars = ("NPS","NHS")

json_blob = ""

while True:

  first = True
  json_blob = ""

  ofile = open("car-pos.json", 'w')

  for car in cars:
    sql = """SELECT GPSdatetimeACST,
                    Car_Name
             FROM GPS_Log
             WHERE Finish_line=1 AND Car_Name=""" + '"' + car + '"' + """ 
             ORDER BY GPSdatetimeACST DESC
             LIMIT 1;"""
    cursor.execute(sql)
    if cursor.rowcount: # GPS_Log entries exist for car
      row = cursor.fetchone()
      gps_dt = row[0]
      
    else:
      gps_dt = ""

    if first==True:
      jsonline = ""   # just return for this line
      first=False
    else:
      jsonline = ",\n"  # finish last line and return for this line

    jsonline =  jsonline + '         {"Car_Name":"' + car + '","GPSdatetimeACST":"' + str(gps_dt) + '","lat":"' + str(lat) + '","lon":"' + str(lon) + '"}'
    json_blob += jsonline

  json_blob = '{"pp_cars":[\n' + json_blob + "]\n}"
  ofile.write(json_blob)
  ofile.close()

  # FUDGE: Needed to force cache flush (how do we do it properly??)
  sql = ""
  SendToSQL(sql)
  
  time.sleep(5)

