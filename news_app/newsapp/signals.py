'''Imported modules'''
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import User


@receiver(post_migrate)
def groups_permissions(sender, **kwargs):  # pylint: disable=unused-argument
    """
    Groups permissions
    """
    print(sender.name)
    if 'newsapp' in sender.name:
        readers, _ = Group.objects.get_or_create(name='Reader')
        publishers, _ = Group.objects.get_or_create(name='Publisher')
        journalists, _ = Group.objects.get_or_create(name='Journalist')
        editors, _ = Group.objects.get_or_create(name='Editor')

        content_type = ContentType.objects.get_for_model(User)

        # Publisher Permission
        join_publisher, _ = Permission.objects.get_or_create(
            codename='join_publisher',
            content_type=content_type
        )

        # Publisher and Journalist Permissions
        can_publish, _ = Permission.objects.get_or_create(
            codename='can_publish',
            content_type=content_type
        )

        # Publisher, Journalist and Editor Permissions
        can_create, _ = Permission.objects.get_or_create(
            codename='can_create',
            content_type=content_type
        )

        can_update, _ = Permission.objects.get_or_create(
            codename='can_update',
            content_type=content_type
        )

        can_view, _ = Permission.objects.get_or_create(
            codename='can_view',
            content_type=content_type
        )

        can_remove, _ = Permission.objects.get_or_create(
            codename='can_remove',
            content_type=content_type
        )

        can_subscribe, _ = Permission.objects.get_or_create(
            codename='can_subscribe',
            content_type=content_type
        )

        readers.permissions.add(can_subscribe)
        publishers.permissions.add(can_publish)
        journalists.permissions.add(can_create, can_view,
                                     can_update, can_remove, join_publisher)
        editors.permissions.add(can_view, can_update, can_remove, join_publisher)
