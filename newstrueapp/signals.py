from django.shortcuts import render, reverse, redirect
from django.dispatch import receiver
from django.core.mail import send_mail, mail_managers
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.db.models.signals import pre_save


from .models import Post, User, PostCathegory, SubscribersCathegory
from newstrue import settings

import datetime

def post_for_subscribers(subscriber, title, short_text, subscribers_email, pk):
        html_content = render_to_string('post_for_subscribers.html',
                                        {'text' : short_text,
                                         "link" : f'http://127.0.0.1:8000/post/{pk}',
                                         "user" : subscriber})
        #for n in subscribers_email:
        message = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email='marinaprosche@yandex.ru',
            to= [subscribers_email]
            )
        message.attach_alternative(html_content, "text/html")  # добавляем htm
        message.send()

@receiver(m2m_changed, sender=PostCathegory)
def send_post_for_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        cathegories = list(PostCathegory.objects.filter(post=instance.id).
                            values('cathegory'))
        subscribers_all = []
        for cathegory in cathegories:
            subscribers_all += (SubscribersCathegory.objects.filter(cathegory=cathegory['cathegory']).values
                               ('subscribers__username',
                                'subscribers__email'
                                   ))
            subscribers_list = {}
            for person in subscribers_all:
                #subscribers_list.append(person['subscribers__email'])
                subscribers_list[person['subscribers__username']] = person['subscribers__email']
            for n in subscribers_list.items():
                post_for_subscribers(n[0], instance.head_post, instance.text_post[:50], n[1], instance.pk)

                #post_for_subscribers(person['subscribers__email'], instance.head_post, instance.text_post[:50], subscribers_list, instance.pk)


@receiver(pre_save, sender=Post)
def stop_news(sender, instance, **kwargs):
    author = instance.author
    now = datetime.datetime.now() #текущее время
    day = now - datetime.timedelta(days=1) #промежуток длинною в день
    posts = Post.objects.filter(author = author, date_post__gte=day)
    if len(posts) > 10:
        raise Exception('Вы не можете публиковать больше трех постов в день!')
