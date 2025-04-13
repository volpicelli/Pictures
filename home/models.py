# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from exif import Image
import PIL
from geopy.geocoders import Nominatim
from django.conf import settings
import os,re
from django.core.files.base import ContentFile
from datetime import datetime
import urllib3
import ast
"""
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.user.id, filename)


class MyModel(models.Model):
    upload = models.FileField(upload_to=user_directory_path)
"""
class Album(models.Model):
    #id = models.AutoField(blank=True, null=True)
    nome = models.TextField(blank=True, null=True,unique=True)
    create = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    dataviaggio = models.DateField(blank=True,null=True)
    descrizione = models.TextField(blank=True, null=True)
    multianno = models.BooleanField(blank=True, null=True,default=False)
    multefoto = models.BooleanField(blank=True, null=True,default=False)
    # multianno - Album raccolta di foto di anni diversi messe tutte insieme.
    # tipo album PEPE o MUSH ..... 
    # Da motrare in maniera diversa da un album di un periodo limitato a pochi giorni e/o settimane
    # molytefoto - Album con molte foto in un periodo limitato ( 1/2 settimane ) da presentare divese per giorni


    class Meta:
        managed = True
        db_table = 'album'


class MediaFile(models.Model):
    def set_path(self,filename):
        an = Album.objects.get(pk=self.first_album_id)
        albumname= re.sub('[^a-zA-Z0-9]+', '', an.nome)
        return albumname +'/'+filename
    #id = models.AutoField(blank=True, null=True)
    
    media = models.FileField(upload_to=set_path,null=True,blank=True)
    #media = models.FileField(upload_to='mediafile/',null=True,blank=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    rotation = models.IntegerField(blank=True, null=True)
    display_name = models.TextField(blank=True, null=True)
    exif = models.BooleanField(blank=True, null=True,default=False)
    gps_location = models.BooleanField(blank=True, null=True,default=False)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    altezzaslm = models.FloatField(blank=True, null=True)
    display_name = models.TextField(blank=True, null=True)
    road = models.CharField(max_length=80,blank=True, null=True)
    citta = models.TextField(blank=True, null=True)
    nazione = models.TextField(blank=True, null=True)
    data = models.DateTimeField(blank=True, null=True)
    first_album_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'MediaFile'


