import pytest
from django.urls import reverse
from django.contrib.auth.models import User


# Tests cover login flow:
# - redirect for regular, staff, superuser users
# - login failure
# - access control for dashboards (authorized/unauthorized)

@pytest.mark.django_db
def test_user_without_is_staff_login_redirects_to_account_disabled_message(client):
    # Creates a non-staff user and tests that logging in redirects to the account disabled page
    # Simulates a user whose is_staff flag is False, which should result in immediate logout and redirect
    User.objects.create_user(username='newuser', password='password123', is_staff=False)
    url = reverse('login')
    response = client.post(url, {
        'username': 'newuser',
        'password': 'password123',
    })
    assert response.status_code == 302
    assert response.url == reverse('account_disabled')

@pytest.mark.django_db
def test_is_staff_user_login_redirects_to_admin_dashboard(client):
    # Creates a staff user and tests that logging in redirects to the Django admin dashboard
    User.objects.create_user(username='adminuser', password='adminpass123', is_staff=True)
    url = reverse('login')
    response = client.post(url, {
        'username': 'adminuser',
        'password': 'adminpass123',
    })
    assert response.status_code == 302
    assert response.url == reverse('custom_admin:index')

@pytest.mark.django_db
def test_superuser_login_redirects_to_admin_dashboard(client):
    # Creates a superuser and tests that logging in redirects to the Django admin dashboard
    User.objects.create_superuser(username='superuser', password='superpass123')
    url = reverse('login')
    response = client.post(url, {
        'username': 'superuser',
        'password': 'superpass123',
    })
    assert response.status_code == 302
    assert response.url == reverse('custom_admin:index')

@pytest.mark.django_db
def test_login_fails_with_wrong_password(client):
    # Creates a valid user and tests that login fails with incorrect password
    # Expects the login page to reload with an error message in the response content
    User.objects.create_user(username='newuser', password='password123', is_staff=True)
    url = reverse('login')
    response = client.post(url, {
        'username': 'newuser',
        'password': 'wrongpassword',
    })
    assert response.status_code == 200
    assert b"Please enter a correct username and password" in response.content

@pytest.mark.django_db
@pytest.mark.parametrize("page", ['home', 'register', 'login'])
def test_authenticated_user_redirects_to_admin(client, django_user_model, page):
    # Tests that authenticated users are redirected from login, register, and home pages to admin dashboard
    user = django_user_model.objects.create_user(username='testuser', password='pass', is_staff=True)
    client.force_login(user)

    url = reverse(page)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('custom_admin:index')