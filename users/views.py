from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from users.forms import LoginForm, RegistrationForm, ProfileForm



class AuthLogin(FormView):
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


class AuthRegistration(CreateView):
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


@login_required
def profile(request):
    msg = ''
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        user_data = {request.user.email, request.user.first_name, request.user.last_name}

        if form.is_valid():
            del form.cleaned_data['password']
            if set(form.cleaned_data.values()) != user_data:
                form.save()
                msg = 'Данные успешно изменены'
    else:
        form = ProfileForm(instance=request.user)

    if request.GET.get('remove-user', False):
        request.user.delete()

        return redirect(reverse('main:home'))

    context = {
        'title': 'Профиль',
        'message': msg,
        'form': form
    }
    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:home'))


class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:password-change-done')
    template_name = 'users/password-change-form.html'
