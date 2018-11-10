from django.conf.urls import url

from music import views
app_name= 'music'  # required for namespace
urlpatterns= [
    #/music/
    url(r'^$', views.index, name='index'),

    #/music/register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /music/71/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    #/music/album/add/
    url(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),

    #/music/album/2/
    url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(), name='album-update'),

    #/music/album/2/delete/
    url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(), name='album-delete'),

    #/music/login/
    url(r'^login/$',views.LoginView.as_view(), name='login'),

    #/music/logout/
    url(r'^logout/$',views.logout_user,name='logout'),

    #/music/songs/all/
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),

    #/music/71/add/
    url(r'^(?P<pk>[0-9]+)/add/$', views.SongCreate.as_view(), name='song-add'),

    #/music/song/22/favorite    or     #/music/song/22/favourite
    url(r'^song/(?P<pk>[0-9]+)/favorite/$', views.favorite_song, name='fav_song'),
    url(r'^song/(?P<pk>[0-9]+)/favourite/$', views.favorite_song, name='fav_song'),

    
]