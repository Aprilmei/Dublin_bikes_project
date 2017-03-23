#Get the dynamic data from JCDecaux

#https://developer.jcdecaux.com/#/opendata/vls?page=getstarted
#changed the code on the website, then it works
#here is the guide I followed
#https://maxhalford.github.io/blog/bike-stations/

import requests
import json
import urllib.request

import sqlite3

#using requests
def dynamic_data():
    api_key="8589319d92f1dd6754044ae453f8732f5009d77f"
    link="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={0}".format(api_key)
    req = requests.get(link)
    content=json.loads(req.text)
    return content

#using urllib.request
def data_url():
    api_key="8589319d92f1dd6754044ae453f8732f5009d77f"
    link="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={0}".format(api_key)
    req=urllib.request.urlopen(link)
    req_response = req.read().decode('utf-8')
    content=json.loads(req_response)
    return content

data=dynamic_data()
read=data_url()

#print("Use request package",data)

#print("the dynamic data is ",read)
def db_update():
    conn=sqlite3.connect("bike.db")
    read=data_url()
    for line in read:
        conn.execute("INSERT INTO dynamic_info VALUES (?,?,?,?,?,?) ",(line["number"],line["status"],line["bike_stands"],
                                                                   line["available_bike_stands"],line["available_bikes"],line["last_update"]))
    for row in conn.execute("SELECT * FROM dynamic_info"):
        print(row)
    
    #check how many times we updated db from Dublin BIKE 

    for row in conn.execute("SELECT * FROM dynamic_info WHERE number==42"):
        print(row)
    
    conn.commit()
    conn.close()

#need to write a method to update DB every 5 mins     
db_update()   
