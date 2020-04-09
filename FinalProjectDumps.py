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

#Now for looping the joined table!
rows = cur.fetchall()
for row in rows:
    print(row)

