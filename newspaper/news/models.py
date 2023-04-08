from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        comments_by_author = Comment.objects.filter(user_id=self.user_id).aggregate(models.Sum('rating'))['rating__sum']
        posts = Post.objects.filter(author_id=self.id).aggregate(models.Sum('rating'))
        post_id = Post.objects.filter(author_id=self.id).values_list('id', flat=True)
        comments_to_author_posts = Comment.objects.filter(post_id__in=post_id).aggregate(models.Sum('rating'))['rating__sum']

        self.rating = (int(posts['rating__sum']) * 3) + int(comments_by_author) + int(comments_to_author_posts)
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    AR = 'Article'
    NW = 'News'

    post_types = [
        (AR, 'Article'),
        (NW, 'News')
    ]

    post_type = models.CharField(max_length=7, choices=post_types, default=NW)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    content = models.TextField()

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post')
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        content = self.content[:124]
        if len(content) > 124:
            content += '...'
        return content


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField(max_length=500, default='')
    creation_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
