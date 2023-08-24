from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField


# Модель пользовательских объявлений
class Bulletin(models.Model):
    bul_author = models.ForeignKey(User, on_delete=models.CASCADE)
    bul_title = models.CharField(max_length=255)
    bul_short_description = models.CharField(max_length=100, default='...')
    bul_text = RichTextUploadingField()
    
    create_time = models.DateTimeField(auto_now_add=True)
    categories = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]
    category = models.CharField(max_length=50, choices=categories, default='Танки')

    def __str__(self):
        return f'{self.bul_title}'

    def get_absolute_url(self):
        return f'/board/{self.pk}'


# Модель откликов
class Reply(models.Model):
    reply_bul = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    reply_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField()
    reply_date = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(default=False)

    def get_absolute_url(self):
        return f'/board/{self.reply_bul.id}'


# Модель новостей администрации сайта
class News(models.Model):
    news_author = models.ForeignKey(User, on_delete=models.CASCADE)
    news_title = models.CharField(max_length=255)
    news_short_description = models.CharField(max_length=100, default='...')
    news_text = RichTextUploadingField()
    create_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f'/board/news/{self.pk}'


class Subscribers(models.Model):
    subscriber = models.OneToOneField(User, on_delete=models.CASCADE)

