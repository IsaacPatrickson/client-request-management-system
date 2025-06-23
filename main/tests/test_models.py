import pytest
from django.utils.timezone import make_aware
from datetime import datetime
from main.models import Client, ClientRequest, RequestType  # Adjust the import path if needed

# For TDD - Creating the models

# Test creating a Client instance with valid data
@pytest.mark.django_db
def test_create_client_with_valid_data():
    # Create a timezone-aware datetime object for the created_at field
    created_at = make_aware(datetime(2025, 6, 18, 14, 0))
    
    # Create a new Client object with all required fields
    client = Client.objects.create(
        name='Test Client',
        email='client@example.com',
        contact_number='123456789',
        company_url='https://example.com',
        created_at=created_at,
        is_active=True
    )
    
    # Assert each field matches the expected value
    assert client.name == 'Test Client'
    assert client.email == 'client@example.com'
    assert client.contact_number == '123456789'
    assert client.company_url == 'https://example.com'
    assert client.created_at == created_at
    assert client.is_active is True

# Test creating a RequestType instance with valid data
@pytest.mark.django_db
def test_create_request_type_with_valid_data():
    # Create a new RequestType object
    request_type = RequestType.objects.create(
        name='SEO Tech Check',
        description='Generic description of the request type. SEO Tech Check Description.',
    )
    
    # Assert the name and description contain expected values
    assert request_type.name == 'SEO Tech Check'
    assert 'SEO Tech Check' in request_type.description

# Test creating a ClientRequest instance including related Client and RequestType objects
@pytest.mark.django_db
def test_create_client_request_with_dependencies():
    # Create a timezone-aware datetime for timestamp fields
    timestamp = make_aware(datetime(2025, 6, 18, 15, 0))

    # Create a Client instance to be used as a foreign key
    client = Client.objects.create(
        name='Test Client',
        email='client@example.com',
        contact_number='123456789',
        company_url='https://example.com',
        created_at=timestamp,
        is_active=True
    )

    # Create a RequestType instance to be used as a foreign key
    request_type = RequestType.objects.create(
        name='SEO Tech Check',
        description='SEO Tech Check Description.'
    )

    # Create a ClientRequest linking to the Client and RequestType objects
    client_request = ClientRequest.objects.create(
        client=client,
        request_type=request_type,
        description='Run an SEO Check for VetPartners.',
        status='In Progress',
        created_at=timestamp,
        updated_at=timestamp
    )

    # Assert the ClientRequest fields and related foreign keys have expected values
    assert client_request.client.name == 'Test Client'
    assert client_request.request_type.name == 'SEO Tech Check'
    assert client_request.status == 'In Progress'
    assert 'VetPartners' in client_request.description
    assert client_request.created_at == timestamp
