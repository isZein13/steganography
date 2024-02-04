from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('create', views.create, name='create'),
    path('account/create', views.signUpView, name='signup'),
    path('account/login', views.loginView, name='login'),
    path('account/logout', views.signoutView, name='logout'),
    path('account/profile', views.profile, name='profile'),
    path('account/test', views.test, name='test'),
    path('account/iopE', views.iope, name='iope'),
    path('account/iopD', views.iopd, name='iopd'),
    path('account/test/upload', views.image_upload_view, name='test-picture'),
    path('account/test/delete', views.deleteImage, name='delete-picture'),

]
