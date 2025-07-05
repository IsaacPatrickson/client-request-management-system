import pytest
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from main.models import Client, RequestType, ClientRequest
from main.management.commands.create_limited_user_group import create_limited_users_permission_group

@pytest.fixture
def limited_user_client(client, django_user_model):
    # Set up permissions and user
    group = create_limited_users_permission_group()
    user = django_user_model.objects.create_user(username='limited', password='secure123', is_staff=True)
    user.groups.add(group)
    client.login(username='limited', password='secure123')
    return client


@pytest.mark.django_db
def test_limited_user_client_CRUD_permissions(limited_user_client):  
    client = limited_user_client
    
    # === Create Client ===
    # Get form first
    add_url = reverse('admin:main_client_add')
    response = client.get(add_url)
    assert response.status_code == 200
    
    response = client.post(add_url, {
        'name': 'Test Client',
        'email': 'test@example.com',
        'contact_number': '0123456789',
        'company_url': 'https://example.com',
        'is_active': 'on',
        '_save': 'Save',
        # Required for inlines
        'clientrequest_set-TOTAL_FORMS': 0,
        'clientrequest_set-INITIAL_FORMS': 0,
    })    
    assert response.status_code == 302  # Redirect on success
    assert Client.objects.filter(name='Test Client').exists()
    
    # === Read Client (Changelist) ===
    changelist_url = reverse('admin:main_client_changelist')
    response = client.get(changelist_url)
    assert response.status_code == 200

    # === Update Client ===
    client_obj = Client.objects.get(name='Test Client')
    change_url = reverse('admin:main_client_change', args=[client_obj.pk])
    response = client.post(change_url, {
        'name': 'Updated Client',
        'email': 'test@example.com',
        'contact_number': '0123456789',
        'company_url': 'https://example.com',
        'is_active': False,
        # Required again for inlines
        'clientrequest_set-TOTAL_FORMS': 0,
        'clientrequest_set-INITIAL_FORMS': 0,
        '_save': 'Save'
    })
    assert response.status_code == 302
    assert Client.objects.filter(name='Updated Client').exists()

    # === Delete Client (forbidden) ===
    delete_url = reverse('admin:main_client_delete', args=[client_obj.pk])
    response = client.get(delete_url)
    assert response.status_code == 403
    
@pytest.mark.django_db
def test_limited_user_request_type_CRUD_permissions(limited_user_client):
    client = limited_user_client

    # === Create Request Type ===
    add_url = reverse('admin:main_requesttype_add')
    response = client.post(add_url, {
        'name': 'Test Request Type',
        'description': 'Test Description'
    })
    assert response.status_code == 302  # Redirect on success
    assert RequestType.objects.filter(name='Test Request Type').exists()
    
    # === Read Request Type ===
    changelist_url = reverse('admin:main_requesttype_changelist')
    response = client.get(changelist_url)
    assert response.status_code == 200


    # === Update Request Type ===
    request_type_obj = RequestType.objects.get(name='Test Request Type')
    change_url = reverse('admin:main_requesttype_change', args=[request_type_obj.pk])
    response = client.post(change_url, {
        'name': 'Updated Test Request Type',
        'description': 'Updated Test Description'
    })
    assert response.status_code == 302
    assert RequestType.objects.filter(name='Updated Test Request Type').exists()

    # === Delete Request Type (forbidden) ===
    delete_url = reverse('admin:main_requesttype_delete', args=[request_type_obj.pk])
    response = client.get(delete_url)
    assert response.status_code == 403
    
@pytest.mark.django_db
def test_limited_user_client_request_CRUD_permissions(limited_user_client):
    client = limited_user_client
    
    # Create required foreign key objects
    client_obj = Client.objects.create(name='DCC', email='test@example.com')
    request_type = RequestType.objects.create(name='SEO Tech Check', description='Technical SEO audit')

    # === Create Client Request ===
    add_url = reverse('admin:main_clientrequest_add')
    response = client.post(add_url, {
        'client': client_obj.pk,
        'request_type': request_type.pk,
        'status': 'Pending',
        'description': 'Test Client Request Description'
    })
    assert response.status_code == 302  # Redirect on success
    assert client_obj.clientrequest_set.filter(description='Test Client Request Description').exists()
    
    # === Read Client Request ===
    changelist_url = reverse('admin:main_clientrequest_changelist')
    response = client.get(changelist_url)
    assert response.status_code == 200

    # === Update Client Request ===
    updated_client_obj = Client.objects.create(name='VetPartners', email='test@example.com')
    updated_request_type = RequestType.objects.create(name='Plugin Updates', description='Updating plugins')
    
    request_type_obj = ClientRequest.objects.get(description='Test Client Request Description')
    change_url = reverse('admin:main_clientrequest_change', args=[request_type_obj.pk])
    response = client.post(change_url, {
        'client': updated_client_obj.pk,
        'request_type': updated_request_type.pk,
        'status': 'In Progress',
        'description': 'Updated Test Client Request Description'
    })
    assert response.status_code == 302
    assert ClientRequest.objects.filter(description='Updated Test Client Request Description').exists()

    # === Delete Client Request (forbidden) ===
    delete_url = reverse('admin:main_clientrequest_delete', args=[request_type_obj.pk])
    response = client.get(delete_url)
    assert response.status_code == 403
    
models = ['client', 'requesttype', 'clientrequest']
actions = ['view', 'add', 'change']

@pytest.mark.django_db
def test_limited_user_permissions_check():
    # Assuming your create_limited_users_permission_group function is imported and available
    group = create_limited_users_permission_group()
    # Check group has the correct permissions for models
    expected_models = ['client', 'requesttype', 'clientrequest']
    expected_actions = ['view', 'add', 'change']

    for model in expected_models:
        content_type = ContentType.objects.get(app_label='main', model=model)
        # Check for view/add/change permissions
        for action in expected_actions:
            codename = f"{action}_{model}"
            perm = group.permissions.filter(content_type=content_type, codename=codename)
            assert perm.exists(), f"Group missing permission: {codename}"
        # Check that delete permission is NOT present
        delete_codename = f"delete_{model}"
        delete_perm = group.permissions.filter(content_type=content_type, codename=delete_codename)
        assert not delete_perm.exists(), f"Group should NOT have permission: {delete_codename}"