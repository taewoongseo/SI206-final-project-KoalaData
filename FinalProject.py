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

#Have a user type in a city on Yelp
city_input = input('Please type the city name: ' )

parameters = {'term': 'restaurants', 'limit': 20, 'radius': 9000, 'location': city_input}

#Request 20 restaurants in that city
yelp_r = requests.get(url = endpoint, params = parameters, headers = headers)

yelp_data = yelp_r.json()

#Set up a database
conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Yelp (name TEXT, rating FLOAT, rating_count INTEGER)''')


#Idk if I need to do the following
yelp_lst = []
yelp_d = {}

#IDK if I have to do the follwoing - Now add name, rating, and review_count to a dictionary
for biz in yelp_data['businesses']:
    yelp_d['name'] = biz['name']
    yelp_d['rating'] = biz['rating']
    yelp_d['rating_count'] = biz['review_count']
    yelp_lst.append(yelp_d)

print(yelp_lst)


#Use the dictionary and add to the table using SQL

#Requesting data from Google Maps API

#Read the city name and find the same 20 restaurants on Google Maps, add to the table

#Join the table using the shared key of names

#User does this five times, making sure there are no duplicated cities - add more items to the table

#Select the rate/price info from the table

#Create a csv file 

#For each city, calculate average rating per price level

#Graph the correlation for each city

