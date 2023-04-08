from django.contrib.auth.models import User
from django.db.models import Max
from news.models import Author
from news.models import Category
from news.models import Post
from news.models import Comment


# Создание 2х пользователей
user1 = User.objects.create_user('fannat')
user2 = User.objects.create_user('Я-робот')

# Создание 2х авторов связанных с пользователями
author_1 = Author.objects.create(user=user1)
author_2 = Author.objects.create(user=user2)


# Создание 4х категорий
Category.objects.bulk_create([Category(category_name='Футбол'), Category(category_name='Хоккей'), Category(category_name='Баскетбол'), Category(category_name='Жены Спортсменов')])


# Создание 2х статей и новости

text_1 = ''' Ванда Нара, являющаяся супругой нападающего "Интера" Мауро Икарди, заявила,
что информация о том, что форвард не будет играть за клуб, пока ему не вернут капитанскую повязку,
является ложной. Во вторник об этом сообщило итальянское издание Gazzetta dello Sport, 
также написавшее, что девушка потребовала от "нерадзурри" извинений.
- Позор! La Gazzetta является партнером "Интера". То, что они продолжают публиковать этот мусор, делает ситуацию более опасной. Правда всегда одна '''
text_2 = ''' В конце прошлой недели «Спартак» стал победителем Winline Зимнего кубка РПЛ.
 Результаты мачей с участием красно-белых:
  «Ростов» — 0:0 в основное время и 2:1 по пенальти, «Краснодар» — 4:0, «Сочи» — 2:0.
  По результату безупречно: победа на турнире при шести забитых и нуле пропущенных мячей. '''
text_3 = ''' "Вашингтон" вылетел из плей-офф Кубка Стэнли. Клуб из столицы США в овертайме проиграл "Флориде" со счетом 3:4.
Отличиться Овечкину на этот раз не удалось. Итоговый счет в серии – 4:2 в пользу "Флориды". '''

post_1 = Post.objects.create(post_type='AR', title='"Позор и мусор". Жена Икарди - о слухах вокруг форварда "Интера"', content=text_1, author=author_2)
post_1.categories.add(*Category.objects.filter(category_name__in=['Футбол', 'Жены Спортсменов']))

post_2 = Post.objects.create(post_type='AR', title='Спартак все равно всех победит', content=text_2, author=author_2)
post_2.categories.add(*Category.objects.filter(category_name__in=['Футбол']))

post_3 = Post.objects.create(post_type='NW', title='Вашингтон вылетел из борьбы за кубок Стэнли', content=text_3, author=author_1)
post_3.categories.add(Category.objects.get(category_name='Хоккей'))


#Комментарии

comment_1 = Comment.objects.create(comment='Ванда - классная ципочка!', post_id=1, user_id=1)
comment_2 = Comment.objects.create(comment='Спартак чемпион!!!', post_id=2, user_id=1)
comment_3 = Comment.objects.create(comment='Удачи Овечкину и Бекстрому в следующем году.', post_id=3, user_id=2)
comment_4 = Comment.objects.create(comment='Флорида не была явно сильнее,просто повезло.', post_id=3, user_id=2)
comment_5 = Comment.objects.create(comment='Ванда - Женщина с низкой социальной ответственностью :) ', post_id=1, user_id=2)

# Изменение рейтинга постов и комментарий с помощью like и dislike

Post.objects.get(id="1").like()
Post.objects.get(id="1").like()
Post.objects.get(id="1").dislike()

Post.objects.get(id="2").like()
Post.objects.get(id="2").like()
Post.objects.get(id="2").like()
Post.objects.get(id="3").like()
Post.objects.get(id="3").like()

Post.objects.get(id="3").dislike()
Post.objects.get(id="3").like()
Post.objects.get(id="3").dislike()
Post.objects.get(id="3").like()

Comment.objects.get(id="1").dislike()
Comment.objects.get(id="1").dislike()
Comment.objects.get(id="1").dislike()

Comment.objects.get(id="2").dislike()
Comment.objects.get(id="2").like()

Comment.objects.get(id="3").like()
Comment.objects.get(id="3").dislike()
Comment.objects.get(id="3").dislike()

Comment.objects.get(id="4").like()
Comment.objects.get(id="4").like()
Comment.objects.get(id="4").like()
Comment.objects.get(id="4").dislike()

Comment.objects.get(id="5").like()
Comment.objects.get(id="5").like()


Author.objects.get(id=1).update_rating()
Author.objects.get(id=2).update_rating()

# Получение имени пользователя с максимальным рейтингом

max_rating = Author.objects.aggregate(max_rating=Max('rating'))['max_rating']
best_author = Author.objects.select_related('user').get(rating=max_rating)
best_author_info = Author.objects.order_by('-rating').values_list('user__username', 'rating').first()

# Вывод данных о лучшем посте

post_max_rating = Post.objects.filter(post_type='AR').aggregate(rating_max=Max('rating'))['rating_max']
max_rat_pid = Post.objects.get(rating=post_max_rating, post_type='AR').id
prev = Post.objects.get(id=max_rat_pid).preview()

best_article_information = Post.objects.filter(id=max_rat_pid).values_list('created', 'author_id__user__username', 'rating', 'title').first(), prev

# Комментарии

r = Comment.objects.filter(post_id=max_rat_pid).values_list('creation_time', 'user_id__username', 'rating', 'comment')