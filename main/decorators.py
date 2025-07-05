from django.core.exceptions import PermissionDenied
from functools import wraps

# staff_member_required_403 decorator ensures:
# - Only authenticated staff users can access the admin views
# - Unauthenticated users get redirected to login
# - Authenticated non-staff users get HTTP 403 Forbidden instead of redirect
def staff_member_required_403(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not request.user.is_staff:
            raise PermissionDenied  # This sends 403 instead of redirect
        return view_func(request, *args, **kwargs)
    return _wrapped_view
