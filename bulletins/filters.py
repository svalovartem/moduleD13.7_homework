from django_filters import FilterSet, ChoiceFilter, DateFromToRangeFilter, CharFilter, TypedChoiceFilter
from .models import *
from distutils.util import strtobool


class BulFilter(FilterSet):
    create_time = DateFromToRangeFilter(label='Дата публикации')
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
    category = ChoiceFilter(choices=categories, label='Категория')

    class Meta:
        model = Bulletin
        fields = {'create_time',
                  'category'}


class BulWideFilter(FilterSet):
    bul_author__username = CharFilter(label='Автор', lookup_expr='icontains')
    bul_title = CharFilter(label='Заголовок', lookup_expr='icontains')
    create_time = DateFromToRangeFilter(label='Дата публикации')
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
    category = ChoiceFilter(choices=categories, label='Категория')

    class Meta:
        model = Bulletin
        fields = {'bul_author__username',
                  'bul_title',
                  'create_time',
                  'category'}


class NewsFilter(FilterSet):
    create_time = DateFromToRangeFilter(label='Дата публикации')

    class Meta:
        model = News
        fields = {'create_time',
                  }


class ReplyFilter(FilterSet):
    reply_date = DateFromToRangeFilter(label='Дата публикации')
    reply_bul__bul_title = CharFilter(label='Объявление', lookup_expr='icontains')
    reply_user__username = CharFilter(label='Автор отклика', lookup_expr='icontains')
    BOOLEAN_CHOICES = (('false', 'Не принят'), ('true', 'Принят'))
    accept = TypedChoiceFilter(choices=BOOLEAN_CHOICES, coerce=strtobool, label='Статус отклика')

    class Meta:
        model = Reply
        fields = {'reply_bul__bul_title',
                  'reply_user__username',
                  'reply_date',
                  'accept'}


class SelfReplyFilter(FilterSet):
    reply_date = DateFromToRangeFilter(label='Дата публикации')
    reply_bul__bul_title = CharFilter(label='Объявление', lookup_expr='icontains')
    BOOLEAN_CHOICES = (('false', 'Не принят'), ('true', 'Принят'))
    accept = TypedChoiceFilter(choices=BOOLEAN_CHOICES, coerce=strtobool, label='Статус отклика')

    class Meta:
        model = Reply
        fields = {'reply_bul__bul_title',
                  'reply_date',
                  'accept'}
