from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('main.urls', namespace='main')),
    path('users/', include('users.urls', namespace='users'))
]

handler404 = views.page_not_found
