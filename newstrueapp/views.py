from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives, send_mail

from .models import Post, Cathegory, PostCathegory, SubscribersCathegory
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_post_for_subscribers_celery
from django.core.cache import cache


class PostList(ListView):
    model = Post
    ordering = '-date_post'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cathegory'] = list(PostCathegory.objects.filter(
            post=self.kwargs['pk']).values('cathegory', 'cathegory__cathegory_name'))
        check_subscribe = list(SubscribersCathegory.objects.filter(subscribers=self.request.user.id).values('cathegory'))
        context['subscribed'] = [n['cathegory'] for n in check_subscribe]
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь,
        # и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newstrueapp.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        path = self.request.META['PATH_INFO']
        if path == '/post/article/create/':
            post.type_post = 'article'

        post = form.save()
        send_post_for_subscribers_celery.delay(post.pk)
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('newstrueapp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
def subscribe(request, pk):
    user = request.user
    cathegory = Cathegory.objects.get(id=pk)
    cathegory.subscribers.add(user)
    return redirect('/post/')


@login_required
def unsubscribe(request, pk):
    user = request.user
    cathegory = Cathegory.objects.get(id=pk)
    cathegory.subscribers.remove(user)
    return redirect('/post/')

