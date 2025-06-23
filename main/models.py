from django.db import models
from django.utils import timezone


# Define the Client model to store client information
class Client(models.Model):
    name = models.CharField(max_length=255) # Client's name (required)
    email = models.EmailField(blank=True, null=True) # Optional email address
    contact_number = models.CharField(max_length=20, blank=True, null=True) # Optional phone number
    company_url = models.URLField(blank=True, null=True) # Optional company website URL
    created_at = models.DateTimeField(default=timezone.now) # Timestamp when client was created
    is_active = models.BooleanField(default=True) # Flag to indicate if client is active

    def __str__(self):
        # String representation for easy identification in admin or logs
        return f'{self.id} | {self.name} | {self.company_url} | {self.is_active}'

# Define the RequestType model to categorize different types of client requests
class RequestType(models.Model):
    name = models.CharField(max_length=255) # Name of the request type
    description = models.TextField(blank=True, null=True) # Optional detailed description

    def __str__(self):
        return f'{self.id} | {self.name}'

# Define the ClientRequest model representing a request made by a client
class ClientRequest(models.Model):
    # Status choices for tracking progress of the request
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE) # Link to the client who made the request; cascade deletes
    request_type = models.ForeignKey(RequestType, on_delete=models.CASCADE) # Type/category of request
    description = models.TextField(blank=True, null=True) # Optional detailed description of the request
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True) # Current status of the request
    created_at = models.DateTimeField(default=timezone.now) # Timestamp when request was created
    updated_at = models.DateTimeField(auto_now=True) # Timestamp when request was last updated

    def __str__(self):
        return f'{self.id} | {self.client.name} | {self.request_type.name} | {self.status} | {self.updated_at}'