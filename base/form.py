from django.forms import ModelForm,EmailField
from .models import Room, Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']

class UserForm(UserCreationForm):
    email = EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

