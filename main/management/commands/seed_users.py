from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from main.management.commands.create_limited_user_group import create_limited_users_permission_group


class Command(BaseCommand):
    help = 'Seed example users with various permissions and groups'

    def handle(self, *args, **options):
        created = []

        # Ensure the LimitedUsers group and its permissions exist
        create_limited_users_permission_group()

        # Create superadmin
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_superuser('superadmin', 'superadmin@example.com', 'superpass123')
            created.append('superadmin')
            self.stdout.write(self.style.SUCCESS('Created user: superadmin'))
        else:
            self.stdout.write('User "superadmin" already exists.')

        # Create admin user with full permissions
        if not User.objects.filter(username='adminuser').exists():
            admin_user = User.objects.create_user(
                'adminuser', 'admin@example.com', 'adminpass123', is_staff=True
            )
            # Give all permissions to adminuser
            admin_user.user_permissions.set(Permission.objects.all())
            created.append('adminuser')
            self.stdout.write(self.style.SUCCESS('Created user: adminuser'))
        else:
            self.stdout.write('User "adminuser" already exists.')

        # Create limited user and assign to LimitedUsers group
        if not User.objects.filter(username='limiteduser').exists():
            limited_user = User.objects.create_user(
                'limiteduser', 'user@example.com', 'userpass123', is_staff=True
            )
            limited_group = Group.objects.get(name='LimitedUsers')  # use existing group
            limited_user.groups.add(limited_group)
            created.append('limiteduser')
            self.stdout.write(self.style.SUCCESS('Created user: limiteduser'))
        else:
            self.stdout.write('User "limiteduser" already exists.')

        # Create no permissions user
        if not User.objects.filter(username='nopermissionsuser').exists():
            User.objects.create_user(
                'nopermissionsuser', 'user@example.com', 'userpass123'
            )
            created.append('nopermissionsuser')
            self.stdout.write(self.style.SUCCESS('Created user: nopermissionsuser'))
        else:
            self.stdout.write('User "nopermissionsuser" already exists.')

        self.stdout.write(self.style.NOTICE(f'Users created: {created}'))
