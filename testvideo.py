from common.MyExifTool import MyExifTool
from django.db.models.functions import TruncDay,TruncMonth
from django.db.models import Count
import sys
import argparse
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


#parser = argparse.ArgumentParser(description='Process to upload zip file and ingest CME events ')
#parser.add_argument('--directory','-d',  help='Directory to parse and upload files ', required=True)
#parser.add_argument('--album','-a',  help='Nome dell`album  ', required=True)

#args = parser.parse_args()
#print(args.directory)
#print(args.album)



a= Album.objects.get(pk=14)


m2a = a.mediaalbums.all().order_by('-media__data')

#m2a = a.mediaalbums.all()
tm = set(m2a.annotate(day=TruncDay('media__data')).values_list('day').annotate(c=Count('id')))
for oo in tm:
        print("OO",oo)
print("TM",tm)
response=[]
videototali = 0
for s in tm:
       # if s['day']:
        if s:
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
                print('ITEM',item)

        #im=i2abb.filter(image__data__date=dd).order_by('-image__data')
                #mf=m2a.filter(media__data__year=s['day'].year,media__data__month=s['day'].month,media__data__day=s['day'].day).order_by('media__data')
                mf=m2a.filter(media__data__year=s[0].year,media__data__month=s[0].month,media__data__day=s[0].day).order_by('media__data')
                print("MF",mf)
                #vi2 = MediaFile.objects.filter(data__year=i['data__year'],data__month=i['data__month'])
                videos=[]
                for i2 in mf:
                        print(i2)
                        video={'id':i2.id,'media': i2.media.media.name,'ora':i2.media.data.time(),
                        'lat':i2.media.lat,'lon':i2.media.lon,'citta':i2.media.citta,'data':i2.media.data.date}
                        videos.append(video)
                #        print(i2.image.name,i2.data.time())
                item['video']=videos
                item['total'] = len(videos)
                response.append(item)     
print("RESPONSE",response)   
for item in response:
        print(item['year'])
        print(item['month'])
        print(item['day'])
        #print("TOTAL",item['total'])
        for one in item['video']:
                print(one['id'])
                print(one['media'])
                print(one['ora'])
                print(one['data'])
        
