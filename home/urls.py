from django.urls import path
from .views import Index,PrimaPagina,UploadMediaFile,Video,ShowFiles,DownloadImage
urlpatterns = [
    path(r'',PrimaPagina.as_view(),name='primapagina'),
    path(r'video',Video.as_view(),name='video'),
    #path(r'media',Media.as_view(),name='media'),
    path(r'uploadmedia',UploadMediaFile.as_view(),name='uploadfoto'),
    path(r'showfiles',ShowFiles.as_view(),name='showfiles'),
    path(r'download/<int:img_id>',DownloadImage.as_view(),name='download'),

    
]