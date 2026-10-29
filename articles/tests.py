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

class CustomPaginationTestCase(APITestCase):
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

    def test_custom_pagination_structure_and_default_size(self):
        url = reverse('article-list-custom')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('page_info', response.data)
        self.assertIn('items_info', response.data)
        self.assertIn('results', response.data)

        page_info = response.data['page_info']
        items_info = response.data['items_info']

        self.assertEqual(page_info['current_page'], 1)
        self.assertEqual(page_info['total_pages'], 7)
        self.assertTrue(page_info['has_next'])
        self.assertFalse(page_info['has_previous'])

        self.assertEqual(items_info['total_items'], 50)
        self.assertEqual(items_info['page_items_count'], 8)
        self.assertEqual(items_info['page_size'], 8)
        self.assertEqual(len(response.data['results']), 8)

    def test_custom_pagination_dynamic_size(self):
        url = reverse('article-list-custom') + '?page_size=12'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items_info']['page_size'], 12)
        self.assertEqual(len(response.data['results']), 12)

    def test_custom_pagination_invalid_page_size(self):
        url_invalid = reverse('article-list-custom') + '?page_size=invalid'
        response_invalid = self.client.get(url_invalid)
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('page_size', response_invalid.data)

        url_zero = reverse('article-list-custom') + '?page_size=0'
        response_zero = self.client.get(url_zero)
        self.assertEqual(response_zero.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('page_size', response_zero.data)

        url_neg = reverse('article-list-custom') + '?page_size=-5'
        response_neg = self.client.get(url_neg)
        self.assertEqual(response_neg.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('page_size', response_neg.data)
