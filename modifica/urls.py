from django.urls import path
from .views import SetExifTags,CheckMetadata
urlpatterns = [
    path(r'setexif/<int:img_id>',SetExifTags.as_view(),name='setexiftag'),
    path(r'checkMetadata/<int:img_id>',CheckMetadata.as_view(),name='checkmetadata'),
    
]