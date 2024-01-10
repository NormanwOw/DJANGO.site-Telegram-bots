from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from main.models import Order
from users.forms import LoginForm, RegistrationForm, ProfileForm
from users.models import User


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(reverse('main:home'))
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)

            return redirect(reverse('main:home'))
    else:
        form = RegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)

    if request.GET.get('remove-user', False):
        User.objects.filter(id=request.user.id).delete()
        return redirect(reverse('main:home'))

    context = {
        'title': 'Профиль',
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
