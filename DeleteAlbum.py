from common.MyExifTool import MyExifTool
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


parser = argparse.ArgumentParser(description='Process to upload zip file and ingest CME events ')
parser.add_argument('--album','-a',  help='ID dell`album  ', required=True)

args = parser.parse_args()
print(args.album)



print("ALBUM",args.album)
try:
    A = Album.objects.get(pk=args.album)
except Album.DoesNotExist:
    #Do Something
    exit()

im2al = A.albums.all()
me2al = A.mediaalbums.all()
for one in me2al:
    print(one.id,one.media.id,one.album.id)
    media_id= one.media.id
    one.delete()
    MediaFile.objects.get(pk=media_id).delete()

for one in im2al:
    #print(one.id,one.media.id,one.album.id)
    image_id= one.image.id
    one.delete()
    Immagine.objects.get(pk=image_id).delete()

#print(me2al)
#print(im2al)
