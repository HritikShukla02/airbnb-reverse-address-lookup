import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote_plus, urljoin
from concurrent.futures import ThreadPoolExecutor

from request_retry import owner_request_2




def process(df, index):
    # print(df.loc[index])

    h_no = df.loc[index, 'house_number']
    road = df.loc[index, 'road']
    city = df.loc[index, 'city']
    state = df.loc[index, 'state']
    postcode = df.loc[index, 'postcode']
   
  

    try:
        address = f"{str(int(h_no))}, {road}"
    except:
        address = f"{str(h_no)}, {road}"

    locality = f"{city}, {state}, {str(int(postcode))}"
    print(address)
    print(locality)


    url = f'https://www.truepeoplesearch.com/resultaddress?streetaddress={quote_plus(address)}&citystatezip={quote_plus(locality)}'
    
    try:
        r = owner_request_2(url=url)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    else:

        # if r is not None:
        soup = BeautifulSoup(r.content, "html.parser")
        try:

            link = soup.select_one(selector='a.btn.btn-success.btn-lg.detail-link.shadow-form')
            if link is not None:
                link = link.get('href')
                
            else:
                raise Exception

            new_url = urljoin(base='https://www.truepeoplesearch.com', url=link)
    
            res = owner_request_2(url=new_url)
            if link is None:
                raise Exception
        except:
            print("\n")
            print("No details present for address: "+ address )
            print("\n")

        else:
            if res is not None:
                soup = BeautifulSoup(res.content, "html.parser")

                # Finding Owner name
                name = soup.select_one(selector='div.col > h1.oh1').get_text().strip()
                df.loc[index, 'owner'] = name
                
                # Owner's current address
                curr_street_add = soup.select_one(selector='span[itemprop="streetAddress"]').get_text().strip()
                df.loc[index, 'curr_address'] = curr_street_add
                
                    
                #Owner's Locality
                curr_locality = soup.select_one(selector='span[itemprop="addressLocality"]').get_text().strip()
                curr_region = soup.select_one(selector='span[itemprop="addressRegion"]').get_text().strip()
                curr_postalcode = soup.select_one(selector='span[itemprop="postalCode"]').get_text().strip()

                df.loc[index, 'owner_locality'] = f"{curr_locality}, {curr_region} {curr_postalcode}"

                
                #Owner's Contact
                contact = soup.select_one(selector='span[itemprop="telephone"]').get_text().strip()
                df.loc[index, 'contact'] = contact
                
                #Owner's mail address
                email_1 = soup.select_one(selector='#personDetails > div:nth-child(13) > div.col-12.col-sm-11.pl-sm-1 > div:nth-child(2) > div > div').get_text().strip()
                if "@" in email_1:
                    df.loc[index, 'owner_email_1'] = email_1

                email_2 = soup.select_one(selector='#personDetails > div:nth-child(13) > div.col-12.col-sm-11.pl-sm-1 > div:nth-child(3) > div > div').get_text().strip()
                if "@" in email_2:
                    df.loc[index, 'owner_email_2'] = email_2

            # print(df.loc[index])
            # return row

def process_in_batches(df, batch_size):

    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        for index in df.index:
            executor.submit(process,df, index)

 
# Process DataFrame in batches of 5

def owner_info(data):
    process_in_batches(data, 5)
    return data















