import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_regular_user_redirects_to_user_dashboard(client):
    # Test that a regular user is redirected to the user dashboard after login
    # Create a standard user (not staff or superuser)
    User.objects.create_user(username='newuser', password='password123')
    
    # Post login credentials to the login URL
    url = reverse('login')
    response = client.post(url, {
        'username': 'newuser',
        'password': 'password123',
    })

    # Assert the response is a redirect (status code 302)
    assert response.status_code == 302
    # Assert the redirect location is the user dashboard URL
    assert response.url == reverse('user-dashboard')
    
    
@pytest.mark.django_db
def test_admin_user_redirects_to_admin_dashboard(client):
    # Test that a staff user is redirected to the admin dashboard after login
    # Create a staff user by setting is_staff=True
    User.objects.create_user(
        username='adminuser',
        password='adminpass123',
        is_staff=True  # or is_superuser=True
    )

    # Post login credentials to login URL
    url = reverse('login')
    response = client.post(url, {
        'username': 'adminuser',
        'password': 'adminpass123',
    })

    # Assert redirect response status code 302
    assert response.status_code == 302
    # Assert redirect location is the django admin dashboard URL
    assert response.url == '/admin/'    
    
@pytest.mark.django_db
def test_admin_user_redirects_to_admin_dashboard(client):
    # Test that a superuser is redirected to the admin dashboard after login
    # Create a superuser by setting is_superuser=True
    User.objects.create_user(
        username='superuser',
        password='superpass123',
        is_superuser=True
    )

    # Post login credentials to login URL
    url = reverse('login')
    response = client.post(url, {
        'username': 'superuser',
        'password': 'superpass123',
    })

    # Assert redirect response status code 302
    assert response.status_code == 302
    # Assert redirect location is the django admin dashboard URL
    assert response.url == '/admin/'    
    
    
    
@pytest.mark.django_db
def test_login_fails_with_wrong_password(client):
    # Test that login fails when incorrect password is provided
    # Create a test user
    User.objects.create_user(username='newuser', password='password123')

    # Attempt login with wrong password
    url = reverse('login')
    response = client.post(url, {
        'username': 'newuser',
        'password': 'wrongpassword',
    })

    # Assert response status code 200 (login form re-rendered)
    assert response.status_code == 200
    # Assert error message about incorrect credentials is present in response content
    assert b"Please enter a correct username and password" in response.content
       
# Test that accessing user dashboard requires login
@pytest.mark.django_db
def test_user_dashboard_requires_login(client):
    # Access user dashboard URL without logging in
    url = reverse('user-dashboard')
    response = client.get(url)
    # Should redirect to login (302)
    assert response.status_code == 302

# Test that accessing admin dashboard requires staff privileges
@pytest.mark.django_db
def test_admin_dashboard_requires_staff(client):
    # Create a regular user (not staff)
    user = User.objects.create_user(
        username='user',
        password='pass',
        email='test@test.com',
    )
    # Log in as the regular user
    client.login(username='user', password='pass')

    # Access admin dashboard URL
    url = reverse('admin-dashboard')
    response = client.get(url)
    # Should either redirect to login (302) or return 403 Forbidden
    assert response.status_code in (302, 403) # Either redirect or forbidden