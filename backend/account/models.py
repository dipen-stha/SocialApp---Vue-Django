import uuid

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.db import models

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, name, password, email=None, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address")
        try:
            self.normalize_email(email.email)

            user = self.model(email=email, name=name, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

            return user
        except:
            raise ValueError("Use proper email format")


    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('email')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)

    def all(self):
        return self.filter(email__is_verified=True, email__is_blocked=False)


class Email(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=150, null=True, blank=True)
    token_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'

    @property
    def is_expired(self):
        return self.token_created_at < datetime.now()

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=255, unique=True, null=True)
    name = models.CharField(max_length=255, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email.email


class Permissions(models.Model):
    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.display_name}"

class Roles(models.Model):
    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permissions)

    def __str__(self):
        return f"{self.display_name}"

class AdminUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Roles)

    def __str__(self):
        return f"{self.user.name}"


class CustomerUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name}"