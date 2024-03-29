from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, reverse, render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView
from django.http import HttpResponse, JsonResponse

from users.forms import LoginForm, RegistrationForm, ProfileForm
from users.models import User


class AuthLoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(self.request, user)

        return JsonResponse({'status': 'ok'}, status=200)

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)


class AuthRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        super().form_valid(form)
        new_user = auth.authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        auth.login(self.request, new_user)

        return JsonResponse({'status': 'ok'}, status=200)

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль'}

    def form_valid(self, form, **kwargs):
        form.save()
        return JsonResponse({'message': 'Данные успешно изменены'}, status=200)

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)

    def get(self, request, *args, **kwargs):
        if kwargs['pk'] != str(self.request.user.pk):
            return HttpResponse(status=404)

        if request.GET.get('remove-user'):
            self.request.user.delete()
            return redirect('main:home')

        return render(request, 'users/profile.html')

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.pk})


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:home'))


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/password-change-form.html'

    def form_valid(self, form, **kwargs):
        form.save()
        return JsonResponse({'status': 'ok'}, status=200)

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password-reset-form.html'
    email_template_name = 'users/password-reset-email.html'
    html_email_template_name = 'users/password-reset-email.html'
    success_url = reverse_lazy('users:password-reset-done')

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)

        return JsonResponse({'status': 'ok'}, status=200)
