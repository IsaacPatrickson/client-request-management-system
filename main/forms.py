from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group


class UserRegistrationForm (forms.ModelForm):
    # Explicitly declared fields usually display before the fields defined in class Meta
    username = forms.CharField(
        required=True,
        min_length=5,
        max_length=20,
        help_text='Enter a username between 5-20 characters.',
        widget=forms.TextInput(attrs={
            'autocomplete': 'username',
            'class': 'form-control',
        })
    )
    
    email = forms.EmailField(
        required=True,
        help_text='Enter a valid email address.',
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={          # Rendered as a password input (masked)
            'autocomplete': 'new-password',
            'class': 'form-control',
        }),
        required=True,                              # Mandatory field
        min_length=12,                              # Enforce minimum length of 12 characters
        help_text='Password required. Must be at least 12 characters.'
    )

    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={          # Confirm password field, also masked
            'autocomplete': 'new-password',         
            'class': 'form-control',
        }),
        label='Confirm Password',                   # Label override
        required=True                               # Mandatory field
    )
    
    class Meta:
        model = User                    # Link to Django's built-in User model
        fields = ['username', 'email']  # Only expose these model fields in the form
        
    # Specify order of fields in the rendered form
    field_order = ['username', 'email', 'password', 'password_confirm']
        
    def clean(self):
        # Override the default clean method to add custom validation logic
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Validate that password and confirmation match
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Passwords do not match')
        return cleaned_data
    
    def save(self, commit=True):
        # Override save to set password properly and assign group
        user = super().save(commit=False)                   # Create User instance without saving to DB yet
        user.set_password(self.cleaned_data['password'])    # Hash and set password securely
        user.is_staff = True                                # Automatically assign staff status to new users
        if commit:
            user.save() # Save user to the database
            try:
                # Attempt to add user to the 'LimitedUsers' group if it exists
                limited_group = Group.objects.get(name='LimitedUsers')
                user.groups.add(limited_group)
            except Group.DoesNotExist:
                # If group doesn't exist, silently ignore
                pass
        return user