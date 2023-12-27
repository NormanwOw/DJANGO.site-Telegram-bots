from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('order-page/', views.order_page, name='order-page'),
    path('about/', views.about, name='about'),
    path('prices/', views.prices, name='prices'),
    path('new-order/', views.new_order, name='new-order'),
    path('contacts/', views.contacts, name='contacts'),
]

handler404 = views.page_not_found
