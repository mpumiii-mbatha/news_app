from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Publisher, Journalist, Article, Subscription
from .signals import groups_permissions

User = get_user_model()


# Groups & Permissions Tests
class GroupsPermissionsTest(TestCase):

    def setUp(self):
        groups_permissions(sender=type('Sender', (), {'name': 'newsapp'})())

        # Groups
        self.readers = Group.objects.get(name='Reader')
        self.publishers = Group.objects.get(name='Publisher')
        self.journalists = Group.objects.get(name='Journalist')
        self.editors = Group.objects.get(name='Editor')

        # Permissions
        content_type = ContentType.objects.get_for_model(User)
        self.join_publisher = Permission.objects.get(codename='join_publisher', content_type=content_type)
        self.can_publish = Permission.objects.get(codename='can_publish', content_type=content_type)
        self.can_create = Permission.objects.get(codename='can_create', content_type=content_type)
        self.can_update = Permission.objects.get(codename='can_update', content_type=content_type)
        self.can_view = Permission.objects.get(codename='can_view', content_type=content_type)
        self.can_remove = Permission.objects.get(codename='can_remove', content_type=content_type)
        self.can_subscribe = Permission.objects.get(codename='can_subscribe', content_type=content_type)

    def test_groups_created(self):
        self.assertIsNotNone(self.readers)
        self.assertIsNotNone(self.publishers)
        self.assertIsNotNone(self.journalists)
        self.assertIsNotNone(self.editors)

    def test_permissions_created(self):
        perms = [
            self.join_publisher, self.can_publish, self.can_create,
            self.can_update, self.can_view, self.can_remove, self.can_subscribe
        ]
        for perm in perms:
            self.assertIsNotNone(perm)

    def test_readers_permissions(self):
        perms = self.readers.permissions.all()
        self.assertIn(self.can_subscribe, perms)
        self.assertEqual(perms.count(), 1)

    def test_publishers_permissions(self):
        perms = self.publishers.permissions.all()
        self.assertIn(self.can_publish, perms)
        self.assertEqual(perms.count(), 1)

    def test_journalists_permissions(self):
        perms = self.journalists.permissions.all()
        expected = [self.can_create, self.can_view, self.can_update, self.can_remove, self.join_publisher]
        for perm in expected:
            self.assertIn(perm, perms)
        self.assertEqual(perms.count(), len(expected))

    def test_editors_permissions(self):
        perms = self.editors.permissions.all()
        expected = [self.can_view, self.can_update, self.can_remove, self.join_publisher]
        for perm in expected:
            self.assertIn(perm, perms)
        self.assertEqual(perms.count(), len(expected))


# CRUD Tests
class NewsAppCRUDTests(TestCase):

    def setUp(self):
        groups_permissions(sender=type('Sender', (), {'name': 'newsapp'})())

        self.user = User.objects.create_user(username='testuser', password='password123', email='test@test.com')
        self.client = Client()
        self.client.login(username='testuser', password='password123')

        self.publisher = Publisher.objects.create(user=self.user)
        self.journalist = Journalist.objects.create(user=self.user, publisher=self.publisher)

    def test_register_user_get(self):
        response = self.client.get(reverse('news_app:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsapp/register.html')

    def test_register_user_post_success(self):
        response = self.client.post(reverse('news_app:register'), {
            'username': 'newuser',
            'password': 'StrongPass123!',
            'email': 'new@test.com'
        })
        self.assertRedirects(response, reverse('news_app:choose_group'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_create_post_get(self):
        response = self.client.get(reverse('news_app:create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsapp/create_post.html')

    def test_create_post_article_post(self):
        response = self.client.post(reverse('news_app:create_post'), {
            'post_type': 'article',
            'title': 'Test Article',
            'content': 'This is a test article',
            'publisher_id': self.publisher.id
        })
        self.assertRedirects(response, reverse('news_app:home'), fetch_redirect_response=False)
        self.assertTrue(Article.objects.filter(title='Test Article').exists())

    def test_article_list(self):
        Article.objects.create(title='Article 1', content='Content 1', journalist=self.journalist, publisher=self.publisher)
        response = self.client.get(reverse('news_app:article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Article 1')

    def test_read_article(self):
        article = Article.objects.create(title='Read Test', content='Read content', journalist=self.journalist, publisher=self.publisher)
        response = self.client.get(reverse('news_app:read_article', args=[article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Read Test')

    def test_subscribe_post_publisher(self):
        response = self.client.post(reverse('news_app:subscribe'), {'publisher_id': self.publisher.id})
        self.assertRedirects(response, reverse('news_app:subscribed_articles'))
        self.assertTrue(Subscription.objects.filter(user=self.user, publisher=self.publisher).exists())

    def test_register_under_publisher_post_journalist(self):
        response = self.client.post(reverse('news_app:register_under_publisher'), {'publisher_id': self.publisher.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'successfully registered')

    def test_view_mine_articles(self):
        Article.objects.create(title='My Article', content='My content', journalist=self.journalist, publisher=self.publisher)
        response = self.client.get(reverse('news_app:view_mine'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Article')
