from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .forms import UserRegistrationForm


# Home view
class HomeView(TemplateView):
    template_name = 'home.html'

# # Registration form view
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    
# Custom login view with role-based redirect logic
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        # First, check if there's a 'next' parameter (automatically handled by get_redirect_url)
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to
        
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse('admin:index')
        return reverse_lazy('user-dashboard')

# Regular user dashboard (must be logged in)
@login_required
def user_dashboard_view(request):
    return render(request, 'dashboards/user_dashboard.html')

# Admin dashboard (must be logged in + is_staff)
@user_passes_test(lambda u: u.is_staff)
@login_required
def admin_dashboard_view(request):
    return render(request, 'dashboards/admin_dashboard.html')