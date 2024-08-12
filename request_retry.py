from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()
scraper_api = os.getenv("SCRAPERAPI")
RAPID_API = os.getenv("RAPIDAPI")
LOCATION_IQ_API = os.getenv("LOCATIONIQ")
SCRAPEOPS_API = os.getenv("SCRAPEOPS")


def req_retry(url, params, headers={}):
    delay = 1
    backoff = 2
    retry_count = 3
    attempts = 0
    while attempts < retry_count:
        try:
        

            response = requests.get(url, params, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as ex:
            attempts += 1
            if attempts == retry_count:
                print('retry count exceeded for url: '+ url)
                raise ex
            
            time.sleep(delay)
            delay *= backoff


def search_property(loc):
    url = "https://airbnb45.p.rapidapi.com/api/v1/searchLocation"
    querystring = {"query":loc}
    headers = {
		"x-rapidapi-key": RAPID_API,
		"x-rapidapi-host": "airbnb45.p.rapidapi.com"
	}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['data']


def property_request(loc, cur=''):
    url = "https://airbnb45.p.rapidapi.com/api/v1/searchPropertyByLocation"
    headers = {
		"x-rapidapi-key": RAPID_API,
		"x-rapidapi-host": "airbnb45.p.rapidapi.com"
	}
    querystring = {"location":loc,"nextPageCursor":cur,"typeOfPlace":"entire_home"}
    response = req_retry(url, params=querystring, headers=headers)
    data = response.json()['data']
    return data


def owner_request(url):
    payload ={ 'api_key': scraper_api, 'url': url }
    uri = 'https://api.scraperapi.com/'
    return req_retry(uri, payload)


def owner_request_2(url):
    uri=url
    params={
        'api_key': SCRAPEOPS_API,
        'url': uri, 
    }
    return req_retry('https://proxy.scrapeops.io/v1/', params)


def location_iq_req(lat, long):
    url = "https://us1.locationiq.com/v1/reverse"
    params = {
        "key":LOCATION_IQ_API,
        "lat":lat,
        "lon":long,
        "format":"json"
    }
    response = req_retry(url, params)
    return response.json()


    


    
