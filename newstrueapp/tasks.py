from celery import shared_task
from newstrueapp.signals import post_for_subscribers
from .models import PostCathegory, SubscribersCathegory, Post, Cathegory
from newstrue import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

import datetime
import time

@shared_task
def send_post_for_subscribers_celery(post_pk):
    post = Post.objects.get(id=post_pk) #получаем пост
    cathegories = post.cathegories.all() #получаем все категории поста
    subscribers_all = []
    for cathegory in cathegories:
        subscribers_all += cathegory.subscribers.all() #для каждой категории находим подписчиков и добавляем в список
    subscribers_list = {} #создаем словарь
    for person in subscribers_all:
        #subscribers_list.append(person.email) #для каждого из подписчиков добавляем мэйл и имя
        subscribers_list[person.username] = person.email
    for n in subscribers_list.items():
        post_for_subscribers(n[0], post.head_post, post.text_post[:50], n[1], post.pk)


@shared_task
def week_post():
    today = datetime.datetime.now()
    day_week_ago = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_post__gte=day_week_ago)
    cathegories = set(posts.values_list('cathegories__cathegory_name', flat=True)) #берем только имя
    subscribers = set(Cathegory.objects.filter(cathegory_name__in=cathegories).values_list('subscribers__email', flat=True))

    html_content = render_to_string('week_posts.html',{
            'link': f'http://127.0.0.1:8000',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject="Новости за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
