from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import CustomUser
from .forms import CustomUserCreationForm
from .forms import UserProfileForm, LoginForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class UserProfileEditView(LoginRequiredMixin, DetailView, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'profile_edit.html'
    context_object_name = 'user_profile'

    slug_field = 'username'
    slug_url_kwarg = 'username'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse('profile_edit', kwargs={'username': self.object.username})


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile_detail.html'
    context_object_name = 'user_profile'

    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_profile'] = self.request.user == self.object
        context['can_view_profile'] = (
            self.object.profile_is_public or
            self.request.user == self.object or
            self.request.user.is_staff
        )
        return context

