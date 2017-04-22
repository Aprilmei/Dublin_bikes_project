'''
Created on 31 Mar 2017

@author: April
'''
import datetime
import functools
import json
import os
import sqlite3
import urllib.request
from flask import Flask, g, jsonify
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, \
     render_template, flash
from sqlalchemy import *
from db_related.db_info import *
import numpy as np
import pandas as pd


app = Flask(__name__)

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
    #join station and dynamic data table on latest updated time (for dynamic data)
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
    
    #display only entries 3 days ago to today
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=3)
    df = df[start:end]
    # take mean of entries within each hour
    res = df['available_bike_stands'].resample('1h').mean()
    res2 = df['available_bikes'].resample('1h').mean()
    #some entries become NaN after resample and mean, res.fillna is useful to convert them to 0 and jsonify everything without problems
    res.fillna(0,inplace=True)
    res2.fillna(0,inplace=True)
    return jsonify(data=json.dumps(list(zip(map(lambda x:x.isoformat(), res.index), res.values, res2.values))))



if __name__ == "__main__":
    app.run(debug=True)
