import csv

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews import models


class Command(BaseCommand):
    """
    Imports tables from CSV files.

    Make sure to clear your db before using this command.

    Usage:
    ```
    manage.py flush
    manage.py importcsv [-s, --silent]
    ```
    """

    help = 'Imports tables from CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--silent',
            action='store_true',
            help='Hide creation messages.',
        )

    def handle(self, *args, **options):
        data = (
            ('category.csv', models.Category, 'Категория'),
            ('genre.csv', models.Genre, 'Жанр'),
            ('users.csv', models.User, 'Пользователь'),
            ('title.csv', models.Title, 'Произведение'),
            ('title_genre.csv', models.TitleGenre, 'Произведение-жанр'),
            ('review.csv', models.Review, 'Отзыв'),
            ('comments.csv', models.Comment, 'Комментарий'),
        )
        for item in data:
            with open(
                BASE_DIR / 'static' / 'data' / item[0],
                encoding='utf-8',
            ) as f:
                dreaded = csv.DictReader(f)
                for row in dreaded:
                    _, created = item[1].objects.update_or_create(**row)
                    if created and not options['silent']:
                        print(f'{item[2]} `{_}` has been created.')
