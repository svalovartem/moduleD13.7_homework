from django.forms import ModelForm
from .models import *


class BulletinForm(ModelForm):

    class Meta:
        model = Bulletin
        fields = ['bul_title',
                  'category',
                  'bul_short_description',
                  'bul_text']

        labels = {'bul_title': 'Заголовок',
                  'category': 'Категория',
                  'bul_short_description': 'Краткое описание',
                  'bul_text': 'Текст объявления'}


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['news_title',
                  'news_short_description',
                  'news_text']

        labels = {'news_title': 'Заголовок новости',
                  'news_short_description': 'Краткое описание',
                  'news_text': 'Текст новости'}


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_text']

        labels = {'reply_text': 'Оставить отклик'}
