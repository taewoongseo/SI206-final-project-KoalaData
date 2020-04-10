#Team Name: Koala Data
#Our Names: Natalie Sangkagalo, Taewoong Seo
#File Description: This file dumps data to the db Browser by joining two tables, processes data, and creates visualized charts

import sqlite3
import json
import os
import csv

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
    print(row)
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

percent_difference_d = {}
for city in yelp_d.keys():
    yelp_tot_city = yelp_d[city]
    if city in google_d.keys():
        google_tot_city = google_d[city]
    per_difference_city = (google_tot_city/yelp_tot_city)*100
    percent_difference_d[city] = per_difference_city

print(percent_difference_d)


#Add to CSV file
dir = os.path.dirname(__file__)
outFile = open(os.path.join(dir, 'yelp_google_raw_data.csv'), "w")
csv_writer = csv.writer(outFile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
csv_writer.writerow(["Name", "Yelp Review Count", "Google Review Count", "City"])
for i in rows:
    csv_writer.writerow([i[0], i[1], i[2], i[3]])

dir = os.path.dirname(__file__)
outFile = open(os.path.join(dir, 'yelp_google_calculations.csv'), "w")
csv_writer = csv.writer(outFile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
csv_writer.writerow(["City", "Total Yelp Review Count", "Total Google Review Count", "Google To Yelp Ratio in %"])
for i in yelp_d.keys():
    csv_writer.writerow([i, yelp_d[i], google_d[i], percent_difference_d[i]])
csv_writer.writerow(['Total', tot_yelp, tot_google, difference])

