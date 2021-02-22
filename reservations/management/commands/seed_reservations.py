import random
from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django_seed import Seed

from reservations.models import Reservation
from rooms.models import Room
from users.models import User

NAME = 'reservations'


class Command(BaseCommand):
    help = f'This command creates many {NAME}.'

    def add_arguments(self, parser):
        parser.add_argument('--number', default=1, type=int, help=f'How many {NAME} do you ant to create?')

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        guest = User.objects.filter(is_superuser=False)
        room = Room.objects.all()
        seeder.add_entity(Reservation, number, {
            'status': lambda x: random.choice(['pending', 'confirmed', 'canceled']),
            'guest': lambda x: random.choice(guest),
            'room': lambda x: random.choice(room),
            'check_in': lambda x: datetime.now(),
            'check_out': lambda x: datetime.now() + timedelta(days=random.randint(3, 25)),
        })
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f'{number} {NAME} created!'))
