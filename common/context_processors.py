from home.models import Album

def albums_context(request):
        #if '/access/login' in request.path or '/admin/login' in request.path  :
        #    return ""
        #else:
    #if request.user: #.is_authenticated():
        albums= Album.objects.order_by("-dataviaggio").values('nome','id','multianno','multefoto').exclude(nome='Varie') #, flat=True)
        for album in albums:
                if album['multefoto']:
                        album['multefoto'] = "/mf"
                else:
                        album['multefoto'] = ""
                if album['multianno']:
                        album['multianno'] = "/ma"
                else:
                        album['multianno'] = ""
        return {'albums': albums }
     


                