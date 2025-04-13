from django.urls import path
from albums.views import ShowAlbum,CreateAlbum,ModifyImage,Modal_ModifyImage,UploadFoto
urlpatterns = [
    path(r'show/<int:album_id>',ShowAlbum.as_view(),name='showalbum'),
    path(r'show/<int:album_id>/<slug:uitype>',ShowAlbum.as_view(),name='showalbum'),
    path(r'show',ShowAlbum.as_view(),name='showlastalbum'),
    path(r'show_modal_modify/<int:img_id>',Modal_ModifyImage.as_view(),name='showmodalmodify'),
    path(r'create',CreateAlbum.as_view(),name='createalbum'),
    path(r'upload',UploadFoto.as_view(),name='uploadfoto'),
    path(r'modify/<int:img_id>',ModifyImage.as_view(),name='modifyimage'),
]