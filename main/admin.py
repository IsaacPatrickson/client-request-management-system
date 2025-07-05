from django.contrib import admin
from .models import Client, RequestType, ClientRequest
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.admin import AdminSite
from .decorators import staff_member_required_403
from django.utils import timezone

# Custom AdminSite subclass to override permission checks and caching behavior
class CustomAdminSite(AdminSite):
    # Override admin_view to apply custom access control and caching rules
    def admin_view(self, view, cacheable=False):
        # Wrap the original admin view with a custom decorator that restricts access
        # to staff members, returning HTTP 403 if unauthorized
        view = staff_member_required_403(view)
        # If the view should not be cached, wraps it with Django's never_cache decorator
        # to prevent browsers and proxies from caching sensitive admin pages
        if not cacheable:
            from django.views.decorators.cache import never_cache
            view = never_cache(view)
        # Return the decorated view function
        return view

# Instantiate the custom admin site; models will be registered on this instead of default admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Inline admin for editing ClientRequest directly on the Client admin page
class ClientRequestInline(admin.TabularInline):
    model = ClientRequest
    extra = 1  # Number of extra blank forms to show
    fields = ('request_type', 'status', 'description', 'created_at')  # Fields shown in inline
    readonly_fields = ('created_at',)  # created_at is read-only
    show_change_link = True  # Show link to edit full ClientRequest object
       

# Register Client table(model) with custom admin options
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'contact_number', 'company_url', 'created_at', 'is_active')  # Columns in list view
    search_fields = ('name', 'email', 'contact_number', 'company_url')  # Searchable fields
    list_filter = ('is_active', 'created_at')  # Filters on sidebar
    readonly_fields = ('created_at',)  # created_at cannot be edited
    ordering = ('-created_at',)  # Default ordering: newest first
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'contact_number', 'company_url', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),  # Collapsible fieldset in admin UI
        }),
    )
    
    inlines = [ClientRequestInline]  # Include the ClientRequest inline admin on Client detail page

# Register Client model with custom admin site and ClientAdmin options
custom_admin_site.register(Client, ClientAdmin)

# Admin customization for RequestType model
class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',)  # Name is editable in main section
        }),
        ('Description', {
            'fields': ('description',),  # Description in collapsible section
            'classes': ('collapse',),
        }),
    )
    
# Register RequestType with the custom admin site
custom_admin_site.register(RequestType, RequestTypeAdmin)

# Factory function to create admin actions to update status of ClientRequest
def make_status_action(status_value):
    def action(modeladmin, request, queryset):
        now = timezone.now()
        # Update selected ClientRequest objects with new status and updated timestamp
        updated_count = queryset.update(status=status_value, updated_at=now)
        # Show message to user confirming how many were updated
        modeladmin.message_user(request, f'{updated_count} requests marked as {status_value}.')
    # Set the function name and description for display in admin UI
    action.__name__ = f'mark_as_{status_value.lower().replace(" ", "_")}'
    action.short_description = f'Mark selected requests as {status_value}'
    return action


# Admin customization for ClientRequest model
class ClientRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'request_type_name', 'status', 'description','created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__name', 'request_type__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('client', 'request_type', 'status')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Define admin actions using the status update factory function
    actions = [
        make_status_action('Pending'),
        make_status_action('In Progress'),
        make_status_action('Completed'),
    ]
    
    # Display client name in list view by accessing related object
    def client_name(self, obj):
        return obj.client.name
    client_name.short_description = 'Client'
    
    # Display request type name similarly
    def request_type_name(self, obj):
        return obj.request_type.name
    request_type_name.short_description = 'Request Type'
    
# Register ClientRequest model with the custom admin site
custom_admin_site.register(ClientRequest, ClientRequestAdmin)

# Custom User admin: extending Django's default UserAdmin without modifications here
class UsersAdmin(DefaultUserAdmin):
    # Inherit Django's built-in UserAdmin to get all user admin features.
    pass

# Register User model with the custom admin site using the default UserAdmin
custom_admin_site.register(User, UsersAdmin)
