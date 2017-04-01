'''
Created on 31 Mar 2017

@author: April
'''

#!/usr/bin/python
import sys
import logging
import json
import pymysql
from sqlalchemy import create_engine
from db_related.db_info import *

import sqlalchemy as sqla
import traceback
import os
from pprint import pprint

import requests
import time


logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name,
                           passwd=password, db=db_name, connect_timeout=10)
    print("success")
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()



#dialect+driver://username:password@host:port/database
# mysql-python
#engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')
connectDB=create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(name,password,rds_host,port,db_name ),echo=True)

def create_table():
    sql_1="""CREATE TABLE IF NOT EXISTS station_info (number int, name text, address text, latitude int, longitude int)
"""
    try:
        res = connectDB.execute("DROP TABLE IF EXISTS station_info")
        res = connectDB.execute(sql_1)
        print(res.fetchall())
    except Exception as e:
        print(e)
    
    sql_2="""
    CREATE TABLE IF NOT EXISTS dynamic_info (number int, status text, bike_stands int, available_bike_stands int, available_bikes int, last_update timestamp)
    """
    connectDB.execute(sql_2)

def station_rds(file):    
    buffer = open(file).read()
    station_data=json.loads(buffer)
    print(station_data)
    
    for line in station_data:
        print(line)
        connectDB.execute("INSERT INTO station_info VALUES (%s,%s,%s,%s,%s) ",(line.get("number"),line.get("name"),line.get("address"),line.get("latitude"),line.get("longitude")))

    return 

#create_table()
#station_rds("Dublin.json")   
for row in connectDB.execute("SELECT * FROM dynamic_info WHERE number=42"):
        print(row)
