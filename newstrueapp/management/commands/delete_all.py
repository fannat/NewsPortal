from django.core.management.base import BaseCommand, CommandError
from newstrueapp.models import Post, Cathegory, PostCathegory

class Command(BaseCommand):
    help = 'Удаление всех новостей выбранной категории'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('cathegory', type=str)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(f'Do you really want to delete all news in {options["cathegory"]}? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все статьи
            cathegory = Cathegory.objects.get(cathegory_name=options['cathegory'])
            Post.objects.filter(cathegories__cathegory_name = cathegory).delete()
            if Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category {cathegory}'))
            else:
                self.stdout.write(self.style.SUCCESS('Succesfully wiped news!'))
        else:
            self.stdout.write(self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим, что в доступе отказано