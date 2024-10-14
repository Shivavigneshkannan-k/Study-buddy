from . import views
from django.urls import path

urlpatterns = [
    path("",views.getRoutes),
    path("rooms",views.getRooms),

]
