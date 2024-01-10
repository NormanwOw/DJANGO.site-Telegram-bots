from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from users import views
from users.views import UserPasswordChangeView

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('password-reset/',
         PasswordResetView.as_view(
            template_name='users/password-reset-form.html',
            email_template_name='users/password-reset-email.html',
            html_email_template_name='users/password-reset-email.html',
            success_url=reverse_lazy('users:password-reset-done')
         ),
         name='password-reset'),

    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name='users/password-reset-done.html'
         ),
         name='password-reset-done'),

    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
            template_name='users/password-reset-confirm.html',
            success_url=reverse_lazy('users:password-reset-complete')
         ),
         name='password-reset-confirm'),

    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(
             template_name='users/password-reset-complete.html'
         ),
         name='password-reset-complete'),

    path('password-change/',
         UserPasswordChangeView.as_view(
             template_name='users/password-change-form.html'
         ),
         name='password-change'),

    path('password-change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password-change-done.html'
         ),
         name='password-change-done'),
]
