from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from newsapp.models import Article, Newsletter, Journalist, Publisher
from newsapp.signals import groups_permissions  # ensure groups/permissions are set up


class NewsAppAPITests(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Setup groups and permissions
        class MockSender:
            name = "newsapp"
        groups_permissions(sender=MockSender())  # avoids AttributeError

        # Assign user to Journalist group
        journalist_group = Group.objects.get(name='Journalist')
        self.user.groups.add(journalist_group)
        self.user.save()

        # Create related publisher and journalist
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.journalist = Journalist.objects.create(user=self.user, publisher=self.publisher)

        # Use APIClient and authenticate
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Sample data
        self.article_data = {
            "title": "Test Article",
            "content": "This is a test article content.",
            "approved": True
        }
        self.newsletter_data = {
            "title": "Test Newsletter",
            "content": "This is a test newsletter content.",
            "approved": True
        }

    # -------------------- ARTICLE TESTS --------------------

    def test_get_articles(self):
        Article.objects.create(
            title="Article1",
            content="Content1",
            journalist=self.journalist,
            publisher=self.publisher,
            approved=True
        )
        url = reverse('news_app:api_articles')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_article(self):
        url = reverse('news_app:article-list')  # Updated for DRF viewset URL naming
        response = self.client.post(url, self.article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().title, "Test Article")

    # -------------------- NEWSLETTER TESTS --------------------

    def test_get_newsletters(self):
        Newsletter.objects.create(
            title="Newsletter1",
            content="Content1",
            journalist=self.journalist,
            publisher=self.publisher,
            approved=True
        )
        url = reverse('news_app:api_newsletters')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_newsletter(self):
        url = reverse('news_app:newsletter-list')  # Updated for DRF viewset URL naming
        response = self.client.post(url, self.newsletter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Newsletter.objects.count(), 1)
        self.assertEqual(Newsletter.objects.first().title, "Test Newsletter")
