from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDay,TruncMonth
from django.http import FileResponse
from django.conf import settings
from home.models import Image2Album,Album,Immagine,MediaFile,Media2Album
from common.MyExifTool import MyExifTool
from common.MyLocation import MyLocation
from home.handleExif import HandleEXIF
from .immagine_serializer import ImmagineSerializer
import magic
import os,time
import json
# Create your views here.
import reverse_geocoder as rg
import pycountry
import urllib3
import ast

import shutil 

class RileggiDataSelezionate(APIView):
    def post(self,request):
        par=json.loads(request.body)
        dd=par['paramName']
        #new_album = par['album']

        #imq=Image2Album.objects.filter(album_id=new_album)
        #print("DIR NEW",os.path.dirname(imq[0].image.image.name))
        #dest_dirname = os.path.dirname(imq[0].image.image.name)
        res=[]
        for one in dd :
        
            img = Image2Album.objects.get(pk=one)
            path=os.path.join(settings.MEDIA_ROOT,img.image.image.name)
            met = MyExifTool(path)
            exiftool = met.read_image_metadata()
            img.image.data = exiftool['createdate']
            img.image.save()
            res.append(exiftool)

        #with open(path, ') as image_file:
        return Response(res)

class RegistraData(APIView):
    def post(self,request):

        id=request.POST.get('id')
        regdata = request.POST.get('data')
        im = Immagine.objects.get(pk=id)
        im.data = str(regdata)
        im.save()
        serializer = ImmagineSerializer(im)#,many=True)

        return Response(serializer.data)

class CallApi(APIView):
    def post(self,request):
        #par = request.POST.get('paramName')
        par=json.loads(request.body)
        dd=par['paramName']
        new_album = par['album']

        imq=Image2Album.objects.filter(album_id=new_album)
        #print("DIR NEW",os.path.dirname(imq[0].image.image.name))
        dest_dirname = os.path.dirname(imq[0].image.image.name)
        
        for one in dd :
            im=Image2Album.objects.get(pk=one)
            source_path = im.image.image.path
            #print("SOURCE PATH",source_path)
            #print("Image_ID",im.image.id)
            source_name = im.image.image.name
            #print("SOURCE NAME",source_name)
            dest_name = os.path.join(dest_dirname,os.path.basename(source_path))
            #print("DEST NAME",dest_name)
            #im.image.image.name = os.path.basename(initial_path)
            #print("filename",im.image.image.name)
            #print("AAA",imq[0].image.image.name)
            dest_path = os.path.join(settings.MEDIA_ROOT ,dest_dirname,os.path.basename(source_path))
            #print("DEST PATH",dest_path)

            os.rename(source_path, dest_path)
            pp=Image2Album(album_id=new_album,image_id=im.image.id)
            pp.image.image.name= dest_name #os.path.join('Bretagna2024',os.path.basename(initial_path))
            pp.image.save()
            pp.save()
            im.delete()

        return Response(par)

class EliminaFotoDaAlbum(APIView):
    def post(self,request):
        #par = request.POST.get('paramName')
        par=json.loads(request.body)
        dd=par['paramName']
        album = par['album']
        
        for one in dd :
            i2a=Image2Album.objects.get(pk=one)
            im_id=i2a.image.id
            i2ai=Image2Album.objects.filter(image_id=im_id)
            if len(i2ai) == 1:
                # album_id=1 => VArie
                pp=Image2Album(album_id=1,image_id=im_id)
                i2ai[0].delete()
                pp.save()
            if len(i2ai) > 1:
                i2ai.get(album_id=album).delete()
        
        msg = {}
        msg['success'] = "Eliminati dall'album :"
        msg['image2Abum ID'] = par
        return Response(msg)
            

class AncheAltroAlbum(APIView):
    def post(self,request):
        #par = request.POST.get('paramName')
        par=json.loads(request.body)
        dd=par['paramName']
        altro_album = par['album']


        #imq=Image2Album.objects.filter(album_id=altro_album)
        #dest_dirname = os.path.dirname(imq[0].image.image.name)
        
        for one in dd :
            im=Image2Album.objects.get(pk=one)
            #source_path = im.image.image.path
            
            #source_name = im.image.image.name
            #dest_name = os.path.join(dest_dirname,os.path.basename(source_path))
            #dest_path = os.path.join(settings.MEDIA_ROOT ,dest_dirname,os.path.basename(source_path))

            #os.rename(source_path, dest_path)
            pp=Image2Album(album_id=altro_album,image_id=im.image.id)
            #pp.image.image.name= dest_name #os.path.join('Bretagna2024',os.path.basename(initial_path))
            #pp.image.save()
            pp.save()
            #im.delete()

        return Response(par)
 


