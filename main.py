import pandas as pd
from airbnb import search_by_location, search_location
from location import reverse_geocode
from owner_info import owner_info
import os


def choice_geocode():
    while True:
        choice = input("Would you like us to procced to next step,i.e.gathering owner details for found properties (y/n): ")
        if choice == "n":
            print('Thank You for your trust.')
            print('Terminating the program!!!')
            return choice
        elif choice == "y":
            return choice
        else:
            print('wrong input ⚠️')
          

def choice_runagain():
    while True:
        choice = input("Would you like to run again? (y/n): ")
        if choice == "n":
            print('Thank You for your trust.')
            print('Terminating the program!!!')
            return choice
        elif choice == "y":
            return choice
        else:
            print('wrong input ⚠️')


run = True
while run:
    locate = input("Enter the search location or type 'exit' to close the program: ")
    if locate == "exit":
        print('Thank You for your trust.')
        print('Terminating the program!!!')
        run = False
    else:
        print("\n")
        print("Searching for list of locations ... ")
        location = search_location(locate)

        print("\n")
        print("Searching for listed properties in " + location + "⌚⌚⌚")
        properties = search_by_location(loc=location)

        print("\n")
        print(f"Total number of listed properties found in '{location}': {properties.shape[0]}")

        choice = choice_geocode()
        if choice == "n":
            properties.to_csv(f"{location}.csv")
            run = False
        elif choice == "y":
            print("\n")
            print("Reverse geo-coding the addresses for found properties 🏡🏡🏡")
            properties_with_address = reverse_geocode(properties)
            print('\n')
            print(f"successfully found addresses for {properties_with_address['full_address'].count()} properties.")

            print('\n')
            print('Gathering Owner Details for each property 🫅🫅🫅')
            master_properties = owner_info(properties_with_address)

            master_properties.to_csv(f'./output/{location}.csv')


            summary_data = {
                "summary":['Total_listings', 'Owner_names_found', 'Owner_contacts_found', 'Owner_email_1_found', 'Owner_email_2_found'],
                "count":[master_properties['id'].count(), master_properties['owner'].count(), master_properties['contact'].count(), master_properties['owner_email_1'].count(), master_properties['owner_email_2'].count()]
            }
            print('All the required data is collected and stored in Output folder📁')
            print("Generatting quick Summary of Output data:")
            summary = pd.DataFrame(data=summary_data)
            print(summary)
            print('\n\n')
            choice = choice_runagain()
            if choice == "y":
                os.system('cls')
            elif choice == "n":
                run =False
                
