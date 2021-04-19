import requests
import json
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENTID")
client_secret = os.getenv("CLIENTSECRET")

fs_url = 'https://api.foursquare.com/v2/venues/explore'


def query_api(location, search, radius):
    params = dict(
        client_id=client_id,
        client_secret=client_secret,
        v='20180323',
        ll=location,
        query=search,
        radius=radius,
        sortByDistance=True,
        limit=100
    )
    resp = requests.get(url=fs_url, params=params).json()
    return resp


def query_airports_api(location, search):
    params = dict(
        client_id=client_id,
        client_secret=client_secret,
        v='20180323',
        ll=location,
        query=search,
        category_id="4bf58dd8d48988d1ed931735",
        sortByDistance=True,
        limit=100
    )
    resp = requests.get(url=fs_url, params=params).json()
    return resp


def make_dataframe(mylist):
    data = mylist.get("response").get("groups")[0].get("items")
    return get_place_info(data)


def get_place_info(data):
    places_info = list()
    for element in data:
        new_dictionary = {}
        new_dictionary["name"] = element.get("venue").get("name")
        new_dictionary["latitude"] = element.get(
            "venue").get("location").get("lat")
        new_dictionary["longitude"] = element.get(
            "venue").get("location").get("lng")
        new_dictionary["distance"] = element.get(
            "venue").get("location").get("distance")
        places_info.append(new_dictionary)

    return pd.DataFrame(places_info)
