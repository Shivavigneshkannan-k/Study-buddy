from django.urls import path
from . import views

urlpatterns =[
    path("",views.home,name="home"),
    path("room/<str:pk>/",views.room,name="room"),
    path("create-room/",views.createRoom,name="create-room"),
    path("update-room/<str:pk>/",views.updateRoom,name="update-room"),
    path("delete-room/<str:pk>/",views.deleteRoom,name="delete-room"),
    path("login/",views.loginPage,name="login"),
    path("loginout/",views.logoutFeature,name="logout"),
    path("registerUser/",views.registerUser,name="registerUser"),
    path("delete-message/<str:pk>/",views.deleteMessage,name="delete-message"),
    path("user-profile/<str:pk>/",views.UserProfile,name="user-profile"),
]

