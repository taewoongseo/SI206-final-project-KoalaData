#Team Name: Koala Data
#Names: Taewoong Seo, Natalie Sangkagalo
#Project Title: Google vs Yelp
#File Description: This file loads data from Google and Yelp APIs to the db browser file

import requests
import json
import sqlite3

#Requesting data from Yelp API 
api_key = "lsaOrp_HuaqwvKRcdzWZKs0Yuq2A5asFK2wn0s8fcdOba7ss78GnvapTlX8aimzpUD9mpCuB_PazBvrdck4mKHeZvuezlJkMFsWmER2FOqrhrsT6w2p0u9BmbGOJXnYx"
business_id = 'CW46zBqGxTKPQPaKeWtImg'
endpoint = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % api_key}

print('Examples of cities to compare: Ann Arbor, Seattle, Vancouver, New York City, Hong Kong, Los Angeles, Tokyo, ...')
city_name = input('Please type in a city name that you have not entered before: ')

parameters = {'term': 'restaurants', 'limit': 20, 'radius': 9000, 'location': city_name}



#Request 20 restaurants in that city
yelp_r = requests.get(url = endpoint, params = parameters, headers = headers)

yelp_data = yelp_r.json()

biz_names = []
biz_ratings = []
biz_review_counts = []
biz_coordinates = [] 

#Add name, rating, and review_count to each list
for biz in yelp_data['businesses']:
    biz_names.append(biz['name'])
    biz_ratings.append(biz['rating'])
    biz_review_counts.append(biz['review_count'])
    latitude = biz['coordinates']['latitude']
    longitude = biz['coordinates']['longitude']
    coord_tup = str(latitude) + ',' + str(longitude)
    biz_coordinates.append(coord_tup)



#Requesting data from Google API 

google_dict = []
endpoint2 = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
for i in range(len(biz_names)):
    restaurant_name_for_google = biz_names[i]
    coord_tup_google = biz_coordinates[i]
    parameters2 = {'key': "AIzaSyAZb7lF87OYuosZWGdDMvNnVaGxazfadXk", "input": restaurant_name_for_google, "inputtype": "textquery", 'locationbias': 'circle:1@' + coord_tup_google, 'fields': "name,user_ratings_total,geometry,formatted_address"}
    google_r = requests.get(url = endpoint2, params = parameters2)
    google_data = google_r.json()
    google_dict.append(google_data)

google_names = []
google_review_counts = []
google_coordinates = []

for google_biz in google_dict:
    google_names.append(google_biz['candidates'][0]['name'])
    if 'user_ratings_total' in google_biz['candidates'][0].keys():
        google_review_counts.append(google_biz['candidates'][0]['user_ratings_total'])
    else:
        google_review_counts.append(0)
    g_latitude = google_biz['candidates'][0]['geometry']['location']['lat']
    g_longitude = google_biz['candidates'][0]['geometry']['location']['lng']
    g_coord_tup = str(g_latitude) + ',' + str(g_longitude)
    google_coordinates.append(g_coord_tup)

#restaurant_id set up 
conn = sqlite3.connect('restaurant_data.db')
cur = conn.cursor()
cur.execute(' SELECT count(name) FROM sqlite_master WHERE type= ? AND name= ? ', ('table', 'Yelp', ))
if cur.fetchone()[0] == 1:
    cur.execute('SELECT restaurant_id FROM Yelp WHERE restaurant_id = (SELECT max(restaurant_id) FROM Yelp)')
    yelp_restaurant_id = cur.fetchone()[0] + 1 
else:
    yelp_restaurant_id = 1


#Set up a database for Yelp
cur.execute('CREATE TABLE IF NOT EXISTS Yelp (restaurant_id INTEGER, name TEXT, city TEXT, rating REAL, yelp_review_count INTEGER, coordinates TEXT)')

for i in range(len(biz_names)):
    cur.execute('INSERT OR IGNORE INTO Yelp (restaurant_id, name, city, rating, yelp_review_count, coordinates) VALUES (?, ?, ?, ?, ?, ?)', (yelp_restaurant_id, biz_names[i], city_name, biz_ratings[i], biz_review_counts[i], biz_coordinates[i]))
    yelp_restaurant_id += 1
conn.commit()

cur.execute(' SELECT count(name) FROM sqlite_master WHERE type= ? AND name= ? ', ('table', 'Google', ))
if cur.fetchone()[0] == 1:
    cur.execute('SELECT restaurant_id FROM Yelp WHERE restaurant_id = (SELECT max(restaurant_id) FROM Google)')
    google_restaurant_id = cur.fetchone()[0] + 1 
else:
    google_restaurant_id = 1
    
#Set up a database for Google
conn = sqlite3.connect('restaurant_data.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Google (restaurant_id INTEGER, name TEXT, google_review_count INTEGER, coordinates TEXT)')


for i in range(len(google_names)):
    cur.execute('INSERT OR IGNORE INTO Google (restaurant_id, name, google_review_count, coordinates) VALUES (?, ?, ?, ?)', (google_restaurant_id, google_names[i], google_review_counts[i], google_coordinates[i]))
    google_restaurant_id += 1
conn.commit()