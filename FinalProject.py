#Team Name: Koala Data
#Names: Taewoong Seo, Natalie Sangkagalo
#Project Title:

import requests
import json
import sqlite3

#Requesting data from Yelp API 
api_key = "lsaOrp_HuaqwvKRcdzWZKs0Yuq2A5asFK2wn0s8fcdOba7ss78GnvapTlX8aimzpUD9mpCuB_PazBvrdck4mKHeZvuezlJkMFsWmER2FOqrhrsT6w2p0u9BmbGOJXnYx"
business_id = 'CW46zBqGxTKPQPaKeWtImg'
endpoint = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % api_key}

print('Examples of college towns: Ann Arbor, East Lansing, Berkeley, Madison, Boulder, State College, Ithaca, Eugene, ...')
city_name = input('Please type in a college town name: ')

parameters = {'term': 'restaurants', 'limit': 20, 'radius': 9000, 'location': city_name}

#Request 20 restaurants in that city
yelp_r = requests.get(url = endpoint, params = parameters, headers = headers)

yelp_data = yelp_r.json()

biz_names = []
biz_ratings = []
biz_review_counts = []

#Add name, rating, and review_count to each list
for biz in yelp_data['businesses']:
    biz_names.append(biz['name'])
    biz_ratings.append(biz['rating'])
    biz_review_counts.append(biz['review_count'])

#Set up a database
conn = sqlite3.connect('restaurant_data.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Yelp (name TEXT, city_name TEXT, rating FLOAT, review_count INTEGER)')



for i in range(len(biz_names)):
    cur.execute('INSERT OR IGNORE INTO Yelp (name, city_name, rating, review_count) VALUES (?, ?, ?, ?)', (biz_names[i], city_name, biz_ratings[i], biz_review_counts[i]))


conn.commit()


#Use the dictionary and add to the table using SQL

#Requesting data from Google Maps API

#Read the city name and find the same 20 restaurants on Google Maps, add to the table

#Join the table using the shared key of names

#User does this five times, making sure there are no duplicated cities - add more items to the table

#Select the rate/price info from the table

#Create a csv file 

#For each city, calculate average rating per price level

#Graph the correlation for each city

