from django.core.management.base import BaseCommand
from main.models import Client

class Command(BaseCommand):
    help = 'Seed example clients into the database'

    def handle(self, *args, **options):
        created = []

        clients_to_seed = [
            {
                'name': 'vetpartners',
                'email': 'vetpartners@site.com',
                'contact_number': '07999999',
                'company_url': 'https://www.vetpartners.co.uk/',
                'is_active': True
            },
            {
                'name': 'dcc',
                'email': 'dcc@site.com',
                'contact_number': '07899999',
                'company_url': 'https://dccpropane.com/',
                'is_active': True
            },
            {
                'name': 'curaleaf',
                'email': 'curaleaf@site.com',
                'contact_number': '07891999',
                'company_url': 'https://curaleafpharmacy.co.uk/',
                'is_active': False
            }
        ]

        for client in clients_to_seed:
            if not Client.objects.filter(name=client['name']).exists():
                Client.objects.create(**client)
                created.append(client['name'])
                self.stdout.write(self.style.SUCCESS(f"Created client: {client['name']}"))
            else:
                self.stdout.write(f"Client '{client['name']}' already exists.")

        self.stdout.write(self.style.NOTICE(f"Clients created: {created}"))
