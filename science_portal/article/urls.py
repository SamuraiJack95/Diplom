from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('articles/', views.articles, name='articles'),
    path('articles/<str:pk>', views.article, name='article'),
    # path('category/<slug:cat_slug>/', BlogCategory.as_view(), name='category'),
    path('create-article', views.create_article, name='create-article'),
    path('update-article/<str:pk>', views.update_article, name='update-article'),
    path('delete-article/<str:pk>', views.delete_article, name='delete-article'),
    path('category/<slug:cat_slug>/', views.articles, name='category'),
]
