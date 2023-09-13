from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from reviews.models import Category, Genre, Title, User


class CategoryTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin, cls.admin_client = (
            mixer.blend(User, role='admin'),
            APIClient(),
        )
        cls.admin_client.force_authenticate(cls.admin)
        cls.category = mixer.blend(Category)
        cls.genre = mixer.blend(Genre)

    def test_create_category(self):
        """Ensure we can create a new category object."""
        url = reverse('api:category-list')
        data = {
            'name': 'Игры',
            'slug': 'games',
        }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.json(),
        )
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(pk=2).name, data['name'])

    def test_delete_category(self):
        """Ensure we can delete category object."""
        url = reverse('api:category-detail', args=(self.category.slug,))
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_cant_create_category_anonymous(self):
        """
        Ensure we can't create a new category object anonymously.
        """
        url = reverse('api:category-list')
        data = {
            'name': 'Игры',
            'slug': 'games',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(Category.objects.count(), 1)

    def test_cant_delete_category_anonymous(self):
        """Ensure we can't delte a category object anonymously."""
        url = reverse('api:category-detail', args=(1,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(Category.objects.count(), 1)

    def test_cant_create_category_same_slug(self):
        """
        Ensure we can't create a new category object with the same slug.
        """
        url = reverse('api:category-list')
        data = {
            'name': 'Тигры',
            'slug': self.category.slug,
        }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            response.json()['slug'][0],
            'категория с таким слаг уже существует.',
        )
        self.assertEqual(Category.objects.count(), 1)

    def test_cant_patch_category(self):
        """
        Ensure we can't patch a category object.
        """
        url = reverse('api:category-detail', args=(1,))
        data = {
            'name': 'Тигры',
            'slug': 'games',
        }
        response = self.admin_client.patch(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_cant_replace_category(self):
        """
        Ensure we can't patch a category object.
        """
        url = reverse('api:category-detail', args=(1,))
        data = {
            'name': 'Тигры',
            'slug': 'games',
        }
        response = self.admin_client.put(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class TitleTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin, cls.admin_client = (
            mixer.blend(User, role='admin'),
            APIClient(),
        )
        cls.admin_client.force_authenticate(cls.admin)
        cls.category = mixer.blend(Category)
        cls.genre_1 = mixer.blend(Genre)
        cls.genre_2 = mixer.blend(Genre)
        cls.title = mixer.blend(Title)

    def test_get_titles(self):
        """Ensure we can get titles list."""
        self.assertEqual(Title.objects.count(), 1)
        url = reverse('api:title-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['results'][0]['name'],
            self.title.name,
        )

    def test_create_title(self):
        """Ensure we can create a new title object."""
        url = reverse('api:title-list')
        data = {
            'name': 'Silent Hill',
            'year': 2006,
            'description': 'Про город',
            'category': self.category.slug,
            'genre': [self.genre_1.slug, self.genre_2.slug],
        }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], data['name'])

    def test_delete_title(self):
        """Ensure we can delete title object."""
        self.assertEqual(Title.objects.count(), 1)
        url = reverse('api:title-detail', args=(1,))
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Title.objects.count(), 0)

    def test_patch_title(self):
        """Ensure we can partially update title object."""
        data = {
            'year': 1006,
        }
        url = reverse('api:title-detail', args=(1,))
        response = self.admin_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Title.objects.get().year, data['year'])

    def test_put_title(self):
        """Ensure we can replace title object."""
        data = {
            'name': 'Silent Hill',
            'year': 2006,
            'description': 'Про город',
            'category': self.category.slug,
            'genre': [self.genre_1.slug, self.genre_2.slug],
        }
        url = reverse('api:title-detail', args=(1,))
        response = self.admin_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Title.objects.get().year, data['year'])

    # Negative testing

    def test_cant_create_title_with_many_categories(self):
        category_2 = mixer.blend(Category)
        data = {
            'name': 'Silent Hill',
            'year': 1006,
            'description': 'Про город',
            'category': [self.category.slug, category_2.slug],
            'genre': [self.genre_1.slug, self.genre_2.slug],
        }
        url = reverse('api:title-list')
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_create_title_year_from_future(self):
        data = {
            'name': 'Silent Hill',
            'year': 3006,
            'description': 'Про город',
            'category': self.category.slug,
            'genre': [self.genre_1.slug],
        }
        url = reverse('api:title-list')
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(
            response.json()['year'][0],
            'Нельзя указывать произведения из будущего!',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
