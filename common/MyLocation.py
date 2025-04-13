import numpy as np
import reverse_geocoder as rg
import pycountry
from geopy.geocoders import Nominatim

class MyLocation():
    latlon=(0,0)
    def __init__(self,lat,lon):
        self.latlon = (lat,lon)
    
    def getLoc2(self):
 
        # Creating a geocoder object
        geolocator = Nominatim(user_agent="my_app")
        
        # Reverse geocoding coordinates
        #ll =f"{self.latlon[0]},{self.latlon[1]}"
        address = geolocator.reverse("{}, {}".format(self.latlon[0], self.latlon[1]),language="IT")
        if address is not None:
            print(address)
        else:
            print("Coordinates not found")
        return address.address
    def get_location(self):
        try: 
            #coordinates = self.get_dd_coordinates() 
            location_info = rg.search(self.latlon,mode=1)#[0]
            print(location_info)
            location_info['country'] = pycountry.countries.get(alpha_2=location_info['cc'])
            #print(location_info['country'])
            nazione =location_info['cc']
            citta = location_info['name']
            
        except:
            #print("NO LOCATION")
            nazione = None   
            citta = None
        return nazione,citta 