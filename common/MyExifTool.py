from exiftool import ExifToolHelper
import os
class MyExifTool():

    jsonret={}
    md={}
    MIMEType = ''
    def __init__(self,mediafile):
        with ExifToolHelper() as et:
            self.md = et.get_metadata(mediafile)
            if self.md:
                 self.exif = True
                 self.jsonret['exif'] = True
            self.MIMEType = self.md[0]['File:MIMEType']

    def read_video_metadata(self):
        # .mp4 video files
        #jsonret={}
        #with ExifToolHelper() as et:
            for d in self.md: #et.get_metadata(mediafile):
                #print(d)
                try:
                    self.jsonret['duration']  = d['QuickTime:Duration']
                except:
                    self.jsonret['duration'] = None
                try:
                    self.jsonret['latitude']  = d['Composite:GPSLatitude']
                except:
                    self.jsonret['latitude']  = None
                try:
                    self.jsonret['longitude'] = d['Composite:GPSLongitude']
                except:
                    self.jsonret['longitude'] = None

                try:
                     self.jsonret['altitude']  = d['Composite:GPSAltitude']
                except:
                     self.jsonret['altitude']  = None
                try:
                    self.jsonret['rotation']  = d['Composite:Rotation']
                except:
                     self.jsonret['rotation']  = None
                try:
                    self.jsonret['createdate']= d['QuickTime:CreationDate'].replace(":","-",2)
                except: 
                    self.jsonret['createdate']= None 
                try:
                    self.jsonret['createdate']= d['QuickTime:CreateDate'].replace(":","-",2)
                except: 
                    self.jsonret['createdate']= None 
         
                try:
                    self.jsonret['width']     = d['QuickTime:ImageWidth']
                except:
                     self.jsonret['width']  = None
                try:
                    self.jsonret['height']    = d['QuickTime:ImageHeight']
                except:
                     self.jsonret['height']    =None
                try:
                    self.jsonret['mimetype']  = d['File:MIMEType']
                except:
                     self.jsonret['mimetype']  =None
                #for k, v in d.items():
                #    print(f"Dict: {k} = {v}")

            return  self.jsonret
    def read_image_metadata(self):
        # .jpg video files
        #jsonret={}
        #with ExifToolHelper() as et:
            #print(et.get_metadata(imagefile))
            for d in self.md : #et.get_metadata(imagefile):
                #jsonret['duration']  = d['QuickTime:Duration']
                if 'Composite:GPSLatitude' in d:
                     self.jsonret['latitude']  = d['Composite:GPSLatitude']
                else:
                     self.jsonret['latitude']  = None
                if 'Composite:GPSLongitude' in d:
                     self.jsonret['longitude'] = d['Composite:GPSLongitude']
                else:
                     self.jsonret['longitude'] = None
                if 'Composite:GPSAltitude' in d:
                     self.jsonret['altitude']  = d['Composite:GPSAltitude']
                else:
                     self.jsonret['altitude']  = None

                if 'EXIF:DateTimeOriginal' in d:
                     self.jsonret['datetime_original']= d['EXIF:DateTimeOriginal'].replace(":","-",2)
                else:
                     self.jsonret['datetime_original']= None

                if 'EXIF:CreateDate' in d:
                    self.jsonret['createdate']= d['EXIF:CreateDate'].replace(":","-",2)
                else:
                     self.jsonret['createdate']= None
                if 'EXIF:ExifImageWidth' in d:
                    self.jsonret['width']     = d['EXIF:ExifImageWidth']
                else:
                     self.jsonret['width']  = None
                if 'EXIF:ExifImageHeight' in d:
                    self.jsonret['height']    = d['EXIF:ExifImageHeight']
                else:
                     self.jsonret['height']    =None
                if 'File:MIMEType' in d:
                    self.jsonret['mimetype']  = d['File:MIMEType']
                else:
                     self.jsonret['mimetype']  =None
                #jsonret['rotation']  = d['Composite:Rotation']
                #jsonret['createdate']= d['QuickTime:CreateDate'].replace(":","-",2)

                #for k, v in d.items():
                #    print(f"Dict: {k} = {v}")

            return  self.jsonret
