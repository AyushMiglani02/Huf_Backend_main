from django.urls import path 
from . import views

urlpatterns = [
    path('', views.EjournalView.as_view(), name="ejournal"),
    path('get-all', views.GetAllEjournal.as_view(), name='all-ejournal'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('unsubscribe', views.unsubscribe, name='unsubscribe')
]