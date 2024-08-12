import os
from dotenv import load_dotenv
import pandas as pd
from request_retry import property_request, search_property
load_dotenv()

RAPID_API = os.getenv("RAPIDAPI")
# print(RAPID_API)

def choice_loc(num):
	
	while True:
		
		try:
			ch = int(input("Enter Your choice: "))
		except:
			print("Wrong Input ⚠️")
		else:
			if ch < num:
				return ch
			else:
				print("Wrong Input ⚠️")



def search_location(location):
	response = search_property(location)
	print('Choose the preferred search location: ')
	print("\n")
	for i in range(len(response)):
		print(f"press {i} to search for: {response[i]['display_name']}")
	
	choice = choice_loc(len(response))
	return response[choice]['display_name']
	
	

def search_by_location(location):
	
	properties = pd.DataFrame(columns=['id', 'title', 'name', 'localized_city', 'city', 'rating', 'num_ratings', 'url', 'latitude', 'longitude'])
	data = property_request(loc=location)
	# data = response.json()['data']
	ind = 0
	run = True
	while run:

		for lst in data['list']:
			listing = lst['listing']
			# print(listing)
			properties.loc[ind,'id'] = listing["id"]
			properties.loc[ind,'title'] = listing['title']
			properties.loc[ind,'name'] = listing['name']
			try:
				properties.loc[ind,'rating'] = float(listing['avgRatingLocalized'].split(" (")[0])
				properties.loc[ind,'num_ratings'] = (listing['avgRatingLocalized'].split(" (")[1].split(')')[0])
			except:
				properties.loc[ind,'rating'] = "new"
				properties.loc[ind,'num_ratings'] = 0
			finally:
				pass
			properties.loc[ind,'url'] = "https://www.airbnb.co.in/rooms/" + listing['id']
			properties.loc[ind,'latitude'] = listing['coordinate']['latitude']
			properties.loc[ind,'longitude'] = listing['coordinate']['longitude']

			ind += 1

		if data['nextPageCursor'] is not None:
			cursor = data['nextPageCursor']

			data = property_request(loc=location, cur=cursor) 

			# data = response.json()['data']
		else:
			run = False

	return properties


