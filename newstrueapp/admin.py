from django.contrib import admin
from .models import Author, Post, Cathegory, Comment, PostCathegory, SubscribersCathegory

def nullfy_rating_post(modeladmin, request, queryset):# request — объект хранящий информацию о запросе
# и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating_post=0)
nullfy_rating_post.short_description = 'Обнулить рейтинг'

class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с новостями
    #list_display = [field.name for field in Post._meta.get_fields()] для всех полей
    list_display = ('date_post', 'author', 'popular', 'head_post', 'type_post', 'rating_post', 'show_cat')
    #list_filter = ('rating_post', 'head_post')
    search_fields = ('type_post', 'cathegories__cathegory_name')
    actions = [nullfy_rating_post]

# Register your models here.
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Cathegory)
admin.site.register(Comment)
admin.site.register(PostCathegory)
admin.site.register(SubscribersCathegory)
#admin.site.unregister(Post)