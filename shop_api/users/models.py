from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    REGISTRATION_CHOICES = (
        ('local', 'Локальная регистрация'),
        ('google', 'Google OAuth'),
    )

    email = models.EmailField(unique=True)
    phone_number =models.CharField(max_length=20 ,blank=True , null=True)
    birthdate = models.DateField(blank=True , null=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    registration_source = models.CharField(max_length=20, choices=REGISTRATION_CHOICES, default='local')
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "birthdate"]

    def __str__(self):
        return self.email or ''


class ConfirmationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Код подтверждения для {self.user.email}"