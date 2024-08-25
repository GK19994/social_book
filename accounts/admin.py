from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    # Specify the fields to display in the user form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('public_visibility', 'birth_year', 'address')}),
    )

# Register your custom user model with the customized admin
admin.site.register(CustomUser, CustomUserAdmin)