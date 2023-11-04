# Generated by Django 4.2.4 on 2023-11-02 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='О тебе'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=500, null=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profiles/user-default.png', null=True, upload_to='profiles/', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='short_info',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Классификация'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Имя пользователя'),
        ),
    ]