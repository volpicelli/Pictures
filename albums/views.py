from django.shortcuts import render
from django.db.models.functions import TruncDay,TruncMonth
from django.db.models import Count
from django.views  import View
from home.models import Image2Album, Album,Media2Album,Immagine,MediaFile
# Create your views here.
class ModifyImage(View):
     template_name="albums/modify.html"
     def get(self,request,img_id):
          context={}
          img = Immagine.objects.get(pk=img_id)
          context={'image':img}
          return render(request,self.template_name, context)
     
class Modal_ModifyImage(View):
     template_name="includes/albums/modal/modal_modify_image.html"
     def get(self,request,img_id):
          context={}
          img = Image2Album.objects.get(pk=img_id)
          context={'image':img.image}
          return render(request,self.template_name, context)


class ShowAlbum(View):
    
    template_name = "albums/show.html"
    
 
    def get(self,request,uitype=None,album_id=None):
            # col setta il numero di foro per riga col=3 mette 4 colonne ( 3x4=12) col-2 ne mette 6 ( 2x6=12)
            
            album = Album.objects.get(pk=album_id)
            foto = Image2Album.objects.filter(album=album.id).order_by('image__data')
            video = Media2Album.objects.filter(album=album_id).order_by('media__data')
            thisalbum = Album.objects.get(pk=album.id)
            context={'foto':foto,'this':thisalbum,'video':video,'col':3}
            
            if uitype is not None:      

                self.template_name = "albums/showmf.html"
                """     
                if album_id :
                    album = Album.objects.get(pk=album_id)
                    foto = Image2Album.objects.filter(album=album.id).order_by('image__data')
                    video = Media2Album.objects.filter(album=album_id).order_by('media__data')
                    thisalbum = Album.objects.get(pk=album.id)
                    context={'foto':foto,'this':thisalbum,'video':video,'col':3}
                else:
                    #album = Album.objects.all().order_by('-create').first()
                    album_id=49
                    foto = Image2Album.objects.filter(album=album_id).order_by('-image__data')
                    thisalbum = Album.objects.get(pk=album_id)
                    context={'foto':foto,'this':thisalbum,'col':2}
                """ 
                a = Album.objects.get(pk=album_id)
                i2abb = a.albums.all()#
                t = i2abb.annotate(day=TruncDay('image__data')).values('day').annotate(c=Count('id'))
                #t = i2abb.annotate(month=TruncMonth('image__data')).values('month').annotate(c=Count('id'))
                r=[]
                fotototali = 0
                for s in t:
                        if s['day']:
                                item={}
                                item['year'] = s['day'].year
                                item['month'] = s['day'].month
                                item['day'] = s['day'].day

                                dd = s['day'].strftime('%Y-%m-%d')
                                item['total'] = s['c']
                                months=['tt','Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre']
                                item['nomemese']=months[s['day'].month]

                        #im=i2abb.filter(image__data__date=dd).order_by('-image__data')
                                im=i2abb.filter(image__data__year=s['day'].year,image__data__month=s['day'].month,image__data__day=s['day'].day).order_by('image__data')
                                fotos=[]
                                for i in im:
                                        fotototali+=1
                                        ora = i.image.data.strftime("%H:%M:%S")
                                        dd = i.image.data.strftime('%Y-%m-%d')
                                        f={'id':i.image.id,
                                                'foto': i.image.image.name,
                                                'ora': ora,
                                                'lat':i.image.lat,
                                                'lon':i.image.lon,
                                                'citta':i.image.citta,
                                                'display': i.image.display_name,
                                                'data': dd }
                                        fotos.append(f)
                                item['fotos']=fotos
                                r.append(item)
                        #response.append(item)
                #album = Album.objects.all().order_by('-create').first()
                
                # VIDEO
                vi=MediaFile.objects.all().order_by('-data__year','-data__month').values('data__year','data__month').annotate(total=Count('id'))
                m2a = a.mediaalbums.all().order_by('-media__data')
                # Uso set perche' SQLite3 non supporta DISTINCT nella select , usando set i record con la stessa data non vengono duplicati
                tm = set(m2a.annotate(day=TruncDay('media__data')).values_list('day')) #.annotate(c=Count('media__data')))
                #for oo in tm:
                #        print("OO",oo)
                #print("TM",tm)
                response=[]
                videototali = 0
                for s in tm:
                # if s['day']:
                        if s[0]:
                                item={}
                                #item['year'] = s['day'].year
                                #item['month'] = s['day'].month
                                #item['day'] = s['day'].day

                                #dd = s['day'].strftime('%Y-%m-%d')
                                
                                item['year'] = s[0].year
                                item['month'] = s[0].month
                                item['day'] = s[0].day

                                dd = s[0].strftime('%Y-%m-%d')

                                #item['total'] = s['c']
                                months=['tt','Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre']
                                #item['nomemese']=months[s['day'].month]
                                item['nomemese']=months[s[0].month]
                                #print('ITEM',item)

                        #im=i2abb.filter(image__data__date=dd).order_by('-image__data')
                                #mf=m2a.filter(media__data__year=s['day'].year,media__data__month=s['day'].month,media__data__day=s['day'].day).order_by('media__data')
                                mf=m2a.filter(media__data__year=s[0].year,media__data__month=s[0].month,media__data__day=s[0].day).order_by('media__data')
                                #print("MF",mf)
                                #vi2 = MediaFile.objects.filter(data__year=i['data__year'],data__month=i['data__month'])
                                videos=[]
                                for i2 in mf:
                                        #print(i2)
                                        video={'id':i2.id,'media': i2.media.media.name,'ora':i2.media.data.time(),
                                        'lat':i2.media.lat,'lon':i2.media.lon,'citta':i2.media.citta,'data':i2.media.data.date}
                                        videos.append(video)
                                        videototali+=1
                                #        print(i2.image.name,i2.data.time())
                                item['video']=videos
                                item['total'] = len(videos)
                                response.append(item)                        
                               
                """
                                videos=[]
                                for i in mf:
                                        videototali+=1
                                        ora = i.media.data.strftime("%H:%M:%S")
                                        dd = i.media.data.strftime('%Y-%m-%d')
                                        f={'id':i.media.id,
                                                'foto': i.image.image.name,
                                                'ora': ora,
                                                'lat':i.image.lat,
                                                'lon':i.image.lon,
                                                'citta':i.image.citta,
                                                'display': i.image.display_name,
                                                'data': dd }
                                        fotos.append(f)
                                item['fotos']=fotos
                                r.append(item)
                """



                """
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
                """
                #context={'itemsvideo':response,'col':4,'albums':albums}
                # END VIDEO

                context={'itemsfoto':r,'col':3,'this':thisalbum,'fotototali':fotototali,'videototali':videototali,'itemsvideo':response}

            return render(request,self.template_name, context)

class CreateAlbum(View):
    template_name = "albums/create.html"
    
    def get(self,request):
        context={}
        return render(request,self.template_name, context)


class UploadFoto(View):
    template_name = "albums/upload.html"
    
    def get(self,request):
        context={}
        return render(request,self.template_name, context)


