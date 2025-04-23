from django.urls import path
from . import views

urlpatterns = [
    path("", views.FooterView.as_view()),
]
