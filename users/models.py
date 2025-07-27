from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utils.models import TimeStampedModel
from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    class RoleEnum(models.TextChoices):
        ADMIN = 'admin'
        MANAGER = 'manager'
        SALES = 'sales'
        SUPPORT = 'support'
        VIEWER = 'viewer'

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=8, choices=RoleEnum.choices, default=RoleEnum.SALES)
    phone_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']


    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'