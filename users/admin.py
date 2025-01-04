from django.contrib import admin

from main.admin import OrderTabularAdmin
from users.models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = 'username', 'first_name', 'last_name', 'email'
    search_fields = 'username', 'first_name', 'last_name', 'email'
    readonly_fields = 'date_joined', 'last_login'
    exclude = ('password',)

    inlines = [OrderTabularAdmin]
