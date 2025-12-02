'''Modules imported'''
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from rest_framework import serializers


class Publisher(models.Model):
    """
     Represents a Publisher in the system.

    Attributes:
        user (User): One-to-one relationship with Django's User model.
        published_at (DateTimeField): Timestamp when the
        publisher profile was created.

    Meta:
        permissions (list): Custom permissions for publishers.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username  # pylint: disable=no-member

    class Meta:
        permissions = [
            ("can_publish", "Can publish posts"),
            ("can_view", "Can view own articles"),
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
    Represents a Journalist in the system.

    Attributes:
        user (User): One-to-one relationship with Django's User model.
        publisher (Publisher): Foreign key to the
        Publisher the journalist belongs to.
        created_at (DateTimeField): Timestamp when the
        journalist profile was created.

    Meta:
        permissions (list): Custom permissions for journalists.
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
    Represents an Editor in the system.

    Attributes:
        user (User): One-to-one relationship with Django's User model.
        publisher (Publisher): Foreign key to the
        Publisher the editor belongs to.
        edited_at (DateTimeField): Timestamp when the
        editor profile was created.

    Meta:
        permissions (list): Custom permissions for editors.
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
            ("can_publish", "Can publish posts"),
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
    Represents a Reader in the system.

    Attributes:
        user (User): One-to-one relationship with Django's User model.

    Meta:
        permissions (list): Custom permissions for readers.
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
    Represents a news article in the application.

    Attributes:
        title (str): The title of the article.
        journalist (Journalist): Author of the article.
        publisher (Publisher): Publisher of the article.
        content (TextField): The body text of the article.
        approved (bool): Indicates whether the article is approved for
        publishing.
        created_at (DateTimeField): Timestamp when the article was created.
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

    def __str__(self):  # pylint: disable=no-member
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
    Represents a Newsletter published by a journalist.

    Attributes:
        title (str): The title of the newsletter.
        journalist (Journalist): Author of the newsletter.
        publisher (Publisher): Publisher of the newsletter.
        content (TextField): Body text of the newsletter.
        approved (bool): Indicates whether the newsletter is approved.
        created_at (DateTimeField): Timestamp when the newsletter was created.
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
     Represents a user's subscription to a Publisher or Journalist.

    Attributes:
        user (User): The user who subscribes.
        type (str): Subscription type ('publisher' or 'journalist').
        publisher (Publisher): Optional, if subscribing to a publisher.
        journalist (Journalist): Optional, if subscribing to a journalist.
        subscription_date (DateTimeField): Date when the subscription was created.
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
    Represents a password reset token for a user.

    Attributes:
        user (User): The user associated with the reset token.
        token (str): The unique token string.
        expiry_date (DateTimeField): Expiration date of the token.
        used (bool): Flag indicating whether the token has been used.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)
