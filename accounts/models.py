from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from .managers import CustomUserManager
from django.conf import settings

class CustomUser(AbstractUser):
    public_visibility = models.BooleanField(default=True)
    birth_year = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    @property
    def age(self):
        if self.birth_year:
            return date.today().year - self.birth_year
        return None
    
    objects = CustomUserManager() 
class UploadedFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='uploads/')
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.BooleanField(default=True)  # Public or Private
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_published = models.IntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    