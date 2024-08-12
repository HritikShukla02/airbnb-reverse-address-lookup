import pandas as pd
from request_retry import location_iq_req
from concurrent.futures import ThreadPoolExecutor



def process(df, ind):
    lat = df.loc[ind, 'latitude']
    long = df.loc[ind, 'longitude']

    data = location_iq_req(lat, long)
    
    df.loc[ind,'house_number'] = data['address']['house_number']
    df.loc[ind,'road'] = data['address']['road']
    df.loc[ind,'city'] = data['address']['city']
    df.loc[ind,'county'] = data['address']['county']
    df.loc[ind,'state'] = data['address']['state']
    df.loc[ind, 'postcode'] = int(data['address']['postcode'])
    df.loc[ind, 'country'] = data['address']['country']
    df.loc[ind, 'full_address'] = data['display_name']

def process_in_batches(df, batch_size):

    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        for index in df.index:
            executor.submit(process,df, index)

 
# Process DataFrame in batches of 1
def reverse_geocode(data):
    process_in_batches(data, 1)
    return data

