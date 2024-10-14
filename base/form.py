from django.forms import ModelForm,EmailField
from .models import Room, Message,User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['name','username',"email",'password1','password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']

class UserForm(UserCreationForm):
    email = EmailField()
    class Meta:
        model = User
        fields = ["name",'username','email','password1','password2']

class UserUpdateForm(ModelForm):
    email = EmailField()
    class Meta:
        model = User
        fields = ["avatar","name",'username','email',"bio"]


