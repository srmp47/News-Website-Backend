from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import News

class NewsListAPITest(APITestCase):
    def setUp(self):
        News.objects.create(title="first news", content="first content", tags="sport")
        News.objects.create(title="second news", content="second content", tags="healthy")

    def test_news_list(self):
        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_news_list_with_tag_filter(self):
        url = reverse('news-list') + '?tags=sport'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "first news")
