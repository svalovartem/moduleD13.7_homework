from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.core.mail import get_connection, EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import datetime


@receiver(post_save, sender=News)
def news_created(sender, instance, created, **kwargs):
    if created:
        mails = list()
        subs = Subscribers.objects.all()
        for sub in subs:
            html_content = render_to_string(
                'subscribe/newnews.html', {'news_title': instance.news_title,
                                           'news_text': instance.news_text,
                                           'pk': instance.id})
            text_message = f'Здравствуй, {sub.subscriber.username}. Новости: "{instance.news_title}"'
            mail = sub.subscriber.email
            msg = EmailMultiAlternatives(
                subject=instance.news_title,
                body=text_message,
                from_email='ShinyBlackArrow@yandex.ru',
                to=[mail],
            )
            msg.attach_alternative(text_message + html_content, "text/html")
            mails.append(msg)

        get_connection().send_messages(mails)


@receiver(post_save, sender=Reply)
def replied(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string(
            'subscribe/replyemail.html', {'reply_bul': instance.reply_bul.bul_title,
                                          'reply_user': instance.reply_user.username,
                                          'pk': instance.reply_bul.id})
        text_message = f'Здравствуйте, {instance.reply_bul.bul_author.username}'
        mail = instance.reply_bul.bul_author.email
        msg = EmailMultiAlternatives(
            subject='Новый отклик на Ваше объявление в ДО The Steel MMORPG',
            body=text_message,
            from_email='ShinyBlackArrow@yandex.ru',
            to=[mail],
        )
        msg.attach_alternative(text_message + html_content, "text/html")
        msg.send()


@receiver(post_save, sender=Reply)
def accepted(sender, instance, update_fields, **kwargs):
    if update_fields and 'accept' in update_fields:
        if instance.accept:
            html_content = render_to_string(
                'subscribe/acceptemail.html', {'reply_bul': instance.reply_bul.bul_title,
                                               'reply_user': instance.reply_user.username,
                                               'pk': instance.reply_bul.id})
            text_message = f'Здравствуйте, {instance.reply_user.username}'
            mail = instance.reply_user.email
            msg = EmailMultiAlternatives(
                subject=f'Ваш отклик в ДО The Steel MMORPG принят',
                body=text_message,
                from_email='ShinyBlackArrow@yandex.ru',
                to=[mail],
            )
            msg.attach_alternative(text_message + html_content, "text/html")
            msg.send()


@receiver(post_save, sender=Subscribers)
def subscribed(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Подписка на новости Доски объявлений The Steel MMORPG',
            f'Здравствуйте, {instance.subscriber.username}. Вы подписались на новостную рассылку Доски объявлений The Steel MMORPG',
            'ShinyBlackArrow@yandex.ru',
            [f'{instance.subscriber.email}'],
            fail_silently=False,
        )
