from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):  # Inherit from BaseUserManager
    def active_users(self):
        return self.filter(is_active=True)

    def public_users(self):
        return self.filter(public_visibility=True)

    # You can add other custom methods if needed
