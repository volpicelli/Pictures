from django.shortcuts import render
from os import walk
import magic,os
from django.db.models import Count
from django.db.models.functions import TruncDay,TruncMonth

from common.MyExifTool import MyExifTool

from django.views  import View
from django.db.models import Count
from .models import Image2Album,Album,Immagine,MediaFile
from django.http import FileResponse

# Create your views here.
class DownloadImage(View):
    def get(self,request,img_id):
        image = Immagine.objects.get(pk=img_id)
        filename = os.path.basename(image.image.name)
        response = FileResponse(open(image.image.path, 'rb'), as_attachment=True, filename="my_filename")
        response['Content-Disposition'] = f'attachment; filename={filename}'
        #response['Content-Type'] = 'application/octet-stream'
        #cheatsheet = get_object_or_404(Cheatsheet, pk=cheatsheet_id)
        return response
        
        file_path = image.image.path
        resp= image.image.url
        response = FileResponse(open(file_path, 'rb'),content_type=' image/jpg')
        response['Content-Disposition'] = 'attachment; filename=pollo.jpg'
        return response

class Media(View):
    
    template_name = "home/media.html"
    
 
    def get(self,request):
            # col setta il numero di foro per riga col=3 mette 4 colonne ( 3x4=12) col-2 ne mette 6 ( 2x6=12)
        #tmp = Immagine.objects.filter(album_id=49).order_by('-data')
        #im = Immagine.objects.filter(album_id=49).values('data__year','data__month','data__day').annotate(total=Count('id'))
        #im = tmp.values('data__year','data__month','data__day').annotate(total=Count('id'))#.order_by('-data')
        #im=Immagine.objects.filter(album_id=49).order_by('-data__date').values('data__year','data__month').annotate(total=Count('id'))
        im=Media.objects.filter(album_id=49).order_by('-data__year','-data__month').values('data__year','data__month').annotate(total=Count('id'))

        
        response=[]
        for i in im:
                item={}
                months=['tt','Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre']
                if i['data__month'] is not None:
                        #print(i['data__year'],i['data__month'],i['data__day'],i['total'])
                        ###date = str(i['data__year'])+'-'+str(i['data__month'])+'-'+str(i['data__day'])
                        #print(date)
                        #item['date']=i['data__date']#date
                        item['year']= i['data__year']
                        item['month']=i['data__month']
                        item['nomemese']=months[i['data__month']]
                        #item['date']=i['data__date']
                        item['total'] = i['total']
                        im2 = Immagine.objects.filter(album_id=49,data__year=i['data__year'],data__month=i['data__month'])
                        fotos=[]
                        for i2 in im2:
                                foto={'id':i2.id,'foto': i2.image.name,'ora':i2.data.time(),
                                      'lat':i2.lat,'lon':i2.lon,'citta':i2.citta,'data':i2.data.date}
                                fotos.append(foto)
                        #        print(i2.image.name,i2.data.time())
                        item['fotos']=fotos
                response.append(item)
        #album = Album.objects.all().order_by('-create').first()
        
        context={'items':response,'col':3}



        return render(request,self.template_name, context)

class Video(View):
        template_name = "home/video.html"

        def get(self,request):
            # col setta il numero di foto per riga col=3 mette 4 colonne ( 3x4=12) col-2 ne mette 6 ( 2x6=12)
        #tmp = Immagine.objects.filter(album_id=49).order_by('-data')
        #im = Immagine.objects.filter(album_id=49).values('data__year','data__month','data__day').annotate(total=Count('id'))
        #im = tmp.values('data__year','data__month','data__day').annotate(total=Count('id'))#.order_by('-data')
        #im=Immagine.objects.filter(album_id=49).order_by('-data__date').values('data__year','data__month').annotate(total=Count('id'))
                vi=MediaFile.objects.all().order_by('-data__year','-data__month').values('data__year','data__month').annotate(total=Count('id'))

                
                response=[]
                for i in vi:
                        item={}
                        months=['tt','Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre']
                        if i['data__month'] is not None:
                                #print(i['data__year'],i['data__month'],i['data__day'],i['total'])
                                ###date = str(i['data__year'])+'-'+str(i['data__month'])+'-'+str(i['data__day'])
                                #print(date)
                                #item['date']=i['data__date']#date
                                item['year']= i['data__year']
                                item['month']=i['data__month']
                                item['nomemese']=months[i['data__month']]
                                #item['date']=i['data__date']
                                item['total'] = i['total']
                                vi2 = MediaFile.objects.filter(data__year=i['data__year'],data__month=i['data__month'])
                                videos=[]
                                for i2 in vi2:
                                        video={'id':i2.id,'media': i2.media.name,'ora':i2.data.time(),
                                        'lat':i2.lat,'lon':i2.lon,'citta':i2.citta,'data':i2.data.date}
                                        videos.append(video)
                                #        print(i2.image.name,i2.data.time())
                                item['video']=videos
                        response.append(item)
                albums = Album.objects.all().order_by('-create')
                
                context={'items':response,'col':4,'albums':albums}



                return render(request,self.template_name, context)



