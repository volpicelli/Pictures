from common.MyExifTool import MyExifTool
import sys
import os.path
from os import walk
import urllib3
import ast
"""
'image/jpeg'
video/mp4'
'video/quicktime'
"""

proj_path = "/srv/Pictures/"
# This is so Django knows where to find
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pictures.settings")
import django
django.setup()

sys.path.append(proj_path)
from home.models import MediaFile,Media2Album,Immagine,Image2Album,Album

dir2transfer = sys.argv[1]
w = walk(dir2transfer)

#a = os.path.basename(dir2transfer)
#album=a.replace(" ", "")
#print("ALBUM",album)
A = Album.objects.get(pk=1)
#A.save()
album='Varie'
form = 'json' 

for (dirpath, dirnames, filenames) in w:
        print(os.path.basename(dir2transfer))

        for file in filenames:
                print(file)
                #print(os.path.join(dirpath,file))
                met = MyExifTool(os.path.join(dirpath,file))

                

                if 'video' in met.MIMEType:
                    print("VIDEO")
                    ret = met.read_video_metadata()
                    lat = ret['latitude']
                    lon = ret['longitude']
                    altitude = ret['altitude']
                    createdate = ret['createdate']
                    width = ret['width']
                    height = ret['height']
                    duration = ret['duration']
                    rotation = ret['rotation']
                    mimetype = ret['mimetype']
                    exif = ret['exif']

                    m = MediaFile(first_album_id=A.id)
                    m.save()
                    m.media = os.path.join(os.path.basename(dir2transfer),file)
                    m.save()
                    Media2Album(media=m,album=A).save()
                    m.lat = lat
                    m.lon = lon
                    m.altezzaslm = altitude
                    m.data = createdate
                    m.width = width
                    m.height = height
                    m.duration = duration
                    m.rotation = rotation
                    m.exif = exif
                    if lat is not None :
                        m.gps_location = 1
                    #m.save()
                    #print('LAT',lat)
                    if lat is not None:
                        response = urllib3.request("GET",f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format={form}")
                        
                        dict_str = response.data.decode("UTF-8")
                        mydata = ast.literal_eval(dict_str)
                        #print(repr(mydata))
                        citta=None
                        road=None
                        nazione=None
                        provincia=None

                        if 'address' in mydata.keys():
                            if 'city' in mydata['address'].keys():
                                citta = mydata['address']['city']
                            if 'village' in mydata['address'].keys():
                                citta = mydata['address']['village']
                            if 'municipality' in mydata['address'].keys():
                                provincia = mydata['address']['municipality']
                            if 'road' in mydata['address'].keys():        
                                road = mydata['address']['road']
                            if 'country' in mydata['address'].keys():
                                nazione = mydata['address']['country']
                            if 'display_name' in mydata.keys():
                                display_name = mydata['display_name']
                        
                        m.citta = citta
                        m.nazione = nazione
                        m.road = road
                        m.display_name = mydata['display_name']
                        m.save()

                        print('Road:', road, 'Citta:', citta , 'Provincia:', provincia ,'Nazione:', nazione, 'Display Name:',mydata['display_name'] )
                        print()

                elif 'image' in met.MIMEType:
                    print("IMMAGINE")

                    ret = met.read_image_metadata()
                    lat = ret['latitude']
                    lon = ret['longitude']
                    altitude = ret['altitude']
                    createdate = ret['createdate']
                    width = ret['width']
                    height = ret['height']
                    mimetype = ret['mimetype']
                    exif = ret['exif']


                    m = Immagine(first_album_id=A.id)
                    m.save()
                    m.image = os.path.join(os.path.basename(dir2transfer),file)
                    m.save()
                    m.lat = lat
                    m.lon = lon
                    m.altezzaslm = altitude
                    m.data = createdate
                    m.width = width
                    m.height = height
                    m.exif = exif
                    if lat is not None :
                        m.gps_location = 1
                    Image2Album(image=m,album=A).save()
                    #print('LAT',lat)
                    if lat is not None:
                        response = urllib3.request("GET",f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format={form}")
                        
                        dict_str = response.data.decode("UTF-8")
                        mydata = ast.literal_eval(dict_str)
                        #print(repr(mydata))
                        citta=None
                        road=None
                        nazione=None
                        provincia=None
                        display_name=None

                        if 'address' in mydata.keys():

                            if 'city' in mydata['address'].keys():
                                citta = mydata['address']['city']
                            if 'village' in mydata['address'].keys():
                                citta = mydata['address']['village']
                            if 'municipality' in mydata['address'].keys():
                                provincia = mydata['address']['municipality']
                            if 'road' in mydata['address'].keys():        
                                road = mydata['address']['road']
                            if 'country' in mydata['address'].keys():
                                nazione = mydata['address']['country']
                            if 'display_name' in mydata.keys():
                                display_name = mydata['display_name']

                        m.citta = citta
                        m.nazione = nazione
                        m.road = road
                        m.display_name = display_name
                        m.save()

                        print('Road:', road, 'Citta:', citta , 'Provincia:', provincia ,'Nazione:', nazione, 'Display Name:',display_name)
                        print()

                



                
                
                
exit()
imgs = Immagine.objects.all()[:30]
for img in imgs:
    print(img.image.name)
    met = MyExifTool(os.path.join('/srv/media',img.image.name))
    print("MIMETYPE",met.MIMEType)
    if 'video' in met.MIMEType:
        print("VIDEO")
        ret = met.read_video_metadata()
    else:
        ret = met.read_image_metadata()
    print(ret)
exit()




#met = MyExifTool()
media_file = sys.argv[1]
met = MyExifTool(media_file)
#extension = os.path.splitext(media_file)[1]
#print(extension)
print(met.md)
#print(met.MIMEType)

#print(met.get_coordinates(media_file))

#extension = os.path.splitext(media_file)[1]
#print(extension)
if 'video' in met.MIMEType:
    ret = met.read_video_metadata()
else:
    ret = met.read_image_metadata()
print(ret)

#print(met.get_coordinates(media_file))
