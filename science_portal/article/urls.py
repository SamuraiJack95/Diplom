from django.urls import path
from . import views



urlpatterns = [
    path('', views.start, name='start'),
    path('articles/', views.articles, name='articles'),
]
