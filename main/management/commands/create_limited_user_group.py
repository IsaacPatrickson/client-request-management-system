from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
import logging

logger = logging.getLogger(__name__)

def create_limited_users_permission_group():
    # Ensure the 'LimitedUsers' group exists or create it if not.
    group, _ = Group.objects.get_or_create(name='LimitedUsers')

    models = ['client', 'requesttype', 'clientrequest']
    app_label = 'main'
    permission_actions = ['view', 'add', 'change']

    for model in models:
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            for action in permission_actions:
                codename = f"{action}_{model}"
                try:
                    permission = Permission.objects.get(content_type=content_type, codename=codename)
                    if not group.permissions.filter(pk=permission.pk).exists():
                        group.permissions.add(permission)
                        logger.info(f'Added {action} permission for {model}')
                    else:
                        logger.info(f'Permission {codename} already assigned to group')
                except Permission.DoesNotExist:
                    logger.warning(f'Permission {codename} not found for model {model}')
        except ContentType.DoesNotExist:
            logger.error(f'ContentType for model {model} not found.')

    return group


class Command(BaseCommand):
    help = "Create or update the LimitedUsers permission group with view, add, and change permissions."

    def handle(self, *args, **options):
        group = create_limited_users_permission_group()
        self.stdout.write(self.style.SUCCESS(f"LimitedUsers group created/updated successfully: {group.name}"))
