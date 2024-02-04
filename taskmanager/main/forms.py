from .models import Task, Photo
from django.forms import ModelForm, TextInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='eg. yourmail@gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2', 'email',)


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title","task"]
        widgets = {
        "title": TextInput(attrs=
         {'class':'form-control',
         'placeholder': 'Write the Name of task',
             }),
            "task": TextInput(attrs=
            {'class': 'form-control',
             'placeholder': 'Write the task',
              })
        }


class ImageForm(forms.ModelForm):
    user_text = forms.CharField(max_length=255, required=True, label='Введите ваше сообщение:', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Photo
        fields = ('image', 'user_text')  # Include the 'user_text' field

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'user'):
            self.user = kwargs.pop('user')
        super(ImageForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        image = super(ImageForm, self).save(commit=False)
        image.user = self.user
        
        # Additional field handling
        user_text = self.cleaned_data.get('user_text')
        image.user_text = user_text

        if commit:
            image.save()
        return image