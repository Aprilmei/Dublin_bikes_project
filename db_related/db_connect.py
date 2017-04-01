#This Python program creates DB and only run at the first.
#Everytime it will delete the old DB and create a new one 
import json
import sqlite3
import os 

if os.path.isfile("bike.db"):
    os.remove("bike.db")
    
#create DB 
conn=sqlite3.connect("bike.db")

#Create table for stations 
conn.execute("CREATE TABLE station_info (number int, name text, address text, latitude int, longitude int)")
#Create table for dynamic data 
conn.execute("CREATE TABLE dynamic_info (number int, status text, bike_stands int, available_bike_stands int, available_bikes int, last_update timestamp)")

# Insert station data  into DB

buffer = open("Dublin.json").read()
station_data=json.loads(buffer)
print(station_data)

for line in station_data:
    conn.execute("INSERT INTO station_info VALUES (?,?,?,?,?) ",(line["number"],line["name"],line["address"],line["latitude"],line["longitude"]))

count=0
for row in conn.execute("SELECT * FROM station_info order by number"):
    count+=1
    print(row)
print("the row number of the table is ",count)    
c=conn.cursor()
'''
n=c.execute("SELECT * FROM station_info").rowcount
print("the row number of the table is ",n)
'''
c.execute("select * from station_info")
results = c.fetchall()
print("the length is ",len(results))

   
conn.commit()

conn.close()



'''

    '''

