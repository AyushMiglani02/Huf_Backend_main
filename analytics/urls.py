from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_disease_data, name="all-disease-data"),
    path("<str:disease>", views.get_disease_data, name="disease-data"),
]
