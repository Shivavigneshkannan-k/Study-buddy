from django.shortcuts import render,redirect

# Create your views here.

from django.http import HttpResponse
from .models import Room,Topic,Message
from .form import RoomForm
from django.forms import ModelForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {"id":1,"name":"Learn Django in a week"},
#     {"id":2,"name":"Learn React in a 30days"},
#     {"id":3,"name":"Python bootcamp"},
# ]
    


def home(request):
    q = request.GET.get('q')  if request.GET.get('q') !=None else ""
    rooms = Room.objects.filter(Q(topic__name__icontains=q)|Q(name__icontains=q)|Q(description__icontains=q))
    messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    topic = Topic.objects.all()
    context = {"rooms":rooms,"topics":topic,"messageActivity":messages}
    return render(request,"base/Home.html",context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()
    if request.method == "POST":
        Message.objects.create(
            user = request.user,
            body = request.POST.get("new_message"),
            room = room
        )
        room.participants.add(request.user)
        return redirect("room",pk=room.id)
    context = {"room":room,"room_messages":room_messages,"participants":participants}
    return render(request,"base/Room.html",context)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            print(form)
            form = form.save(commit=False)
            form.host = request.user
            form.save()
            return redirect("home")
    return render(request,"base/room_form.html",{"form":form})

@login_required(login_url="login")
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("you are not allowed here")
    
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request,"base/room_form.html",{"form":form})

@login_required(login_url="login")
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if room.host != request.user:
        return HttpResponse("you are not allowed here")
    if request.method=="POST":
        room.delete()
        return redirect("home")
    return render(request,"base/delete.html",{"obj":room})

@login_required(login_url="login")  
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if message.user != request.user:
        return HttpResponse("you are not allowed here")
    if request.method=="POST":
        message.delete()
        return redirect("home")
    return render(request,"base/delete.html",{"obj":message})
    
def loginPage(request):
    if request.method == "POST":
        Username = request.POST.get("username")
        Password = request.POST.get("password")
        try:
            user = User.objects.get(username=Username)
        except:
            messages.error(request, "user does not exist")
        user = authenticate(request,username=Username,password=Password)

        if user is not None:
                login(request,user)
                return redirect("home")
        else:
            messages.error(request,"username or password is wrong")

    context={}
    return render(request,"base/login.html",context)

def logoutFeature(request):
    logout(request)
    return redirect("home")

def registerUser(request):
    userForm = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST);
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower() 
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Error: invalid data")
    context = {"userForm":userForm}
    return render(request,"base/register.html",context)

def UserProfile(request,pk):
    q = request.GET.get('q') if request.GET.get('q') !=None else ""
    user = User.objects.get(id=pk) 
    room = user.room_set.all()
    topics = Topic.objects.all()
    messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {"user":user,"rooms":room,"messageActivity":messages,"topics":topics}
    return render(request,"base/user-profile.html",context)