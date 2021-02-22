from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'This Command tells me that he loves me.'

    def add_arguments(self, parser):
        parser.add_argument('--times', help='How many times do you want me to tell you that i love you.')

    def handle(self, *args, **options):
        times = options.get('times')
        for t in range(0, int(times)):
            self.stdout.write(self.style.ERROR('i love you'))