class DeleteMultipleFoto(APIView):
    def post(self,request):
        par=json.loads(request.body)

        dd=par['paramName'][0]
        par['dd']=dd
        for one in par['paramName']:
            im = Image2Album.objects.get(pk=one)

            if os.path.exists(os.path.join(settings.MEDIA_ROOT,im.image.image.name)):
                im.image.delete()
                im.delete()
                os.remove(os.path.join(settings.MEDIA_ROOT,im.image.image.name))
                
                msg=f"File {os.path.join(settings.MEDIA_ROOT,im.image.image.name)} is deleted {request.META.get('HTTP_REFERER')}"
            else:
                msg=f"The file  {os.path.join(settings.MEDIA_ROOT,im.image.image.name)} does not exist {request.META.get('HTTP_REFERER')}"
        return Response(msg)   
            #Image2Album.objects.get(image_id=one).delete()
            #Immagine.objects.get(id=one).delete()

        #return Response(par)



class PopulateModalCarousel(APIView):
    def get(self, request,album_id,img_id=None):
            
            if img_id :
                foto = Image2Album.objects.filter(album=album_id).order_by('image__data')
                nfoto = foto.filter(id__gte=img_id)
                mf = []
                for one in nfoto:
                     tmp = {'path':one.image.image.name,'id':one.id,'citta':one.image.citta,'data': one.image.data,'lat':one.image.lat,'lon':one.image.lon}

                     mf.append(tmp)
                  
        
            return Response(mf)
# b=a.albums.all().annotate(key=Trunc('image__data','day'))
#>>> from django.db.models.functions import TruncDay
#>>> t = b.annotate(day=TruncDay('image__data')).values('day').annotate(c=Count('id'))
#>>> t#
class Test(APIView):
    def get(self,request):
        a = Album.objects.get(pk=3)
        i2abb = a.albums.all()#.annotate(key=Trunc('image__data','day')) #.values('image__data__year','image__data__month','image__id').annotate(total=Count('id'))
        #i2abb = a.albums.all().order_by('-image__data__year','-image__data__month').values('image__data__year','image__data__month','image__id').annotate(total=Count('id'))
        #i2a = a.albums.all().order_by('-data__year','-data__month').values('data__year','data__month').annotate(total=Count('id'))
        t = i2abb.annotate(month=TruncMonth('image__data')).values('month').annotate(c=Count('id'))
        r=[]

        for s in t:
                #i = s.values('image__data__year','image__data__month').annotate(total=Count('id'))
                item={}
                item['year'] = s['month'].year
                item['month'] = s['month'].month
                dd = s['month'].strftime('%Y-%m-%d')
                item['total'] = s['c']
                months=['tt','Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre']
                item['nomemese']=months[s['month'].month]
                
                im=i2abb.filter(image__data__year=s['month'].year,image__data__month=s['month'].month).order_by('-image__data')
                fotos=[]
                for i in im:
                    ora = i.image.data.strftime("%H:%M:%S")
                    dd = i.image.data.strftime('%Y-%m-%d')
                    f={'id':i.image.id,
                          'foto': i.image.image.name,
                          'ora': ora,#i.image.data,#.time(),
                          'lat':i.image.lat,
                          'lon':i.image.lon,
                          'citta':i.image.citta,
                          'data': dd }# i.image.data}#.date}

                    #g={'id':i.image.id,'name':i.image.image.name,'data':i.image.data}
                    fotos.append(f)
                item['foto']=fotos
                r.append(item)
                """
                if s.image.data.month is not None: #s['image__data__month'] is not None:
                        #print(i['data__year'],i['data__month'],i['data__day'],i['total'])
                        ###date = str(i['data__year'])+'-'+str(i['data__month'])+'-'+str(i['data__day'])
                        #print(date)
                        #item['date']=i['data__date']#date

                        item['year']= s.image.data.year #s['image__data__year']
                        item['month']=s.image.data.month #s['image__data__month']
                        item['nomemese']=months[s.image.data.month]#s['image__data__month']]
                        
                        #item['date']=s['image__data']
                        #item['total'] = s['total']
                        #id = s['image__id']
                        
                        i2 = Immagine.objects.get(id=s.image.id) #id) #,data__year=i['data__year'],data__month=i['data__month'])
                        fotos=[]
                        #for i2 in im2:
                        foto={'id':i2.id,'ora':i2.data,
                                'lat':i2.lat,'lon':i2.lon,'citta':i2.citta,'data':i2.data,'ora':i2.data.time(),'year':i2.data.year,'month':i2.data.month,'day':i2.data.day}
                        fotos.append(foto)
                        #        print(i2.image.name,i2.data.time())
                        item['fotos']=fotos

                        r.append(item)
                """


        """

        for i in i2a:
            d={}
            d['id'] = i.image.id
            d['citta'] = i.image.citta
            d['lat'] = i.image.lat
            d['lon'] = i.image.lon
            d['display'] = i.image.display_name
            d['data'] = i.image.data
            #d['time'] = i.image.data.time
            d['file'] = i.image.image.name
            
            r.append(d)
        """
        return Response(r)



