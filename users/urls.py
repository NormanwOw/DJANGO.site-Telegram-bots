from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('orders/', views.my_orders, name='orders'),
]