import pytest
from django.contrib.messages import get_messages


# ========================================================
# Test: Successful login shows welcome or success message
# ========================================================
@pytest.mark.django_db  # Enable database access for this test
def test_login_success_message(client, django_user_model):
    # Arrange: create a test user with staff access
    user = django_user_model.objects.create_user(username='isaac', password='test123', is_staff=True)
    
    # Act: submit login form with valid credentials
    response = client.post('/login/', {'username': 'isaac', 'password': 'test123'}, follow=True) # follow redirects so we can capture final response
    
    # Assert: check if any success-related message appears
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any("Welcome" in msg or "successfully logged in" in msg for msg in messages)

# ============================================================
# Test: Successful registration shows confirmation message
# ============================================================
@pytest.mark.django_db
def test_register_success_message(client):
    # Act: post registration form data with matching passwords
    response = client.post('/register/', {
        'username': 'newuser',
        'email': 'test@example.com',
        'password': 'strongpass123',
        'password_confirm': 'strongpass123'
    }, follow=True)  # follow redirect after registration
    
    # Assert: check that a success message was added to messages framework
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any("successfully registered" in msg.lower() for msg in messages)