class DeleteImage(APIView):
    def get(self, request,img_id=None):
        im = Image2Album.objects.filter(pk=img_id)
        for one in im:

            if os.path.exists(os.path.join(settings.MEDIA_ROOT,one.image.image.name)):
                one.image.delete()
                os.remove(os.path.join(settings.MEDIA_ROOT,one.image.image.name))
                
                msg=f"File {os.path.join(settings.MEDIA_ROOT,one.image.image.name)} is deleted {request.META.get('HTTP_REFERER')}"
            else:
                msg=f"The file  {os.path.join(settings.MEDIA_ROOT,one.image.image.name)} does not exist {request.META.get('HTTP_REFERER')}"
        return Response(msg)    
        


class CreaAlbum(APIView):
    def post(self,request):
        nome=request.POST.get('nome',None)
        descr = request.POST.get('descrizione',None)
        created=False
        if nome:
            try:
                na = Album(nome=nome,descrizione=descr)
                na.save()
                created=True
            except:
                na = Album.objects.get(nome=nome)
                return Response({'success': 'warning' ,'msg': " Album esiste  ",'id':na.id,'created': created})
                
            if created:
                return Response({'success': True,'msg': "Album creato ",'id': na.id,'created':created})
            else:
                return Response({'success': 'warning','msg': "Album Esiste ",'id': na.id,'created':created})
        
        return Response({'success': False,'msg': " ERRORE "})



