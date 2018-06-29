# -*- coding: utf-8 -*-

# NOTES : lines marked with (*) is a more clumbersome alternative to
# lines marked with (&)
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.http import HttpResponse
from django.http import Http404  # dont use this import if using get_object_or_404() function
# (*) from django.template import loader
from .models import Album, Song
from django.shortcuts import render  # (&)


class IndexView(generic.ListView):   # class-based generic index view
    template_name= 'music/index.html'
    #context_object_name= 'all_albums' this var is set when the default
    #object_list name has to be changed for list returned by

    def get_queryset(self):
        return Album.objects.all()

def detail(request, album_id):
    try:
        album= Album.objects.get(id=album_id) #try-except of the retreive from DB otherwise 404 can be done simply usign the below line
    except Album.DoesNotExist:
        raise Http404("Album doesnt exist")

    album= get_object_or_404(Album, id=album_id)  # this is alternative to try DB except 404

    return render(request, 'music/detail.html', {'album':album})


def favorite(request, album_id):
    album= get_object_or_404(Album, id=album_id)
    try:
        selected_song= album.song_set.get(id=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', {
            'album':album,
            'error_messege':"You did not select a valid song",
        })
    else:
        selected_song.is_favorite= True
        selected_song.save()
        return render(request, 'music/detail.html', {'album':album,})
