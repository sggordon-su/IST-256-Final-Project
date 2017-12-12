
# coding: utf-8

# # Meetup
# ### Jessica Zuk and Samantha Gordon
# ### Monday, December 11, 2017
# ##### Welcome to Meetup, an application to find the perfect place to meet.
# Start by entering two locations below. As a helpful hint, try to be as detailed as possible. Keep in mind there are oftentimes multiple cities with the same name around the world, so make sure to specify as much as you can to get the best results.

# In[33]:


# import necessary APIs and modules
from geopy.geocoders import Nominatim
from googleplaces import GooglePlaces, types, lang
import requests
import json
import urllib.request, json
import matplotlib
import matplotlib.pyplot as plt
import plotly 
import plotly.plotly as py     
import plotly.graph_objs as go  
import cufflinks as cf
import pandas as pd
import folium
import warnings

#from Google Places API
API_KEY='AIzaSyAFlBQ3-1o2YLGG32dKSpHpyWlkUyWYMIU'
google_places = GooglePlaces(API_KEY)



# In[36]:


try:
    #input two addresses
    location_1 = str(input("Enter Your First Address: "))
    location_2 = str(input("Enter Your Second Address: "))
    # set Nominatim as a variable for easier use
    locator = Nominatim()
    # using geocode (from nominatim) to turn user input into an actual location
    l1 = locator.geocode(location_1)
    l2 = locator.geocode(location_2) 
    # use the lat/long attributes to find the lat/long of the locations above
    lat1=(l1.latitude)
    long1=(l1.longitude)
    long2=(l2.longitude)
    lat2=(l2.latitude)
    # find the average of the latitudes and longitudes to find the midpoint coordinates
    midlat = ((lat1 + lat2) / 2)
    midlong = ((long1 + long2) / 2)
    midpoint = (midlat,midlong)
    # reverse the midpoint to find the address of the coordinates
    midpoint2 = locator.reverse(midpoint)
    print(midpoint,midpoint2)
# account for any errors    
except AttributeError:
    print("One or both of your addresses are not valid. Ensure spelling is correct and you are being as specific as possible. Try again.")
except TypeError:
    print("One or both of your addresses are not valid or not specific enough. Ensure spelling is correct and you are being as specific as possible. Try again.")
except json.decoder.JSONDecodeError as e: 
    print("ERROR: Cannot decode the response into json")
    print("DETAILS", e)
except requests.exceptions.HTTPError as e:
    print("ERROR: Response from ", url, 'was not ok.')
    print("DETAILS:", e)      
except requests.exceptions.RequestException as e: 
    print("ERROR: Cannot connect to ", url)
    print("DETAILS:", e)
except gaierror as e:
    print("ERROR: Cannot connect to ", url)
    print("DETAILS:" , e)
    

# import Google Places API with registered key and necessary parameters
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
params = dict(location = "%s,%s"%(midpoint), rankby='distance', type ='restaurant', key = API_KEY)
response = requests.get(url=url, params=params)
data = json.loads(response.text)

# if the data has no results from the parameters given above, expand the radius parameter and set the dataframe
if data['results']==[]:
    params = dict(location = "%s,%s"%(midpoint), radius=50000, type ='restaurant', key = API_KEY)
    response = requests.get(url=url, params=params)
    data = json.loads(response.text)
    df = pd.DataFrame(data['results'])
# if the original data does have results, set the dataframe with that data
else:
    df = pd.DataFrame(data['results'])
# if the expanded radius still provides no data, print error message
if data['results']==[]:
    print("There are no restaurants within 50,000 meters of this location. Please try again with new locations.")


# In[37]:


# set map to view the midpoint location, the type of map, and the zoom parameters
map = folium.Map(location=midpoint , tiles='Open Street Map' , zoom_start=11)
n=0
# count the number of results in dataframe to ensure all are accounted for on the map
count = len(df)

# a while loop goes through plotting points on the map as many times as it needs to
while n<count:
    lat = (df['geometry'][n]['location']['lat'])
    long = (df['geometry'][n]['location']['lng'])
    pos = (lat,long)
    name= str(data['results'][n]['name'])
    vicinity= str(data['results'][n]['vicinity'])
    # set popup message so that name and address (vicinity) appear on Markers
    popup =folium.Popup((name + " is located at " + vicinity),parse_html=True)
    # customize marker settings to add info icon and color
    marker = folium.Marker(location=pos, popup=popup, icon=folium.Icon(icon='info-sign',color='purple')) 
    #add markers to map
    map.add_child(marker)
    n = int(n+1)


save = input("Would you like to save this map as an .html file to your local host? Type yes to save or any key to continue without saving: ")
if save.lower() == "yes":
    map.save("restaurants.html")
    print("Success! Your map was saved.")
else:
    print("Your map is displayed below. No file saved to your computer.")

map


# In[38]:


df


# In[ ]:




