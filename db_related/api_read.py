#Get the dynamic data from JCDecaux

#https://developer.jcdecaux.com/#/opendata/vls?page=getstarted
#changed the code on the website, then it works
#here is the guide I followed
#https://maxhalford.github.io/blog/bike-stations/

import json
import time
import urllib.request

import requests
from sqlalchemy import create_engine

rds_host = 'dubbiker.ci278m5m2zts.us-west-2.rds.amazonaws.com'
name = "awsuserad"
password = "Rds4DubBike"
db_name = "dubbiker"
port = 3306


connectDB=create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(name,password,rds_host,port,db_name ),echo=True)

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
    read=data_url()
    for line in read:
        connectDB.execute("INSERT INTO dynamic_info VALUES (%s,%s,%s,%s,%s,%s) ",(line.get("number"),line.get("status"),line.get("bike_stands"),
                                                                   line.get("available_bike_stands"),line.get("available_bikes"),line.get("last_update")))
    for row in connectDB.execute("SELECT * FROM dynamic_info"):
        print(row)
    
    #check how many times we updated db from Dublin BIKE 

    for row in connectDB.execute("SELECT * FROM dynamic_info WHERE number=42"):
        print(row)

def station(station_id):    
    data = []
    rows = connectDB.execute("SELECT available_bikes from dynamic_info where number = {};".format(station_id))
    for row in rows:
        data.append(dict(row))
    print(data)

#need to write a method to update DB every 5 mins     
#db_update()  

def main():
    while True:
        db_update()
        time.sleep(5*60)
            
 
if __name__ == "__main__":
    main()