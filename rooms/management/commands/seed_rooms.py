import random

from django.contrib.admin.utils import flatten
from django.core.management import BaseCommand
from django_seed import Seed

from users.models import User
from rooms.models import Room, RoomType, Photo, Amenity, Facility, HouseRule


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
            'name': lambda x: seeder.faker.address(),
            'host': lambda x: random.choice(host_candidate),
            'room_type': lambda x: random.choice(room_types),
            'price': lambda x: random.randint(0, 300),
            'baths': lambda x: random.randint(0, 3),
            'bedrooms': lambda x: random.randint(0, 5),
            'beds': lambda x: random.randint(0, 3),
            'guests': lambda x: random.randint(0, 10),
        })
        created_photos = seeder.execute()
        created_clean = flatten(created_photos.values())

        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        rules = HouseRule.objects.all()

        for pk in created_clean:
            room = Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 17)):
                Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f'room_photos/{random.randint(1, 31)}.webp',
                )
            for amenity in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(amenity)

            for facility in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(facility)

            for rule in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(rule)

        self.stdout.write(self.style.SUCCESS(f'{number} rooms created!'))
