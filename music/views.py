from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Album, Song
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import UserForm
from django.http import JsonResponse
from django.db.models import Q


def index(request):
        if not request.user.is_authenticated:
            return render(request, 'music/login_form.html')
        else:
            albums= Album.objects.filter(user=request.user)
            num= Album.objects.filter(user=request.user).count()
            req= request.GET.get("q")
            if req:
                songs=Song.objects.filter(album=albums)
                albums= albums.filter(
                    Q(album_title__icontains=req) |
                    Q(artist__icontains=req)
                ).distinct()
                songs=songs.filter(
                    Q(song_title__icontains=req)
                ).distinct()
                context={
                'object_list': albums,
                'num': num,
                'songs': songs
                }
            else :
                context={
                'object_list': albums,
                'num': num
                }
            return render(request, 'music/index.html', context) #we are using onject_list here coz for learning classbasedgen views we did the rest accordingly



class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url= 'music:login'
    redirect_field_name= 'go_to'
    model= Album
    template_name= 'music/detail.html'

    def get_context_data(self, *args, **kwargs):
        temp_album= Album.objects.get(pk=self.kwargs['pk'])
        kwargs['song_list']= Song.objects.filter(album= temp_album)
        #kwargs['song_list']= Album.objects.select_related().filter(pk= self.kwargs['pk'])
        return super(DetailView, self).get_context_data(*args, **kwargs)




class SongCreate(LoginRequiredMixin, CreateView):

    login_url='music:login'
    redirect_field_name='go_to'
    model=Song
    fields=['song_title','audio_file']

    def get_context_data(self, *args, **kwargs):
        kwargs['album']= Album.objects.get(pk= self.kwargs['pk'])
        return super(SongCreate, self).get_context_data(*args, **kwargs)


    def form_valid(self, form):
        temp= form.save(commit=False)
        temp.album= Album.objects.get(pk= self.kwargs['pk'])
        temp.save()
        return super(SongCreate, self).form_valid(form)



class AlbumCreate(LoginRequiredMixin, CreateView):
    login_url= 'music:login'
    redirect_field_name='go_to'
    model=Album
    fields=['artist','album_title','genre','album_logo']

    def form_valid(self, form):
        temp= form.save(commit=False)
        temp.user= self.request.user
        temp.save()
        return super(AlbumCreate, self).form_valid(form)






class AlbumUpdate(LoginRequiredMixin, UpdateView):
    login_url= 'music:login'
    redirect_field_name='go_to'
    model=Album
    fields=['artist','album_title','genre','album_logo']

    def form_valid(self, form):
        temp=form.save(commit=False)
        temp.user= self.request.user
        temp.save()
        return super(AlbumUpdate, self).form_valid(form)


class AlbumDelete(LoginRequiredMixin, DeleteView):
    login_url= 'music:login'
    redirect_field_name= 'go_to'
    model=Album
    #success_url= reverse_lazy('music:index')
    def get_success_url(self):
        return reverse_lazy('music:index')

class UserFormView(View):
    form_class= UserForm
    template_name= 'music/registration_form.html'

    def get(self, request): #display blank form for registration
        form= self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form= self.form_class(request.POST)

        if form.is_valid():
            user= form.save(commit=False)

            username= form.cleaned_data['username']
            password= form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns user obj if login creds are correct
            user= authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form':form})


class LoginView(View):

    def get(self, request): #display blank form for logging in
        return render(request,'music/login_form.html')

    def post(self, request):

        username= request.POST.get('username')
        password= request.POST.get('password')

        #returns user obj if login creds are correct
        user= authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/music/')
        else:
            return render(request, 'music/login_form.html', {'error_message':'Not a valid username and pwd. Try Again or make sure that you are a registered user'}) 
        return render(request, 'music/login_form.html')


def logout_user(request):

    if not request.user.is_authenticated:
        return redirect('/music/login/')
    else :
        logout(request)
        return redirect('/music/login/')

def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/music_home.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
})

def favorite_song(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        song= Song.objects.get(pk=pk)
        idee= song.album.pk
        if song.is_favorite:
            song.is_favorite= False
        else:
            song.is_favorite= True
        song.save()
        return redirect('music:songs','favorites')