class UploadMediaFile(APIView):

    def post(self,request,album_id=None):
        files = [request.FILES.get('file[%d]' % i)
                 for i in range(0, len(request.FILES))]  
        #files = request.POST.getlist('file')
        if album_id == None:
            album_id = 1
            a = Album.objects.get(id=album_id)

        else:
            a = Album.objects.get(id=album_id)
        
        #        instance = Immagine(album_id=a.id)
        if files:
            form = 'json'
            
            for f in files:
                ftype = magic.from_file(f.temporary_file_path(), mime=True)
                
                #instance = MediaFile(first_album_id=album_id)
                #instance.save()
                #instance.media=f
                #instance.save()
                met = MyExifTool(f.temporary_file_path())
                #extension = os.path.splitext(media_file)[1]
                #print(extension)
                #print(met.md)
                #ftype  = met.MIMEType
                if "video" in ftype:
                    instance = MediaFile(first_album_id=album_id)
                    instance.save()
                    #instance.setAlbumName("WWWWWW")
                    instance.media=f
                    instance.save()
                    #met = MyExifTool(instance.image.path)#f.temporary_file_path())

                    #csv_m = os.path.getmtime(instance.media.path)
                    #m_ti = time.ctime(csv_m)

                    #t_obj = time.strptime(m_ti)

                    # Transforming the time object to a timestamp 
                    # of ISO 8601 format
                    #m = met.read_video_metadata()


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

                    #m = MediaFile(media=os.path.join(album,file))
                    #m.save()
                    Media2Album(media=instance,album=a).save()
                    instance.lat = lat
                    instance.lon = lon
                    instance.altezzaslm = altitude
                    instance.data = createdate
                    instance.width = width
                    instance.height = height
                    instance.duration = duration
                    instance.rotation = rotation
                    instance.exif = exif
                    if lat is not None :
                        instance.gps_location = 1
                    #m.save()
                    #print('LAT',lat)
                    
                    if lat is not None:
                        response = urllib3.request("GET",f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format={form}&accept-language=en")
                        
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

                        instance.citta = citta
                        instance.nazione = nazione
                        instance.road = road
                        instance.display_name = display_name
                        instance.save()
                    #T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)
                    #creationDate = m['createdate'] # time.strftime("%Y-%m-%d %H:%M",t_obj)
                    #instance.data=creationDate
                    #instance.lat = m['latitude']
                    #nstance.lon = m['longitude']
                    #if instance.lat is not None:
                    #    ml = MyLocation(instance.lat,instance.lon)
                    #    nazione,citta = ml.get_location()
                    #instance.nazione = nazione
                    #instance.citta = citta

                if "image" in ftype:
                    instance = Immagine(first_album_id=album_id)
                    instance.save()
                    #instance.setAlbumName("WWWWWW")
                    instance.image=f
                    instance.save()
                    met = MyExifTool(instance.image.path)#f.temporary_file_path())

                    ret = met.read_image_metadata()
                    lat = ret['latitude']
                    lon = ret['longitude']
                    altitude = ret['altitude']
                    createdate = ret['createdate']
                    width = ret['width']
                    height = ret['height']
                    mimetype = ret['mimetype']
                    exif = ret['exif']


                    #m = Immagine(image=os.path.join(album,file))
                    #m.save()
                    instance.lat = lat
                    instance.lon = lon
                    instance.altezzaslm = altitude
                    instance.data = createdate
                    instance.width = width
                    instance.height = height
                    instance.exif = exif
                    if lat is not None :
                        instance.gps_location = 1
                    Image2Album(image=instance,album=a).save()
                    #print('LAT',lat)
                    if lat is not None:
                        response = urllib3.request("GET",f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format={form}&accept-language=en")
                        
                        dict_str = response.data.decode("UTF-8")
                        mydata = ast.literal_eval(dict_str)
                        #print(repr(mydata))
                        citta=None
                        road=None
                        nazione=None
                        provincia=None
                        display_name = None
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

                        instance.citta = citta
                        instance.nazione = nazione
                        instance.road = road
                        instance.display_name = display_name
                        instance.save()
                #a = Album.objects.get(id=album_id)
                
            return Response('<p>Info Saved! con files </p>') #str(instance._get_name))
            
        else:
            return Response('<p>Info Saved! senza files</p>')


class UploadImages2Album(APIView):

    def post(self,request,album_id=None):
        files = [request.FILES.get('file[%d]' % i)
                 for i in range(0, len(request.FILES))]  
        #files = request.POST.getlist('file')
        if album_id == None:
            album_id = 1
        if files:
            
            for f in files:
                a = Album.objects.get(id=album_id)
                instance = Immagine(first_album_id=a.id)
                #instance.setAlbumName("WWWWWW")
                instance.save()
                instance.image=f
                
                instance.save()
                #a = Album.objects.get(id=album_id)
                i2a=Image2Album(image=instance,album=a)
                i2a.save()
                tag=''
                i=HandleEXIF(os.path.join(settings.MEDIA_ROOT,i2a.image.image.name))
                if i.hasexif:
                    
                    instance.exif = True
                    date = i.get_datetime_original()
                   
                    instance.data= date
                   
                    lat,lon = i.get_dd_coordinates()
                   
                    instance.lat = lat
                    instance.lon = lon                        
                    instance.gps_location = True
                    citta,road,nazione,display_name = instance.get_location_osm(lat,lon) #instance.get_image_location(lat,lon)
                    #nazione,citta = i.get_location()
                    instance.citta = citta
                    instance.road = road
                    instance.nazione = nazione
                    instance.display_name= display_name

                    altezzaslm = i.get_altitude()
                    instance.altezzaslm = altezzaslm
                else:
                    tag='noinfo'
                
                instance.save()
            return Response('<p>Info Saved! con files </p>') #str(instance._get_name))
            
        else:
            return Response('<p>Info Saved! senza files</p>')

class GetLocation(APIView):
    def post(self,request,img_id):
        lat = request.POST.get("newlat")
        lon = request.POST.get("newlon")
        im=Immagine.objects.get(pk=img_id) 
        i=HandleEXIF(os.path.join(settings.MEDIA_ROOT,im.image.name))
        #nazione,citta = i.get_location()
        try:
            coordinates=(float(lat),float(lon))
        except:
            return Response((lat,lon))
        try:
            location_info = rg.search(coordinates)[0]
            location_info['country'] = pycountry.countries.get(alpha_2=location_info['cc'])
            nazione =location_info['cc']
            citta = location_info['name']
        except:
            print("NO LOCATION")
            nazione = None   
            citta = None

        response={}
        response['nazione']=nazione
        response['citta']=citta
        response['location'] = location_info

        return Response(response)
class SetCoordinates(APIView):
    def post(self,request,image_id):
        lat = request.POST.get("newlat")
        lon = request.POST.get("newlon")
        im=Immagine.objects.get(pk=image_id) 

        i=HandleEXIF(os.path.join(settings.MEDIA_ROOT,im.image.name))
        #i.set_coords(float(lat),float(lon))
        i.add_coords(float(lat),float(lon))
        
        #i=HandleEXIF(os.path.join(settings.MEDIA_ROOT,im.image.name))

        #lat,lon = i.get_dd_coordinates()
                   
        im.lat = float(lat)
        im.lon = float(lon)                        
        im.gps_location = True

        citta,road,nazione,display_name = im.get_location_osm(lat,lon) #instance.get_image_location(lat,lon)
        #nazione,citta = i.get_location()
        im.citta = citta
        im.road = road
        im.nazione = nazione
        im.display_name= display_name


        #nazione,citta = i.get_location(im.lat,im.lon)
        #im.citta = citta
        #im.nazione = nazione
        
        altezzaslm = i.get_altitude()
        im.altezzaslm = altezzaslm
    
    
        im.save()
        response = {'file': os.path.join(settings.MEDIA_ROOT,im.image.name),
                    'lat': im.lat,
                    'lon': im.lon,
                    'newlat':lat,
                    'newlon':lon,
                    'display_name':display_name }
        
        return Response(response)

"""
class UploadImages2AlbumOLD(APIView):
    def post(self,request,album_id):
        files = [request.FILES.get('file[%d]' % i)
                 for i in range(0, len(request.FILES))]  
        #files = request.POST.getlist('file')
        if files:
            
            for f in files:
                a = Album.objects.get(id=album_id)
                #album_name=a.nome
                instance = Immagine(album_id=a.id)
                #instance.setAlbumName("WWWWWW")
                instance.save()
                instance.image=f
                #instance = Immagine(image=f)
                #date = instance.test_get_datetime_original(f)
                instance.save()
                #a = Album.objects.get(id=album_id)
                i2a=Image2Album(image=instance,album=a)
                i2a.save()
                tag=''
                if instance.imageHasExif():
                    instance.exif = True
                    date = instance.get_datetime_original()
                    if date:
                        instance.data= date
                    else:
                        tag='nodate'
                    lat,lon,alt = instance.get_image_coordinates()
                    if lat:
                        instance.lat = lat
                        instance.lon = lon
                        instance.altezzaslm = alt
                        instance.gps_location = True
                        citta,address = instance.get_image_location(lat,lon)
                        instance.citta = citta
                    else:
                        tag='noloc'
                    
                else:
                    tag='noinfo'
                
                instance.save()
                                   
                #folder = os.path.join(settings.MEDIA_ROOT,)
                #fs = FileSystemStorage(location=folder)
        #for f in files:
        #    filename = fs.save(f.name, f)
            return Response('<p>Info Saved! con files </p>') #str(instance._get_name))
           
        else:
            return Response('<p>Info Saved! senza files</p>')
        
    
    
        def Test_get_datetime_original(self,file):
            # Questo legge il contenuto di un upload file non ancora salvato
            # file = request.FILES['file']
        
            
            img = Image( ContentFile(file.read()))
            if img.has_exif:
                try:
                    return img.datetime_original
                except AttributeError:
                    return None
            else:
                return None
""" 