from django.core.management.base import BaseCommand
from articles.models import Tag


class Command(BaseCommand):
    help = 'Insert some default tags into the database'

    def handle(self, *args, **kwargs):
        tags = [
            {'name': 'Politics'},
            {'name': 'Drama'},
            {'name': 'Comedy'},
            {'name': 'Science'},
            {'name': 'Fight'},
            {'name': 'Shooting'},
            {'name': 'War'},
            {'name': 'Invention'},
            {'name': 'Discovery'},
            {'name': 'Crime'},
            {'name': 'Economy'},
            {'name': 'Environment'},
            {'name': 'Health'},
            {'name': 'Technology'},
            {'name': 'Espionage'},
            {'name': 'Finance'},
            {'name': 'Corruption'},
            {'name': 'Activism'},
            {'name': 'Government'},
            {'name': 'Celebrity'},
            {'name': 'Music'},
            {'name': 'Movies'},
            {'name': 'Sports'},
            {'name': 'Art'},
            {'name': 'Food'},
            {'name': 'Research'},
            {'name': 'Space'},
            {'name': 'Innovation'},
            {'name': 'Analysis'},
            {'name': 'Interview'},
            {'name': 'Business'},
            {'name': 'Disaster'},
            {'name': 'Accident'},
            {'name': 'Terrorism'},
            {'name': 'Investigation'},
            {'name': 'Scam'},
            {'name': 'Satire'},
            {'name': 'History'},
            {'name': 'Anime'},
            {'name': 'Vigilante'},
            {'name': 'Meme'},
            {'name': 'Crypto'},
            {'name': 'Controversy'},
        ]

        try:
            for tag in tags:
                Tag.objects.create(**tag)
            self.stdout.write(self.style.SUCCESS('Tags successfully inserted'))
        except Exception:
            self.stdout.write(self.style.ERROR('Could not insert tags.\nPerhaps there are duplicated tags?'))
        