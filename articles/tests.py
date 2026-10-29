from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
from articles.models import Article

class GlobalPaginationTestCase(APITestCase):
    def setUp(self):
        now = timezone.now()
        for i in range(1, 56):
            Article.objects.create(
                title=f'Test Article {i}',
                content=f'Content for test article {i}',
                author='Tester',
                is_published=(i <= 50),
                created_at=now - timedelta(days=60 - i)
            )

    def test_global_default_page_size_is_fifteen(self):
        url = reverse('article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 50)
        self.assertEqual(len(response.data['results']), 15)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_global_page_navigation(self):
        url = reverse('article-list') + '?page=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 15)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])

    def test_global_dynamic_page_size(self):
        url = reverse('article-list') + '?page_size=20'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)

    def test_global_max_page_size_limit(self):
        url = reverse('article-list') + '?page_size=100'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 50)

    def test_invalid_page_number_returns_404(self):
        url_out_of_range = reverse('article-list') + '?page=999'
        response = self.client.get(url_out_of_range)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url_non_integer = reverse('article-list') + '?page=abc'
        response_non_integer = self.client.get(url_non_integer)
        self.assertEqual(response_non_integer.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_published_articles_returned_in_creation_order(self):
        url = reverse('article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for item in results:
            self.assertTrue(item['is_published'])
        created_dates = [item['created_at'] for item in results]
        self.assertEqual(created_dates, sorted(created_dates, reverse=True))
