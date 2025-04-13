from django.shortcuts import render
from django.views  import View
from home.models import Image2Album,Immagine
from exif import Image
import os
from common.MyExifTool import MyExifTool
# Create your views here.

class SetExifTags(View):
    template_name="modifica/modify.html"
    def get(self,request,img_id):
          context={}
          img = Immagine.objects.get(pk=img_id)
          context={'image':img}
          return render(request,self.template_name, context)
     
class CheckMetadata(View):
    template_name="modifica/checkMetadata.html"
     
    def get(self,request,img_id):
          img = Immagine.objects.get(pk=img_id)
          path=os.path.join('/srv/media',img.image.name)
          met = MyExifTool(path)
          exiftool = met.read_image_metadata()
          with open(path, 'rb') as image_file:
            my_image = Image(image_file)
            my_image.has_exif
            tags = my_image.list_all()
            mytags = ['image_width','image_height',
                      'datetime_original','gps_longitude_ref',
                      'gps_longitude','gps_latitude_ref','gps_latitude',
                      'gps_altitude','gps_altitude_ref']
            mytagsval = []
            for tag in mytags:
              tmp={}
              tmp[tag] = my_image.get(tag)
              mytagsval.append(tmp)

            #dd = my_image.datetime
            #dt = my_image.get('datetime_original')
            #color = my_image.get("color_space")
            #tmp['DateTimeOriginal']=my_image.DateTimeOriginal
            #tmp['gps_longitude']=my_image.gps_longitude
            #tmp['gps_latitude']=my_image.gps_latitude
            context={'image':img,'tags':mytagsval,'exiftool': exiftool}#,'dd':dd,'dt':dt,'color':color}
          return render(request,self.template_name, context)
          