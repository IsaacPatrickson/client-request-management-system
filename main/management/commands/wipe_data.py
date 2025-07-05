"""
Delete ALL data in User, Client, RequestType, ClientRequest.

Usage:
    python manage.py wipe_data            ← shows a safety prompt
    python manage.py wipe_data --yes      ← skips confirmation
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import Client, RequestType, ClientRequest

class Command(BaseCommand):
    help = "Remove every record from the core tables (User, Client, RequestType, ClientRequest)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Skip confirmation prompt.",
        )

    def handle(self, *args, **options):
        if not options["yes"]:
            confirm = input(
                "⚠️  This will DELETE all Users, Clients, RequestTypes and "
                "ClientRequests.\nType 'delete' to continue: "
            )
            if confirm.lower().strip() != "delete":
                self.stdout.write(self.style.WARNING("Aborted."))
                return

        User = get_user_model()

        deleted_client_requests, _ = ClientRequest.objects.all().delete()
        deleted_request_types, _  = RequestType.objects.all().delete()
        deleted_clients, _        = Client.objects.all().delete()
        deleted_users, _          = User.objects.all().exclude(is_superuser=True).delete()

        total = (
            deleted_client_requests
            + deleted_request_types
            + deleted_clients
            + deleted_users
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {total} objects "
                f"({deleted_users} Users, "
                f"{deleted_clients} Clients, "
                f"{deleted_request_types} RequestTypes, "
                f"{deleted_client_requests} ClientRequests)."
            )
        )