class PrimaPagina(View):
    
    template_name = "home/primapagina.html"
    
 
    def get(self,request):
            # col setta il numero di foro per riga col=3 mette 4 colonne ( 3x4=12) col-2 ne mette 6 ( 2x6=12)
        #tmp = Immagine.objects.filter(album_id=49).order_by('-data')
        #im = Immagine.objects.filter(album_id=49).values('data__year','data__month','data__day').annotate(total=Count('id'))
        #im = tmp.values('data__year','data__month','data__day').annotate(total=Count('id'))#.order_by('-data')
        #im=Immagine.objects.filter(album_id=49).order_by('-data__date').values('data__year','data__month').annotate(total=Count('id'))
        a = Album.objects.get(pk=1)
        i2abb = a.albums.all()#.annotate(key=Trunc('image__data','day')) #.values('image__data__year','image__data__month','image__id').annotate(total=Count('id'))
        #i2abb = a.albums.all().order_by('-image__data__year','-image__data__month').values('image__data__year','image__data__month','image__id').annotate(total=Count('id'))
        #i2a = a.albums.all().order_by('-data__year','-data__month').values('data__year','data__month').annotate(total=Count('id'))
        t = i2abb.annotate(month=TruncMonth('image__data')).values('month').annotate(c=Count('id'))
        r=[]

        for s in t:
                if s['month']:
                #i = s.values('image__data__year','image__data__month').annotate(total=Count('id'))
                        item={}
                        item['year'] = s['month'].year
                        item['month'] = s['month'].month
                        item['day'] = s['month'].day
                        
                        dd = s['month'].strftime('%Y-%m-%d')
                        item['total'] = s['c']
                        months=['tt','Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre']
                        item['nomemese']=months[s['month'].month]
                
                #im=i2abb.filter(image__data__date=dd).order_by('-image__data')
                        im=i2abb.filter(image__data__year=s['month'].year,image__data__month=s['month'].month).order_by('image__data')
                        fotos=[]
                        for i in im:
                                ora = i.image.data.strftime("%H:%M:%S")
                                dd = i.image.data.strftime('%Y-%m-%d')
                                f={'id':i.image.id,
                                        'foto': i.image.image.name,
                                        'ora': ora,
                                        'lat':i.image.lat,
                                        'lon':i.image.lon,
                                        'citta':i.image.citta,
                                        'data': dd }
                                fotos.append(f)
                        item['fotos']=fotos
                        r.append(item)
                #response.append(item)
        #album = Album.objects.all().order_by('-create').first()
        
        context={'items':r,'col':3}



        return render(request,self.template_name, context)




class Index(View):
    
    template_name = "home/index.html"
    
 
    def get(self,request):
            """
            form = AlbumCreateForm()
            #widget=CustomTextInput()
            context = {
                    'form': form,
            }
            """
            #albums = getAlbumsList()
            
            #albums= Album.objects.order_by("nome").values('nome','id') #, flat=True)
            foto = Image2Album.objects.filter(album=31).order_by('image__data')
            #sortedfoto = foto.image.order_by('-data')
            thisalbum = Album.objects.get(pk=31)
            #albums = request.get('/rest/list')
            context={'foto':foto,'this':thisalbum}
            return render(request,self.template_name, context)


class UploadMediaFile(View):
    template_name = "home/uploadmediafile.html"
    
    def get(self,request):
        context={}
        return render(request,self.template_name, context)
    

class ShowFiles(View):
    
    template_name = "home/showfiles.html"
    
 
    def get(self,request):
            # col setta il numero di foro per riga col=3 mette 4 colonne ( 3x4=12) col-2 ne mette 6 ( 2x6=12)
        w = walk('/srv/media/Varie')

        files=[]
        for (dirpath, dirnames, filenames) in w:
            for file in filenames:
                #print(file)
                item = {'file':[],'date':[]}

                ftype = magic.from_file(os.path.join(dirpath,file), mime=True)
                #print(ftype)

                if 'image' in ftype:
                    item['file']=os.path.join('Varie',file)
                    
                    
                    met = MyExifTool(os.path.join(dirpath,file))
                    m = met.read_image_metadata()
                    #T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)
                    creationDate = m['createdate']
                    item['date']= creationDate
                    files.append(item)




            
            context={'files':files,'col':2}



            return render(request,self.template_name, context)