class Immagine(models.Model):
    #id = models.AutoField(blank=True, null=True)
    def set_path(self,filename):
        an = Album.objects.get(pk=self.first_album_id)
        albumname= re.sub('[^a-zA-Z0-9]+', '', an.nome)
        print("PIPPO",albumname +'/'+filename)
        return albumname +'/'+filename
    #image = models.ImageField(null=True,blank=True)
    image = models.ImageField(upload_to=set_path,null=True,blank=True)
    #image = models.ImageField(upload_to='foto/%Y/%m/%d/',null=True,blank=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    display_name = models.TextField(blank=True, null=True)
    road = models.CharField(max_length=80,blank=True, null=True)
    exif = models.BooleanField(blank=True, null=True,default=False)
    gps_location = models.BooleanField(blank=True, null=True,default=False)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    altezzaslm = models.FloatField(blank=True, null=True)
    citta = models.CharField(max_length=80,blank=True, null=True)
    nazione = models.CharField(max_length=80,blank=True, null=True)
    data = models.DateTimeField(blank=True, null=True)
    #album_id serve per creare una directory con il riferimento all'album
    # utilizzato in set_path nel modello Immagine. Porebbe chiamarsi first_album_id
    # 
    first_album_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'immagine'


    #def set_path(self,filename):
    #    an = Album.objects.get(pk=self.album_id)
    #    return 'foto/'+an.nome

    #@property
    #def album_name(self):
    #    return self.album_name
    
    def setAlbumName(self,album_name):
        self.album_name = album_name
        #return album_name

    def decimal_coords(self,coords, ref):
        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref == "S" or ref == "W":
            decimal_degrees = -decimal_degrees
        return decimal_degrees
    

    def get_datetime_original(self):
        img_path= os.path.join(settings.MEDIA_ROOT,self.image.path)
        #print(img_path)
        with open(img_path, 'rb') as src:
            img = Image(src)
        if img.has_exif:
            try:
                date_str = img.datetime_original
                date_format = '%Y:%m:%d %H:%M:%S'
                date_obj = datetime.strptime(date_str, date_format)
                return date_obj
            except AttributeError:
                return None
        else:
            return None

    """
    def get_datetime_original(self,file):
        #img_path= os.path.join(settings.MEDIA_ROOT,self.image.path)
        #print(img_path)
        with open(file, 'rb') as src:
            img = Image(src)
        if img.has_exif:
            try:
                return img.datetime_original
            except AttributeError:
                return None
        else:
            return None
    """
    
    def get_image_coordinates(self):
        #print(img_path)
        img_path= os.path.join(settings.MEDIA_ROOT,self.image.path)
        #print(img_path)
        with open(img_path, 'rb') as src:
            img = Image(src)
        if img.has_exif:
            try:
                #print( img.gps_longitude,img.gps_latitude)
                latdec = self.decimal_coords(img.gps_latitude,img.gps_latitude_ref)
                londec = self.decimal_coords(img.gps_longitude,img.gps_longitude_ref)
            except AttributeError:
                latdec = None
                londec = None
            try:
                altitude = img.gps_altitude
            except AttributeError:
                altitude = None
                #coords = (self.decimal_coords(img.gps_latitude,
                #        img.gps_latitude_ref),
                #        self.decimal_coords(img.gps_longitude,
                #        img.gps_longitude_ref),img.gps_altitude)
                #return coords[0],coords[1],coords[2] # lat,lon,altezza
                
            return latdec,londec,altitude
                
        else:
            return None,None,None
        #print(f"Was taken: {img.datetime_original}, and has coordinates:{coords}")
        #print(coords[0],coords[1],img.datetime_original)
    
    def imageHasExif(self):
        img_path = os.path.join(settings.MEDIA_ROOT,self.image.path)

        # village , town , city 

        with open(img_path, 'rb') as img_file:
            img = Image(img_file)
            if img.has_exif:
                info = f" has the EXIF " #{img.exif_version}"
            else:
                info = "does not contain any EXIF information"
            #print(f"Image {img_file.name}: {info}")
            
        return img.has_exif
        
    def get_location_osm(self,lat,lon):
        form = 'json'
        response = urllib3.request("GET",f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format={form}")

        #print(response.data['address'])
        #ja=json.loads(response.data)#.decode('utf-8'))
        #print(ja)
        dict_str = response.data.decode("UTF-8")
        mydata = ast.literal_eval(dict_str)
        #print(repr(mydata))
        citta=None
        road=None
        nazione=None
        provincia=None
        display_name = None

        try:

            if 'city' in mydata['address'].keys():
                citta = mydata['address']['city']
            if 'village' in mydata['address'].keys():
                citta = mydata['address']['village']
            if 'town' in mydata['address'].keys():
                citta = mydata['address']['town']
            if 'municipality' in mydata['address'].keys():
                provincia = mydata['address']['municipality']
            if 'road' in mydata['address'].keys():        
                road = mydata['address']['road']
            if 'country' in mydata['address'].keys():
                nazione = mydata['address']['country']

            display_name = mydata['display_name'] 
        except:
            a=2

        return citta,road,nazione,display_name

    def get_image_location(self,lat,lon):
        geolocator = Nominatim(user_agent="AntonioMyFoto")

        citta=None
        nazione=None
        display_name=None

        if lat is not None:
            location = geolocator.reverse(str(lat)+","+str(lon),timeout=1000)
        else:
            return citta,nazione,display_name
        # Display
        #print('Location',location)
        #print('Nazione',location['country'])
        address = location.raw['address']
        display_name = location.raw['display_name']
        #print(address)
        

        if 'city' in address.keys():
            citta = address['city']
            #print('City',address['city'])
        if 'village' in address.keys():
            #print('Village',address['village'])
            citta = address['village']
        if 'town' in address.keys():
            #print('Town',address['town'])
            citta = address['town']
        if 'municipality' in address.keys():
            citta = address['municipality']
        if 'country_code' in address.keys():
            nazione = address['country_code']
        return citta,nazione,display_name
 


class Image2Album(models.Model):
    image = models.ForeignKey(Immagine, on_delete=models.CASCADE,related_name='immagini',null=True,related_query_name='bbb')
    album = models.ForeignKey(Album, on_delete=models.CASCADE,related_name='albums',null=True,related_query_name='aaa') #IntegerField(blank=True, null=True)
 
    class Meta:
        managed =True 
        db_table = 'image2album'

class Media2Album(models.Model):
    media = models.ForeignKey(MediaFile, on_delete=models.CASCADE,related_name='mediamedia',null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE,related_name='mediaalbums',null=True) #IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'media2album'
