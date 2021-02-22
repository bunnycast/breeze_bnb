import random

from django.core.management import BaseCommand
from django_seed import Seed

from users.models import User
from rooms.models import Room, RoomType


class Command(BaseCommand):
    help = 'This command creates many rooms.'

    def add_arguments(self, parser):
        parser.add_argument('--number', default=1, type=int, help='How many rooms do you ant to create?')

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        host_candidate = User.objects.filter(is_superuser=False)
        room_types = RoomType.objects.all()
        seeder.add_entity(Room, number, {
            'name': seeder.faker.address(),
            'host': lambda x: random.choice(host_candidate),
            'room_type': lambda x:random.choice(room_types),
            'price': lambda x:random.randint(0, 300),
            'baths': lambda x:random.randint(0, 3),
            'bedrooms': lambda x:random.randint(0, 5),
            'beds': lambda x:random.randint(0, 3),
            'guests': lambda x:random.randint(0, 10),
        })
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f'{number} rooms created!'))
