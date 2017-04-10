'''
Created on 23 Mar 2017

@author: Daniele
'''
'''
Created on 21 Mar 2017

@author: Daniele
'''
# all the imports
import json
import os
import sqlite3
import urllib.request

from flask import Flask, g, jsonify
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, \
     render_template, flash
from sqlalchemy import *

from db_related.api_read import *

from db_related.db_info import *

import simplejson as json


#This Python program creates DB and only run at the first.
#Everytime it will delete the old DB and create a new one 
app = Flask(__name__) 
# create the application instance :)

# Load default config and override config from an environment variable


def connect_to_database():
    engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(name,password,rds_host,port,db_name ),echo=True)

    return engine

def get_db():                                                                                                                                                                                                                                                       
    engine = getattr(g, 'engine', None)                                                                                                                                                                                                                              
    if engine is None:                                                                                                                                                                                                                                                  
        engine = g.engine = connect_to_database()                                                                                                                                                                                                                    
    return engine 

@app.route("/available/<int:station_id>")
def get_stations(station_id):
    engine = get_db()
    data = []
    rows = engine.execute("SELECT available_bikes from dynamic_info where number = {};".format(station_id))
    for row in rows:
        data.append(dict(row))

    return json.dumps(available=data)



@app.route('/station/<int:station_id>')
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

'''
@app.route('/')
def show_entries():
    sql1 = """
    SELECT * FROM station_info
    """
    sql2 = """
    SELECT * FROM dynamic_info
    """
    engine = get_db()
    station_info = engine.execute(sql1).fetchall()
    dynamic_info = engine.execute(sql2).fetchall()
    return render_template('show_entries.html', station_info=station_info,dynamic_info=dynamic_info)
'''


@app.cli.command('db_update')
def db_update_command():
    """Updates the database."""
    db_update()
    print('Database updated.')
    
    
    
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

