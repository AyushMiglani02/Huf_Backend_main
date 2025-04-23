from django.urls import path 
from . import views

urlpatterns = [
    path('', views.PathyView.as_view(), name="pathy"),
]