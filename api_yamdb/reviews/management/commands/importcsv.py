import csv

from django.core.management.base import BaseCommand
from reviews.models import Categories, Comments, Genres, Reviews, Titles, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        models_db = {
            Categories: 'category',
            Comments: 'comments',
            Genres: 'genre',
            Reviews: 'review',
            Titles: 'titles',
            User: 'users'
        }
        for model, file in models_db.items():
            with open(f'static/data/{file}.csv') as f:
                reader = csv.DictReader(f)
                model.objects.bulk_create(model(**data) for data in reader)
