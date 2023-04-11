from django.urls import path
from .views import PostList
from .views import PostDetail, PostCreate, PostUpdate, PostDelete, subscribe, unsubscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60*1) (PostList.as_view()), name = 'post_list'),
    #кэш - для примера, не использовать вместе с низкоуровневым кешированием
    path('<int:pk>', cache_page(60*5) (PostDetail.as_view()), name = 'post_detail'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit', PostUpdate.as_view(), name='article_edit'),
    path('article/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
    path('<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe')
]