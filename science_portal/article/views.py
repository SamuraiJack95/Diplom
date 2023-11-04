from django.shortcuts import render, redirect
from .models import Article, Tag, Category
from django.shortcuts import render, redirect
from .forms import ArticleForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Count

def start(request):
    return render(request, 'article/start.html')

def articles(request, cat_slug=0):
    categories = Category.objects.annotate(Count('article'))
    if cat_slug == 0:
        objects = Article.objects.all()
        return render(request, 'article/articles.html', context={'objects': objects, 'cats': categories, 'cat_selected': 0})
    else:
        category = Category.objects.get(slug=cat_slug)
        objects = Article.objects.filter(cat=category)
        return render(request, 'article/articles.html', context={'objects': objects, 'cats': categories, 'cat_selected': category.id})


def article(request, pk):
    form = ReviewForm()
    article_obj = Article.objects.get(id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.article = article_obj
        review.owner = request.user.profile
        review.save()
        article_obj.get_vote_count()

        messages.success(request, 'Your review was posted successfully!')
        return redirect('article', pk=article_obj.id)

    context = {'article': article_obj, 'form': form}
    return render(request, 'article/single-article.html', context)


@login_required(login_url='login')
def create_article(request):
    profile = request.user.profile
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            art = form.save(commit=False)
            art.owner = profile
            form.save()
            return redirect('user_account')
    context = {'form': form}
    return render(request, 'article/form-template.html', context)

@login_required(login_url='login')
def update_article(request, pk):
    profile = request.user.profile
    article = profile.article_set.get(id=pk)
    form = ArticleForm(instance=article)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('user_account')
    context = {'form': form, 'article': article}
    return render(request, 'article/form-template.html', context)

@login_required(login_url='login')
def delete_article(request, pk):
    profile = request.user.profile
    article = profile.article_set.get(id=pk)

    if request.method == 'POST':
        article.delete()
        return redirect('user_account')

    context = {'article': article}
    return render(request, 'article/delete.html', context)

