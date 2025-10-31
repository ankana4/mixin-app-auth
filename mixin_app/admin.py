from django.contrib import admin
from mixin_app.models import User


class Admin(admin.ModelAdmin):
    fields=['username', 'email', 'phone_no', 'password', 'address', 'created_at', 'updated_at']