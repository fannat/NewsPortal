from django.contrib import admin
from .models import Author, Post, Category, Comment, PostCategory


def nullfy_rating_post(modeladmin, request, queryset):
    queryset.update(rating_post=0)
    nullfy_rating_post.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    search_fields = ('type_post', 'categories__category_name')
    actions = [nullfy_rating_post]


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostCategory)
