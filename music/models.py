# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Album(models.Model):
    user= models.ForeignKey(User, default=1)
    artist= models.CharField(max_length=100)
    album_title= models.CharField(max_length=200)
    genre= models.CharField(max_length=50)
    album_logo= models.FileField()
    album_favorite= models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse('music:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.album_title+' by '+ self.artist

class Song(models.Model):
    album= models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title= models.CharField(max_length=200)
    audio_file= models.FileField(default='')
    is_favorite= models.BooleanField(default=False)
    def __str__(self):
        return self.song_title

    def get_absolute_url(self):
        alb= self.album
        return reverse('music:detail',kwargs={'pk':alb.pk})
