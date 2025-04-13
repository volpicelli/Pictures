from django.urls import path
from .views import PopulateModalCarousel,CreaAlbum,UploadImages2Album,SetCoordinates,\
        DeleteImage,UploadMediaFile,GetLocation,Test,CallApi,DeleteMultipleFoto,RegistraData,\
        RileggiDataSelezionate
        

urlpatterns = [ 
        
        #path(r'populatemodalcarousel/<int:album_id>/<int:img_id>', PopulateModalCarousel.as_view()),
        path(r'upload/<int:album_id>', UploadImages2Album.as_view()),
        path(r'upload', UploadImages2Album.as_view()),
        path(r'mediaupload', UploadMediaFile.as_view()),
        path(r'mediaupload/<int:album_id>', UploadMediaFile.as_view()),
        
        path(r'delete/<int:img_id>', DeleteImage.as_view()),
        #path(r'getlocation/<int:img_id>', GetLocation.as_view()),
        path(r'create', CreaAlbum.as_view()),
        path(r'addcoords/<int:image_id>', SetCoordinates.as_view()),
        
         #path(r'deletemulti', DeleteMultipleFoto.as_view()),
         path(r'callapi', CallApi.as_view()),
         #path(r'test', Test.as_view()),
         path(r'registraData', RegistraData.as_view()),
         path(r'rileggidataimgs', RileggiDataSelezionate.as_view()),
       
        
]
#urlpatterns = format_suffix_patterns(urlpatterns)
