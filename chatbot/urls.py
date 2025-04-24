# chatbot/urls.py
from django.urls import path
from .views import question_detail

urlpatterns = [
    path('question/<int:pk>', question_detail, name='question-detail'),
]
