# main/management/commands/seed_data.py
"""
Create 10 Clients, 10 RequestTypes, 10 ClientRequests + 4 demo Users.

Usage:
    python manage.py seed_data
"""
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from main.models import Client, RequestType, ClientRequest


class Command(BaseCommand):
    help = "Populate the database with predictable seed data."

    def handle(self, *args, **options):

        # -----------------------------------------------------------------
        # 1. Clients
        # -----------------------------------------------------------------
        clients = []
        for i in range(1, 11):
            clients.append(
                Client.objects.create(
                    name=f"client{i:02d}",
                    email=f"client{i:02d}@example.com",
                    contact_number=f"07{random.randint(10000000, 99999999)}",
                    company_url=f"https://client{i:02d}.com",
                    is_active=bool(i % 2),
                )
            )

        # -----------------------------------------------------------------
        # 2. RequestTypes
        # -----------------------------------------------------------------
        request_types = []
        for i in range(1, 11):
            request_types.append(
                RequestType.objects.create(
                    name=f"Request Type #{i}",
                    description=f"Seed description for request type {i}",
                )
            )

        # -----------------------------------------------------------------
        # 3. ClientRequests
        # -----------------------------------------------------------------
        statuses = ["Pending", "In Progress", "Completed"]
        now = timezone.now()

        for i in range(10):
            ClientRequest.objects.create(
                client=clients[i],
                request_type=request_types[i],
                status=statuses[i % 3],
                description=f"Seed request {i+1}",
                created_at=now,
                updated_at=now,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded: 4 Users, 10 Clients, 10 RequestTypes, 10 ClientRequests."
            )
        )
