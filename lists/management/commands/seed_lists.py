import random

from django.contrib.admin.utils import flatten
from django.core.management import BaseCommand
from django_seed import Seed

from lists.models import List
from rooms.models import Room
from users.models import User

NAME = 'lists'


class Command(BaseCommand):
    help = f'This command creates many {NAME}.'

    def add_arguments(self, parser):
        parser.add_argument('--number', default=1, type=int, help=f'How many {NAME} do you ant to create?')

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        user = User.objects.filter(is_superuser=False)
        rooms = Room.objects.all()
        seeder.add_entity(List, number, {
            'user': lambda x: random.choice(user),
        })
        created = seeder.execute()
        cleaned = flatten(created.values())

        for pk in cleaned:
            lists = List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5): random.randint(6, 30)]
            lists.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f'{number} {NAME} created!'))
