from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('orders/', views.my_orders, name='orders'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile')
]