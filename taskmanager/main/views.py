import os
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponseBadRequest
from PIL import Image
from .models import Task, Photo
from .forms import TaskForm, ImageForm
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import iop_encrypt, iop_decrypt
from django.core.files.storage import FileSystemStorage


def home(request):
    return HttpResponse('<h1>Home</h1>')

def index(request):
    tasks = Task.objects.all()
    return render(request ,'main/index.html', {'title':'main tasks','tasks':tasks})


def about(request):
    return render(request ,'main/about.html')


def profile(request):
    return render(request ,'main/user/profile.html')

def test(request):
    return render(request ,'main/user/test.html')

def iope(request):
    if request.user.is_active:
        try:
            photo = Photo.objects.filter(user_id = request.user.id)[0]
        except IndexError:
            photo = None

        if photo is not None:
            return render(request ,'main/user/iope.html', context={'photo': photo})

    return render(request ,'main/user/iope.html')

def iopd(request):
    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request ,'main/user/iopd.html', context={'photo_url': uploaded_file_url, 'result': iop_decrypt(fs.path(filename))})
    return render(request ,'main/user/iopd.html')

def create(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
             form.save()
             redirect('home')
        else:
            error = 'Form has not correct!'
    form = TaskForm()
    context = {
        'form' : form,
        'error' : error
    }
    return render(request ,'main/create.html', context)


def signUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='User')
            user_group.user_set.add(signup_user)
        return render(request, 'main/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request,'main/signup.html', {'form': form})

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return redirect('signup')


    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form':form})


def signoutView(request):
    logout(request)
    return redirect('login')

    
def image_upload_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, user = request.user)
        if request.user.is_active:
            
            if form.is_valid():
                user_text = form.cleaned_data.get('user_text')
                uploaded_image = form.cleaned_data.get('image')
                if uploaded_image:
                    image_extension = os.path.splitext(uploaded_image.name)[-1].lower()
                    if image_extension != '.png':
                        return HttpResponseBadRequest("Invalid image format. Please upload a PNG image.")
                form.save()
                # if width > 900 or height > 900:
                #     form.add_error('image', error='Error! Bad Image resolution. Must be less than 900x900.')
                #     return render(request, 'main/user/test.html', {'form': form})
                try:
                    photo = Photo.objects.filter(user_id = request.user.id)[0]
                except IndexError:
                    photo = None
                if photo is not None:
                    iop_encrypt(form.instance, user_text)
                    

            try:
                photo = Photo.objects.filter(user_id = request.user.id)[0]
            except IndexError:
                return render(request, 'main/user/test.html', {'form': form})

            return render(request, 'main/user/test.html', {'form': form, 'photo': photo})
        return render(request, 'main/user/test.html', {'form': form})
    else:
        form = ImageForm(request.POST, request.FILES, user = request.user)
        if request.user.is_active:
            if form.is_valid():
                photos = Photo.objects.filter(user_id=request.user.id)
                if len(photos) > 0:
                    photo = Photo.objects.filter(user_id=request.user.id)[0]
                    return render(request, 'main/user/test.html', {'form': form, 'photo': photo})
            return render(request, 'main/user/test.html', {'form': form})
        return render(request, 'main/user/test.html', {'form': form})

def deleteImage(request):
    
    if request.user.is_active:
        photo = Photo.objects.filter(user = request.user)
        print(request.user)
        photo.delete()
        

    return HttpResponseRedirect('upload')