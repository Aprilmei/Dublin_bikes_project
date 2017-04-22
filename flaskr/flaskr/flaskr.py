'''
Created on 31 Mar 2017

@author: April
'''
import functools
import json
import os
import sqlite3
import urllib.request
import pandas as pd

from flask import Flask, g, jsonify
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, \
     render_template, flash
from sqlalchemy import *

import numpy

#from db_related.db_info import *


app = Flask(__name__)
rds_host = 'dubbiker.ci278m5m2zts.us-west-2.rds.amazonaws.com'
name = "awsuserad"
password = "Rds4DubBike"
db_name = "dubbiker"
port = 3306
def connect_to_database():
    engine=create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(name,password,rds_host,port,db_name),echo=True)
    return engine

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
        return db



@app.route('/')
def root():
    return render_template('index.html')


@app.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
    engine = get_db()
    sql = """
    SELECT *
    FROM dynamic_info as d1
    JOIN station_info as s
    ON d1.number = s.number
    WHERE last_update = (SELECT MAX(last_update) FROM dynamic_info d2 WHERE d1.number = d2.number)
    GROUP BY d1.number;
    """
    rows = engine.execute(sql).fetchall()
    print('#found {} latest_occupancy_stations', len(rows))
    return jsonify(stations=[dict(row.items()) for row in rows])



@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):
    engine = get_db()
    df = pd.read_sql_query("select * from dynamic_info where number = %(number)s", engine, params={"number": station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
    df.set_index('last_update_date', inplace=True)
    res = df['available_bike_stands'].resample('1h').mean()
    return jsonify(data=json.dumps(list(zip(map(lambda x:x.isoformat(), res.index), res.values))))
     
     

if __name__ == "__main__":
    """
    The URLs you should visit after starting the app:
    http://1270.0.0.1/
    http://1270.0.0.1/hello
    http://1270.0.0.1/user
    http://1270.0.0.1/dbinfo
    http://1270.0.0.1/station/42
    """
    app.run(host='0.0.0.0',debug=True)
