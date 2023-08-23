from django.shortcuts import render, redirect
from .models import Article, Tag
from django.core.paginator import EmptyPage


def article(request):
    art = Article.objects.all()

    context = {'article': art}
    return render(request, 'article/index.html', context)
