from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view()),  # This should be correct
]
