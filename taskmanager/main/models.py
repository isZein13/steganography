from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
# Create your models here.

User = get_user_model()

class Task(models.Model):
    title = models.CharField('Name:', max_length=50)
    task = models.TextField('Description:')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasking'


class Photo(models.Model):
    image = models.ImageField(upload_to='images')
    result = models.TextField('Result is:', null=True, blank=True, default='Didn\'t discovered!')
    
    def __str__(self):
        return self.result

    class Meta:
            verbose_name = 'UserPic'
            verbose_name_plural = 'Picture'

    user = models.ForeignKey(User, verbose_name='UserPic',on_delete=models.CASCADE)