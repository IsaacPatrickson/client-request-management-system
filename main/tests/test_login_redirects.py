import pytest

@pytest.mark.django_db
def test_admin_login_redirects_to_custom_login(client):
    response = client.get('/admin/login/')
    assert response.status_code == 302
    assert response.url == '/login/'

@pytest.mark.django_db
def test_admin_login_redirect_preserves_next_for_admin(client):
    response = client.get('/admin/login/?next=/admin/')
    assert response.status_code == 302
    assert response.url == '/login/'

@pytest.mark.django_db
def test_admin_login_strips_irrelevant_next_param(client):
    response = client.get('/admin/login/?next=/admin/dashboard')
    assert response.status_code == 302
    assert response.url == '/login/'
