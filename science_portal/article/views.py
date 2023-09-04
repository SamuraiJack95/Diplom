from django.shortcuts import render, redirect
from .models import Article, Tag
from django.core.paginator import EmptyPage


def start(request):
    return render(request, 'article/start.html')

def articles(request):
    art = Article.objects.all()

    context = {'article': art}
    return render(request, 'article/articles.html', context)
