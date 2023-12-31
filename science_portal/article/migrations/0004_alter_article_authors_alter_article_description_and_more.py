# Generated by Django 4.2.4 on 2023-11-02 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('article', '0003_alter_article_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='authors',
            field=models.CharField(blank=True, max_length=500, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='article',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, upload_to='article/%Y/%m/%d', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='article',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='article_f/%Y/%m/%d', verbose_name='Файл публикации'),
        ),
        migrations.AlterField(
            model_name='article',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(default=0, max_length=200, unique=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='article.tag', verbose_name='Тэг'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]
