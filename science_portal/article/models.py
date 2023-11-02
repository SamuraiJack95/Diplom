from django.db import models
from users.models import Profile
from django.urls import reverse

class Article(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь')
    slug = models.SlugField(max_length=200, unique=True, default=0, verbose_name='Ссылка')
    title = models.CharField(max_length=200, verbose_name='Название')
    authors = models.CharField(max_length=500, blank=True, verbose_name='Автор')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    featured_image = models.ImageField(null=True, blank=True, upload_to="article/%Y/%m/%d", verbose_name='Изображение')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='Тэг')
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=True, blank=True, upload_to='article_f/%Y/%m/%d', verbose_name='Файл публикации')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('articles', kwargs={'articles_slug': self.slug})
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total']

    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()
        ratio = int((up_votes / total_votes) * 100)
        self.vote_total = total_votes
        self.vote_ratio = ratio

        self.save()

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner', 'article'], ]


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
