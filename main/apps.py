from django.apps import AppConfig
import os
import logging

logger = logging.getLogger(__name__)

class MainConfig(AppConfig):
    # Use BigAutoField by default for model primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    def ready(self):
        # Import permission and seeding utility functions when the app is ready
        from .utils.permissions import create_limited_users_permission_group
        from .utils.seed_example_data import seed_example_clients
        try:
            # Create the limited users permission group and seed example clients on startup
            create_limited_users_permission_group()
            seed_example_clients()
        except Exception:
            # Ignore any exceptions here to avoid breaking app startup if data already exists or errors occur
            pass
        
        # Conditional seeding of example users during development only
        # 'RUN_MAIN' == 'true' ensures this runs only once with autoreload
        # Skip this in production environments
        if os.environ.get('RUN_MAIN') == 'true' and os.environ.get('DJANGO_ENV') != 'production':
            try:
                from .utils.seed_users import seed_example_users
                created = seed_example_users()
                if created:
                    # Log the usernames of users created during seeding
                    logger.info(f"Seeded users: {', '.join(created)}")
            except Exception as e:
                # Log any errors encountered while seeding users
                logger.error(f"Failed to seed users: {e}")