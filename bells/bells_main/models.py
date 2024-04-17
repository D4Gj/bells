from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("REJECTED", "Rejected"),
        ("APPROVED", "Approved"),
    )
STATUS_BELL = (
    ("READY_TO_TRANSFER", "Готов к передаче"),
    ("IN_REQUEST_FOR_APPROVAL", "В заявке на согласование"),
    ("IN_USE", "Используется"),
    ("BELL_MISSING", "Не хватает колокола"),
)

class Temple(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    
    class Meta:
        verbose_name="Храм"
        verbose_name_plural = "Храмы"

    def __str__(self):
        return self.name

class Belltower(models.Model):
    temple = models.OneToOneField(Temple, on_delete=models.CASCADE, primary_key=True)
    belltower_name = models.CharField(max_length=100)

    class Meta:
        verbose_name="Колокольня"
        verbose_name_plural = "Колокольни"
    
    def __str__(self):
        return self.belltower_name

class Bell(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    manufacturer = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='bells/')
    status = models.CharField(max_length=50, choices=STATUS_BELL, default="PENDING")
    image = models.ImageField(upload_to='bell_images/')
    belltower = models.ForeignKey(Belltower, on_delete=models.CASCADE, related_name='bells')
    
    class Meta:
        verbose_name="Колокол"
        verbose_name_plural = "Колоколы"
    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, user_type, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, user_type, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone_number, user_type, password, **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('church_operator', 'Church Operator'),
        ('bell_ringer', 'Bell Ringer'),
        ('moderator', 'Moderator'),
    )

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_key_keeper = models.BooleanField(default=False)
    is_bell_ringer = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'user_type']

    def __str__(self):
        return self.email


class BellMovementRequest(models.Model):

    requester = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="requested_bell_movements",
    )
    destination_church = models.CharField(max_length=100)
    reason = models.TextField()
    bell = models.ForeignKey(Bell, on_delete=models.CASCADE, default=None)
    belltower = models.ForeignKey(Belltower, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name="Перемещение колокола"
        verbose_name_plural = "Перемещение колоколов"

    def __str__(self):
        return f"Обращение {self.requester.get_full_name()} к {self.destination_church}"