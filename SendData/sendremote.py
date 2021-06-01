#!/usr/bin/env python3
# importing the requests library
import requests
import geocoder
  
# defining the api-endpoint 
parameter = "5"
API_ENDPOINT = "http://localhost:5000/menu/api/values/"+parameter+"/"
print(API_ENDPOINT)

g = geocoder.ip('me')
geolocat = str(g.latlng[0])+","+str(g.latlng[1])

# data to be sent to api
data = {
        "readings": "70.1",
        "dates": "19:46:35",
        "location": geolocat
        }
  
# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = data)