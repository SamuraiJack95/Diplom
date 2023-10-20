from django.shortcuts import render, redirect
from .models import Article, Tag, Category
from django.shortcuts import render, redirect
from .forms import ArticleForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.views.generic import ListView

def start(request):
    return render(request, 'article/start.html')

def articles(request, cat_slug=0):
    if cat_slug == 0:
        objects = Article.objects.all()
        return render(request, 'article/articles.html', context={'objects': objects})
    else:
        category = Category.objects.get(cat_slug=cat_slug)
        objects = Article.objects.filter(cat=category)
        return render(request, 'article/articles.html', context={'objects': objects})

# def articles(request, cat):
#     cat_selected = 0
#     cat_selected = Category.objects.get(id=cat)
#     ?
#     ?
#     if cat_selected == 0:
#         art = Article.objects.all()
#     else:
#         art = Category.get_queryset()?
#     ?
#     context = {'articles': art, 'cat_selected': cat_selected}
#     return render(request, 'article/articles.html', context)

# def projects(request):
#     pr = Project.objects.all()
#     page = request.GET.get('page')
#     results = 3
#     paginator = Paginator(pr, results)
#
#     # custom_range = range(1, 20)
#
#     try:
#         pr = paginator.page(page)
#     except PageNotAnInteger:
#         page = 1
#         pr = paginator.page(page)
#     except EmptyPage:
#         page = paginator.num_pages
#         pr = paginator.page(page)
#
#     left_index = int(page) - 4
#
#     if left_index < 1:
#         left_index = 1
#
#     right_index = int(page) + 5
#
#     if right_index > paginator.num_pages:
#         right_index = paginator.num_pages + 1
#
#     custom_range = range(left_index, right_index)
#
#     context = {'projects': pr, 'paginator': paginator, 'custom_range': custom_range}
#     return render(request, 'projects/projects.html', context)

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

# class BlogCategory(ListView):
#     model = Blog
#     template_name = 'blog/index.html'
#     context_object_name = 'posts'
#     allow_empty = False
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Категория - ' + str(context['posts'][0].cat)
#         context['menu'] = menu
#         context['cat_selected'] = context['posts'][0].cat_id
#         return context
#
#     def get_queryset(self):
#         return Blog.objects.filter(cat__slug=self.kwargs['cat_slug'],
#                                    is_published=True).select_related('cat')
#
# Куда это все вставть чтобы все это заработало !!!
#
# def get_queryset(self):
#     return Blog.objects.filter(is_published= True).select_related('cat')

#     def get_queryset(self):
#         return Blog.objects.filter(cat__slug=self.kwargs['cat_slug'],
#                                    is_published=True).select_related('cat')