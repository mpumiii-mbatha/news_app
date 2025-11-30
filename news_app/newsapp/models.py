'''Modules imported'''
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from rest_framework import serializers


class Publisher(models.Model):
    """
    Publisher class
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username  # pylint: disable=no-member

    class Meta:
        permissions = [
            ("can_publish", "Can publish posts"),
        ]


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for publisher class
    """
    class Meta:
        model = Publisher
        fields = ['user', 'published_at']


class Journalist(models.Model):
    """
    Journalist class
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="journalists",
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username  # pylint: disable=no-member

    class Meta:
        permissions = [
            ("can_update", "Can update posts"),
            ("can_create", "Can write articles and newsletters"),
            ("can_remove", "Can delete posts"),
            ("join_publsiher", "Can join publisher"),
            ("can_view", "Can view own articles"),
        ]


class JournalistSerializer(serializers.ModelSerializer):
    """
    Serializer for journalist class
    """
    class Meta:
        model = Journalist
        fields = ['user', 'publisher', 'created_at']


class Editor(models.Model):
    """
    Editor class
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="editors",
        null=True, blank=True
    )
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username  # pylint: disable=no-member

    class Meta:
        permissions = [
            ("can_update", "Can update posts"),
            ("can_remove", "Can delete posts"),
            ("join_publsiher", "Can join publisher"),
            ("can_view", "Can view own articles"),
        ]


class EditorSerializer(serializers.ModelSerializer):
    """
    Serializer for editor class
    """
    class Meta:
        model = Editor
        fields = ['user', 'publisher', 'edited_at']


class Reader(models.Model):
    """
    Reader class
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="reader_profile")

    def __str__(self):
        return self.user.username  # pylint: disable=no-member

    class Meta:
        permissions = [
            ("can_subscribe", "Can subscribe to journalist or publisher"),
        ]


class Article(models.Model):
    """
    Article class
    """
    title = models.CharField(max_length=255)
    journalist = models.ForeignKey(
        Journalist,
        on_delete=models.CASCADE,
        related_name="articles_written"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="articles_published"
    )
    content = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for article class
    """
    class Meta:
        model = Article
        fields = ['title', 'content', 'journalist',
                  'publisher', 'approved', 'created_at']


class Newsletter(models.Model):
    """
    Newsletter class
    """
    title = models.CharField(max_length=255)
    journalist = models.ForeignKey(
        Journalist,
        on_delete=models.CASCADE,
        related_name="newsletters_written"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="newsletters_published"
    )
    content = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for article class
    """
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'journalist',
                  'publisher', 'approved', 'created_at']


class Subscription(models.Model):
    """
    Subscription Model
    """
    SUBSCRIPTION_TYPES = [
        ('publisher', 'Publisher'),
        ('journalist', 'Journalist'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES)
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='publisher_subscriptions'
    )
    journalist = models.ForeignKey(
        Journalist,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='journalist_subscriptions'
    )
    subscription_date = models.DateTimeField(auto_now=True)

    def __str__(self):  # pylint: disable=no-member
        if self.type == 'publisher' and self.publisher:
            return (f"Subscribed to"
                    f"{self.publisher.user.username}")  # pylint: disable=no-member
        elif self.type == 'journalist' and self.journalist:
            return (f"Subscribed to"
                    f"{self.journalist.user.username}")  # pylint: disable=no-member
        return "Successfully Subscribed"


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for subscription class
    """
    class Meta:
        model = Subscription
        fields = '__all__'


class ResetToken(models.Model):
    """
    Class defining tokens granted to user for password restting
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)
