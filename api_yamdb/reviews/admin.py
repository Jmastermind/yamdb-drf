from django.contrib import admin

from api_yamdb.admin import BaseAdmin
from reviews.models import Category, Genre, Title, User


@admin.register(Title)
class TitleAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'get_genres')
    search_fields = ('name',)
    list_filter = ('year',)

    @admin.display(description='genres')
    def get_genres(self, obj):
        return [
            genre[0]
            for genre in Title.objects.values_list('genre__name').filter(
                pk=obj.pk,
            )
        ]


@admin.register(Genre)
class GenreAdmin(BaseAdmin):
    list_display = ('name', 'slug')


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('name', 'slug')


@admin.register(User)
class UserAdmin(BaseAdmin):
    """Users admin panel"""

    list_display = ('username', 'role')
