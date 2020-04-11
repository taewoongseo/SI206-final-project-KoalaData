#Team Name: Koala Data
#Our Names: Natalie Sangkagalo, Taewoong Seo
#File Description: This file dumps data to the db Browser by joining two tables, processes data, and creates visualized charts

import sqlite3
import json
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

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

#Visualization for total counts

N = len(yelp_d.keys())
width = 0.35
ind = np.arange(N)

fig = plt.figure()
ax = fig.add_subplot(111)

yelp_vals = []
google_vals = []
city_vals = []
for city in yelp_d.keys():
    yelp_val = yelp_d[city]
    yelp_vals.append(yelp_val)
    google_val = google_d[city]
    google_vals.append(google_val)
    city_vals.append(city)

label_tups = tuple(city_vals)

p1 = ax.bar(ind, yelp_vals, width, color = 'red')
p2 = ax.bar(ind + width, google_vals, width, color = 'blue')

ax.set_xticks(ind + width / 2)
ax.set_xticklabels(label_tups)
ax.legend((p1[0], p2[0]), ('Yelp', 'Google'))
ax.autoscale_view()

ax.set(xlabel = 'Cities', ylabel = 'Total Review Counts', title = 'Total Review Counts on Yelp vs Google of Restaurants in Different Cities')

#Visualization for % difference
N2 = len(yelp_d.keys())
width2 = 0.4
ind2 = np.arange(N)

percent_vals = []
for city in percent_difference_d.keys():
    percent_vals.append(percent_difference_d[city])
avg = difference
line = 100


fig = plt.figure()
ax2 = fig.add_subplot(111)


p = ax2.bar(ind2, percent_vals, width2, color = 'cyan')


ax2.set_xticks(ind2)
ax2.set_xticklabels(label_tups)
ax2.autoscale_view()

avg_line = ax2.axhline(y = avg, color = 'k', linestyle = "--")
std_line = ax2.axhline(y = line, color = 'b', linestyle = ':')

ax2.legend((avg_line, std_line), ('Average ratio', '100 percent ratio'))


ax2.set(xlabel = 'Cities', ylabel = 'Google to Yelp review count ratio in %', title = 'Google To Yelp Review Count Ratio (%) in Different Cities')

plt.show()