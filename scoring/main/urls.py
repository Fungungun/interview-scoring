from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('final', views.final),
    path('fetchscore', views.fetchScore),
    path('saveForm', views.saveForm),
]

