from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView

from main.views import page_not_found
from users.forms import LoginForm, RegistrationForm, ProfileForm
from users.models import User


class AuthLoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('main:home')
    extra_context = {'title': 'Авторизация'}

    def form_valid(self, form):
        valid = super().form_valid(form)
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(self.request, user)

        return valid


class AuthRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('main:home')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        valid = super().form_valid(form)
        new_user = auth.authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        auth.login(self.request, new_user)

        return valid


class UserProfileView(UpdateView, LoginRequiredMixin):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль'}

    def form_valid(self, form, **kwargs):
        messages.success(self.request, 'Данные успешно изменены')

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if kwargs['pk'] != str(self.request.user.pk):
            return page_not_found(request, 'page404.html')

        if request.GET.get('remove-user'):
            self.request.user.delete()
            return redirect('main:home')

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.pk})


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:home'))


class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:password-change-done')
    template_name = 'users/password-change-form.html'
