from django.urls import path 
from . import views

urlpatterns = [
    path('', views.get_members, name="members"),
    path('<str:team>', views.get_members_detail, name="members-detail"),
]