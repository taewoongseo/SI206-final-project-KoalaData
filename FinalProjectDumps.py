#Team Name: Koala Data
#Our Names: Natalie Sangkagalo, Taewoong Seo
#File Description: This file dumps data to the db Browser by joining two tables, processes data, and creates visualized charts

import sqlite3
import json

conn = sqlite3.connect('restaurant_data.db')
cur = conn.cursor()

#Joining two tables together
cur.execute('SELECT Google.name, Yelp.yelp_review_count, Google.google_review_count, Yelp.city FROM Yelp INNER JOIN Google ON Yelp.restaurant_id = Google.restaurant_id')
conn.commit()

#Calculation time
tot_yelp = 0
tot_google = 0
#Now for looping the joined table!
rows = cur.fetchall()
for row in rows:
    tot_yelp += row[1]
    tot_google += row[2]
print(tot_yelp)
print(tot_google)

#how much is Google bigger than Yelp?
difference = (tot_google/tot_yelp)*100
print(str(difference) + '%')



#Now... by cities!
yelp_d = {}
google_d = {}

for row in rows:
    city = row[-1]
    if city not in yelp_d.keys():
        yelp_d[city] = row[1]
    else:
        yelp_d[city] += row[1]

for row in rows:
    city = row[-1]
    if city not in google_d.keys():
        google_d[city] = row[2]
    else:
        google_d[city] += row[2]

print(yelp_d)
print(google_d)
        



