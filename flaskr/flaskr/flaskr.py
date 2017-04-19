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

from db_related.db_info import *


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
    sql = "select * from station_info;"
    rows = engine.execute(sql).fetchall()
    print('#found {} stations', len(rows))
    return jsonify(stations=[dict(row.items()) for row in rows]) #

@app.route("/<int:station_id>")
def get_station(station_id):
    engine = get_db()
    data = []
    rows = engine.execute("SELECT available_bikes from dynamic_info where number = {};".format(station_id))
    for row in rows:
        data.append(dict(row))

    return jsonify(available=data)


@app.route('/<int:station_id>')
def station(station_id):
    # show the station with the given id, the id is an integer

    # this line would just return a simple string echoing the station_id
    # return 'Retrieving info for Station: {}'.format(station_id)

    # select the station info from the db
    sql = """
    select * from station_info where number = {}
    """.format(station_id)
    engine = get_db() 
    rows = engine.execute(sql).fetchall()  # we use fetchall(), but probably there is only one station
    res = [dict(row.items()) for row in rows]  # use this formula to turn the rows into a list of dicts
    return jsonify(data=res)  # jsonify turns the objects into the correct respose



@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):
    engine = get_db()
    df = pd.read_sql_query("select * from dynamic_info where number = %(number)s", engine, params={"number": station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
    df.set_index('last_update_date', inplace=True)
    res = df['available_bike_stands'].resample('1h').mean()
    #res['dt'] = df.index
    print("this is res",res)
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
    app.run(debug=True)
