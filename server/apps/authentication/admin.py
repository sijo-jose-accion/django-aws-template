from django.contrib import admin
from .models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'name', 'created_at', 'last_login', 'is_active', 'is_staff')


"""
Register Admin Pages
"""
admin.site.register(Account, AccountAdmin)
