from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):  # Inherit from BaseUserManager
    def active_users(self):
        return self.filter(is_active=True)

    def public_users(self):
        return self.filter(public_visibility=True)



    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a regular user, allowing email to be optional.
        """
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a superuser, allowing email to be optional.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)