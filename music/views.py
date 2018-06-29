from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Album
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm


def index(request):
        if not request.user.is_authenticated():
            return render(request, 'music/login_form.html')
        else:
            albums= Album.objects.filter(user=request.user)
            num= Album.objects.filter(user=request.user).count()
            context={
            'object_list': albums,
            'num': num
            }
            return render(request, 'music/index.html', context) #we are using onject_list here coz for learning classbasedgen views we did the rest accordingly


class DetailView(generic.DetailView):
    model= Album
    template_name= 'music/detail.html'


class AlbumCreate(CreateView):
    model=Album
    fields=['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
    model=Album
    fields=['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
    model=Album
    #success_url= reverse_lazy('music:index')
    def get_success_url(self):
        return reverse('music:index')

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

        return render(request, 'music/login_form.html')


def logout_user(request):

    if not request.user.is_authenticated():
        return redirect('/music/login/')
    else :
        logout(request)
        return redirect('/music/login/')
