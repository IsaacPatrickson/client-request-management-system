import pytest

# This test confirms the default Django admin login page
# redirects users to the custom login page at '/login/'
@pytest.mark.django_db
def test_admin_login_redirect_variants(client):
    test_urls = [
        '/admin/login/',
        '/admin/login/?next=/admin/',
        '/admin/login/?next=/admin/dashboard'
    ]
    
    for url in test_urls:
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == '/login/'
