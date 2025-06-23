from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
import logging

logger = logging.getLogger(__name__)

def create_limited_users_permission_group():
    # Ensure the 'LimitedUsers' group exists or create it if not.
    # The underscore (_) captures a boolean indicating if the group was created (True) or retrieved (False).
    group, _ = Group.objects.get_or_create(name='LimitedUsers')

    # Define the models for which permissions will be assigned
    models = ['client', 'requesttype', 'clientrequest']
    app_label = 'main' # Django app label containing these models
    permission_actions = ['view', 'add', 'change'] # Actions to assign permissions for

    # Loop over each model to assign permissions
    for model in models:
        try:
            # Get the ContentType object for the model to identify permissions linked to it
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            for action in permission_actions:
                # Build the permission codename (e.g., 'view_client', 'add_requesttype')
                codename = f"{action}_{model}"
                try:
                    # Retrieve the permission object by content type and codename
                    permission = Permission.objects.get(content_type=content_type, codename=codename)
                    # Add the permission to the group if not already assigned
                    if not group.permissions.filter(pk=permission.pk).exists():
                        group.permissions.add(permission)
                        logger.info(f'Added {action} permission for {model}')
                    else:
                        logger.info(f'Permission {codename} already assigned to group')
                except Permission.DoesNotExist:
                    # Log a warning if the permission does not exist in the database
                    logger.warning(f'Permission {codename} not found for model {model}')
        except ContentType.DoesNotExist:
            # Log an error if the ContentType for the model cannot be found
            logger.error(f'ContentType for model {model} not found.')
            
    return group