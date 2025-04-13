import os
import getopt
import sys
import exifread
from exif import Image
import piexif
from PIL import Image as ImagePil
import numpy as np
import reverse_geocoder as rg
import pycountry
from datetime import datetime

class HandleEXIF:
    hasexif=False
    version = ""

    def __init__(self,imagefilepath):
        self.imagefile = imagefilepath
        with open(imagefilepath, "rb") as handlefile:
            self.image = Image(handlefile)
            self.hasexif = self.image.has_exif
            #if self.hasexif:
            #    self.version = self.image.exif_version

    def get_datetime_original(self):

        try:
            date_str = self.image.datetime_original
            date_format = '%Y:%m:%d %H:%M:%S'
            date_obj = datetime.strptime(date_str, date_format)
            return date_obj
        except AttributeError:
            return None
    

    def format_altitude(self,altitude, altitude_ref):
        altitude_ref_text = "(above or below sea level not specified)"
        if altitude_ref == 0:
            altitude_ref_text = "above sea level"
        elif altitude_ref == 1:
            altitude_ref_text = "below sea level"
        return f"{altitude} meters {altitude_ref_text}"


    def dms_coordinates_to_dd_coordinates(self,coordinates, coordinates_ref):
        decimal_degrees = coordinates[0] + \
                        coordinates[1] / 60 + \
                        coordinates[2] / 3600
        
        if coordinates_ref == "S" or coordinates_ref == "W":
            decimal_degrees = -decimal_degrees
        
        return decimal_degrees

    def dec_to_dms(self,dec):
        
        '''
        Convert decimal degrees to degrees-minutes-seconds
        
        Parameters
        ----------
        dec : float
            Input coordinate in decimal degrees.
        
        Returns
        -------
        list
            Coordinate in degrees-minutes-seconds.
        '''
        degree = np.floor(dec)
        minutes = dec % 1.0 * 60
        seconds = minutes % 1.0 * 60
        minutes = np.floor(minutes)
        
        return (degree, minutes, seconds)
   
    def hasExif(self):
        return self.hasexif
    

    def get_dd_coordinates(self):
        try:
            print(self.image.gps_latitude, self.image.gps_latitude_ref)
            print(self.image.gps_longitude, self.image.gps_longitude_ref)
            decimal_latitude = self.dms_coordinates_to_dd_coordinates(self.image.gps_latitude, self.image.gps_latitude_ref)
            decimal_longitude = self.dms_coordinates_to_dd_coordinates(self.image.gps_longitude, self.image.gps_longitude_ref)
        except:
            print("NO COODINATE")
            decimal_latitude = None
            decimal_longitude = None
        
        return decimal_latitude,decimal_longitude
        
    def get_location(self,lat,lon):
        try: 
            coordinates =(float(lat),float(lon))#self.get_dd_coordinates() 
            location_info = rg.search(coordinates)[0]
            location_info['country'] = pycountry.countries.get(alpha_2=location_info['cc'])
            nazione =location_info['cc']
            citta = location_info['name']
            
        except:
            print("NO LOCATION")
            nazione = None   
            citta = None
        return nazione,citta 


    def Adel_get_location(self):
        try: 
            coordinates = self.get_dd_coordinates() 
            location_info = rg.search(coordinates)[0]
            location_info['country'] = pycountry.countries.get(alpha_2=location_info['cc'])
            nazione =location_info['cc']
            citta = location_info['name']
            
        except:
            print("NO LOCATION")
            nazione = None   
            citta = None
        return nazione,citta 
           
    def get_altitude(self):
        try:    
            #print(myimage.get_thumbnail)
            
            #print(f"{format_altitude(myimage.gps_altitude, myimage.gps_altitude_ref)}\n")
            altezzaslm = self.image.gps_altitude
        except:
            print("NO ALTITUDE")
            altezzaslm=None    
        return altezzaslm
    
    def set_coords(self,lat,lon):
        # Latitude and Longitude
        lat_deg, lat_min, lat_sec = self.dec_to_dms(lat)
        lon_deg, lon_min, lon_sec = self.dec_to_dms(lon)


        if lat_deg > 0 :
            self.image.gps_latitude_ref = "N"
        else: 
            self.image.gps_latitude_ref = "S"
            lat_deg = -1*(lat_deg)
        
        self.image.gps_latitude = (lat_deg, lat_min, lat_sec)

        
        if lon_deg > 0:
            self.image.gps_longitude_ref = "E"
        else:
            self.image.gps_longitude_ref = "W"
            lon_deg = -1*(lon_deg)
        self.image.gps_longitude = (lon_deg, lon_min, lon_sec)

        #self.image.gps_altitude = 199.034  # in meters
        with open(self.imagefile, 'wb') as new_image_file:
            new_image_file.write(self.image.get_file())

    def add_coords(self, lat,lon):
        '''
        Add coordinates to the Exif data of a .jpg file.

        Parameters
        ----------
        path : str
            Full path to the image file.
        coordinates : list or tuple of float
            Latitude and longitude that shall be added to the image file.

        Returns
        -------
        None.
        '''
        img = ImagePil.open(self.imagefile)
        try:
            exif_dict = piexif.load(img.info['exif'])
        except KeyError:
            exif_dict = {'0th':{},'Exif':{},'GPS':{},'1st':{},'thumbnail':None}
        #exif_dict = piexif.load(img['exif'])

        # Latitude and Longitude
        lat_deg, lat_min, lat_sec = self.dec_to_dms(lat)
        lon_deg, lon_min, lon_sec = self.dec_to_dms(lon)
        
        # Set GPS Info
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = [(abs(int(lat_deg)),1), (int(lat_min),1), (int(lat_sec),1)]
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = 'N' if lat >= 0 else 'S'
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = [(abs(int(lon_deg)),1), (int(lon_min),1), (int(lon_sec),1)]
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = 'E' if lon >= 0 else 'W'
        
        exif_bytes = piexif.dump(exif_dict)
        
        img.save(self.imagefile, exif=exif_bytes)
        
        return True