from flask import json
import requests

def getYelpData(businessList=[]):

    yelp_list = []

    for business in businessList:
        yelp_dict = {
            "name":     ifValid(business, "name"),
            "url":      ifValid(business, "url"),
            "location": getAddress(business["location"]["display_address"]),
            "phone":    ifValid(business, "phone"),
            "distance": mToKm(ifValid(business, "distance")),
            "price":    ifValid(business, "price"),
            "fav":      False
            }

        yelp_list.append(yelp_dict)

    return(yelp_list)

def mToKm(value):
    if value is None:
        return None

    """Format value as Km."""
    return f"{value/1000:,.2f} km"


def ifValid(businessDict, key):
    if key not in businessDict:
        return("")
    else:
        return(businessDict[key])


def getMeYelp(term, postalCode):
    # Connect to yelp api
    yelp_api_key = "<Your Yelp API Key>"

    yelpHeaders = {"Authorization": "Bearer %s" % yelp_api_key,}

    yelp_url = "https://api.yelp.com/v3/businesses/search"

    params = {
        "term": term,
        "location": postalCode,
        "radius": 10000,
        "limit": 15
    }

    yelp_res = requests.get(yelp_url, params=params, headers=yelpHeaders)
    yelp_data = yelp_res.json()

    return(getYelpData(yelp_data["businesses"]))


# Get City and Postal code based on the
# latitude and longitude passed in as parameters
def getLocation(lat, long):
    url = "https://revgeocode.search.hereapi.com/v1/revgeocode"
    api_key = "<Your geocode API key>"
    PARAMS = {
        'at': '{},{}'.format(lat, long),
        'apikey': api_key
    }

    # Sending get request and saving the response as response object
    res = requests.get(url=url, params=PARAMS)

    data = res.json()
    city = data["items"][0]["address"]["city"]
    state = data["items"][0]["address"]["state"]
    postalCode = data["items"][0]["address"]["postalCode"]

    return(city, postalCode)

def getAddress(addressList):
    address = ""
    for item in addressList:
        address =  address + item + " "

    return(address.strip())