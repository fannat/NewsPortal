from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category, PostCategory


class Command(BaseCommand):
    help = 'Удаление всех новостей выбранной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(
            f'Вы хотите удалить все новости в разделе {options["category"]}? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()  # Ввести подтверждение вручную

        if answer == 'yes':
            category = Category.objects.get(category_name=options['category'])
            Post.objects.filter(categories__category_name=category).delete()
            if Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Невозможно найти категорию {category}'))
            else:
                self.stdout.write(self.style.SUCCESS('Все новости удалены!'))
        else:
            self.stdout.write(self.style.ERROR('Доступ запрещен'))
