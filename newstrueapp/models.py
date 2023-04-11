import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache

class Author(models.Model):
    rating_author = models.IntegerField(default = 0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rating_author = 0
        all_posts = Post.objects.filter(author = self).values('rating_post')
        for post in all_posts:
            self.rating_author += post['rating_post']*3
        all_comments = Comment.objects.filter(user = self.user).values('rating_comment')
        for comment in all_comments:
            self.rating_author += comment['rating_comment']
        all_comments_for_author = Comment.objects.filter(post__author = self).values('rating_comment')
        for comment_for_author in all_comments_for_author:
            self.rating_author += comment_for_author['rating_comment']
        self.save()

    def __str__(self):
        return f'{self.user}'

class Cathegory(models.Model):
    cathegory_name = models.CharField(max_length = 255, unique = True, default = "other")
    subscribers = models.ManyToManyField(User, through='SubscribersCathegory')

    def __str__(self):
        return f'{self.cathegory_name}'


class SubscribersCathegory(models.Model):
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE)
    cathegory = models.ForeignKey(Cathegory, on_delete=models.CASCADE)

article = 'Article'
news = 'News'
#TYPE_POST = [(article, 'Статья'),
            # (news, 'Новость')]
#choices = TYPE_POST,
class Post(models.Model):
    date_post = models.DateTimeField(auto_now_add=True)
    head_post = models.CharField(max_length = 50, null=True)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0.0)
    type_post = models.CharField(max_length = 7, default='news')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cathegories = models.ManyToManyField (Cathegory, through = 'PostCathegory')

    def like(self):
        self.rating_post = self.rating_post + 1
        self.save()

    def dislike(self):
        self.rating_post = self.rating_post - 1
        self.save()

    def preview(self):
        if len(self.text_post) < 128:
            return self.text_post
        else:
            text_post_short = self.text_post[0:129]
            return f'{text_post_short}...'

    def __str__(self):
        return f'{self.head_post}, {self.date_post}, {self.text_post[0:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    @property
    def popular(self):
        return self.rating_post > 5

    @property
    def show_cat(self):
        cats = set(Post.objects.filter(pk=self.pk).values_list('cathegories__cathegory_name', flat=True))
        return cats

class PostCathegory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    cathegory = models.ForeignKey(Cathegory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.head_post} | {self.cathegory.cathegory_name}'

class Comment(models.Model):
    post = models.ForeignKey (Post, on_delete = models.CASCADE)
    user = models.ForeignKey (User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default = 0)

    def like(self):
        self.rating_comment = self.rating_comment + 1
        self.save()

    def dislike(self):
        self.rating_comment = self.rating_comment - 1
        self.save()

