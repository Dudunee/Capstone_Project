from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultAdmin
from .models import User
class UserAdmin(DefaultAdmin):
    list_display = ('email', 'username')

admin.site.register(User, UserAdmin)