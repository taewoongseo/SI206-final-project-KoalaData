#Team Name: Koala Data
#Names: Taewoong Seo, Natalie Sangkagalo
#Project Title: Google vs Yelp
#File Description: This file loads data from Google and Yelp APIs to the db browser file

import requests
import json
import sqlite3

#Asking for user input
print('Examples of cities to compare: Ann Arbor, Seattle, Vancouver, New York City, Hong Kong, Los Angeles, Tokyo, ...')
user_input_city = input('Please type in a city name that you have not entered before: ')


def gather_data(city_name):

    #Requesting data from Yelp API 
    api_key = "lsaOrp_HuaqwvKRcdzWZKs0Yuq2A5asFK2wn0s8fcdOba7ss78GnvapTlX8aimzpUD9mpCuB_PazBvrdck4mKHeZvuezlJkMFsWmER2FOqrhrsT6w2p0u9BmbGOJXnYx"
    business_id = 'CW46zBqGxTKPQPaKeWtImg'
    endpoint = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'bearer %s' % api_key}


    parameters = {'term': 'restaurants', 'limit': 20, 'radius': 9000, 'location': city_name}



    #Request 20 restaurants in that city
    yelp_r = requests.get(url = endpoint, params = parameters, headers = headers)

    yelp_data = yelp_r.json()

    biz_names = []
    biz_ratings = []
    biz_review_counts = []
    biz_coordinates = [] 

    #Add name, rating, and review_count to each list
    try:
        for biz in yelp_data['businesses']:
            biz_names.append(biz['name'])
            biz_ratings.append(biz['rating'])
            biz_review_counts.append(biz['review_count'])
            latitude = biz['coordinates']['latitude']
            longitude = biz['coordinates']['longitude']
            coord_tup = str(latitude) + ',' + str(longitude)
            biz_coordinates.append(coord_tup)
    except:
        print("Sorry, your city is not featured on Yelp :( Try another city!")



    #Requesting data from Google API 

    google_dict = []
    endpoint2 = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
    for i in range(len(biz_names)):
        restaurant_name_for_google = biz_names[i]
        coord_tup_google = biz_coordinates[i]
        parameters2 = {'key': "AIzaSyAZb7lF87OYuosZWGdDMvNnVaGxazfadXk", "input": restaurant_name_for_google, "inputtype": "textquery", 'locationbias': 'circle:2@' + coord_tup_google, 'fields': "name,user_ratings_total,geometry"}
        try:
            google_r = requests.get(url = endpoint2, params = parameters2)
            google_data = google_r.json()
            google_dict.append(google_data)
        except:
            google_data_null = {'null': 0}
            google_dict.append(google_data_null)

    google_names = []
    google_review_counts = []

    #Add google_review_counts to a list as long as there are 20 restaurants pulled initially
    if len(google_dict) == 20:
        for google_biz in google_dict:
            try:
                google_names.append(google_biz['candidates'][0]['name'])
                if 'user_ratings_total' in google_biz['candidates'][0].keys():
                    google_review_counts.append(google_biz['candidates'][0]['user_ratings_total'])
                else:
                    google_review_counts.append(0)
            except:
                print("Sorry, some restaurants in the city are not matching Google's results :( Try another city!")
                exit()
    else:
        exit()

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
    cur.execute('CREATE TABLE IF NOT EXISTS Yelp (restaurant_id INTEGER, name TEXT, city TEXT, yelp_review_count INTEGER)')

    for i in range(len(biz_names)):
        cur.execute('INSERT OR IGNORE INTO Yelp (restaurant_id, name, city, yelp_review_count) VALUES (?, ?, ?, ?)', (yelp_restaurant_id, biz_names[i], city_name, biz_review_counts[i]))
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
    cur.execute('CREATE TABLE IF NOT EXISTS Google (restaurant_id INTEGER, google_review_count INTEGER)')

    if len(google_names) == 20:
        for i in range(len(google_names)):
            cur.execute('INSERT OR IGNORE INTO Google (restaurant_id, google_review_count) VALUES (?, ?)', (google_restaurant_id, google_review_counts[i]))
            google_restaurant_id += 1
        conn.commit()
    else:
        print("Sorry, some restaurants in the city are not matching Google's results :( Try another city!")
        exit()

    print("Your data has been retrieved!")

gather_data(user_input_city)