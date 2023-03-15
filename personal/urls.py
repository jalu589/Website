from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("aboutmail", views.aboutmail, name="aboutmail"),
    path("aboutauction", views.aboutauction, name="aboutauction"),
    path("aboutnetwork", views.aboutnetwork, name="aboutnetwork"),
]