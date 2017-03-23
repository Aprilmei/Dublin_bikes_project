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

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


#This Python program creates DB and only run at the first.
#Everytime it will delete the old DB and create a new one 
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv





def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
        
        
def init_db():
    buffer = open("C:/Users/Daniele/workspaceComp30670/Dublin_bikes_project2/flaskr/flaskr/Dublin.json").read()
    station_data=json.loads(buffer)
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        for i,line in enumerate(station_data):
            db.execute("INSERT INTO station_info VALUES (?,?,?,?,?,?) ",(i,line["number"],line["name"],line["address"],line["latitude"],line["longitude"]))
        db_update()
    db.commit()
    



@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
    
    
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT * FROM station_info')
    station_info = cur.fetchall()
    cur2 = db.execute('SELECT * FROM dynamic_info')
    dynamic_info = cur2.fetchall()
    return render_template('show_entries.html', station_info=station_info,dynamic_info=dynamic_info)


def data_url():
    api_key="8589319d92f1dd6754044ae453f8732f5009d77f"
    link="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={0}".format(api_key)
    req=urllib.request.urlopen(link)
    req_response = req.read().decode('utf-8')
    content=json.loads(req_response)
    return content

def db_update():
    db = get_db()
    db.commit()
    read=data_url()
    for i,line in enumerate(read):
        db.execute("INSERT INTO dynamic_info VALUES (?,?,?,?,?,?,?) ",(i,line["number"],line["status"],line["bike_stands"],
                                                                   line["available_bike_stands"],line["available_bikes"],line["last_update"]))
    db.commit()

@app.cli.command('db_update')
def db_update_command():
    """Updates the database."""
    db_update()
    print('Database updated.')









@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))