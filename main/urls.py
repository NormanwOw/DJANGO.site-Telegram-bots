from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('prices/', views.prices, name='prices'),
    path('new-order/', views.new_order, name='new-order'),
    path('contacts/', views.contacts, name='contacts'),
    path('accept/', views.accept, name='accept')
]
