import random

from django.core.management import BaseCommand
from django_seed import Seed

from rooms.models import Room
from users.models import User
from reviews.models import Review


class Command(BaseCommand):
    help = 'This command creates many reviews.'

    def add_arguments(self, parser):
        parser.add_argument('--number', default=1, type=int, help='How many reviews do you ant to create?')

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        user = User.objects.filter(is_superuser=False)
        room = Room.objects.all()
        seeder.add_entity(Review, number, {
            'accuracy': lambda x: random.randint(0, 6),
            'communication': lambda x: random.randint(0, 6),
            'cleanliness': lambda x: random.randint(0, 6),
            'location': lambda x: random.randint(0, 6),
            'check_in': lambda x: random.randint(0, 6),
            'value': lambda x: random.randint(0, 6),
            'room': lambda x: random.choice(room),
            'user': lambda x: random.choice(user),
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{number} reviews created!'))
