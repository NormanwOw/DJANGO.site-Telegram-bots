from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, reverse, render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView
from django.http import HttpResponse, JsonResponse

from app.settings import DEBUG
from logger import Logger
from main.application.services.commands.delete_order import DeleteOrder
from main.application.services.commands.get_orders import GetOrders
from main.exceptions import OrderNotFoundException
from shared.infrastructure.uow import UnitOfWork, TestUnitOfWork
from users.application.command.auth_user import AuthUser
from users.application.command.delete_user import DeleteUser
from users.forms import LoginForm, RegistrationForm, ProfileForm
from users.models import UserModel


class AuthLoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    auth = auth
    auth_user_command = AuthUser()

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        self.auth_user_command(auth, self.request, username, password)
        return JsonResponse({'status': 'ok'}, status=200)

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)


class AuthRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('main:home')
    auth = auth
    auth_user_command = AuthUser()

    def form_valid(self, form):
        super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        self.auth_user_command(auth, self.request, username, password)
        return JsonResponse({'status': 'ok'}, status=200)

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = ProfileForm
    template_name = 'users/profile.html'
    logger = Logger()
    get_orders_command = GetOrders(logger)
    delete_user_command = DeleteUser(logger)
    delete_order_command = DeleteOrder(logger)
    uow = UnitOfWork() if not DEBUG else TestUnitOfWork()

    def form_valid(self, form, **kwargs):
        form.save()
        return JsonResponse({'message': 'Данные успешно изменены'}, status=200)

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        return JsonResponse({'errors': errors}, status=400)

    def get(self, request, *args, **kwargs):
        if kwargs['pk'] != str(self.request.user.pk):
            return HttpResponse(status=404)

        remove_order_id = request.GET.get('remove-order')
        if remove_order_id:
            try:
                self.delete_order_command(self.uow, self.request.user.pk, int(remove_order_id))
                return redirect('users:profile', pk=request.user.pk)
            except OrderNotFoundException:
                return HttpResponse(status=404)

        if request.GET.get('remove-user'):
            self.delete_user_command(self.uow, self.request.user)
            return redirect('main:home')

        context = {
            'title': 'Профиль',
            'orders': self.get_orders_command(self.uow, self.request.user),
        }
        return render(request, 'users/profile.html', context=context)

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
