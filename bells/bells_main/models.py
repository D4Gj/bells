from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models

STATUS_CHOICES = (
    ("PENDING", "Ожидание"),
    ("REJECTED", "Отклонён"),
    ("APPROVED", "Одобрено"),
)
STATUS_BELL = (
    ("READY_TO_TRANSFER", "Готов к передаче"),
    ("IN_REQUEST_FOR_APPROVAL", "В заявке на согласование"),
    ("IN_USE", "Используется"),
    ("BELL_MISSING", "Не хватает колокола"),
)


class Temple(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    address = models.CharField(max_length=200, verbose_name="Адрес")

    class Meta:
        verbose_name = "Храм"
        verbose_name_plural = "Храмы"

    def __str__(self):
        return self.name


class Belltower(models.Model):
    temple = models.OneToOneField(Temple, on_delete=models.CASCADE, primary_key=True, verbose_name="Церковь")
    belltower_name = models.CharField(max_length=100, verbose_name="Название колокольни")

    class Meta:
        verbose_name = "Колокольня"
        verbose_name_plural = "Колокольни"

    def __str__(self):
        return self.belltower_name


class Bell(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    weight = models.FloatField(verbose_name="Вес")
    manufacturer = models.CharField(max_length=100, verbose_name="Производитель")
    audio_file = models.FileField(upload_to="media/bell_sounds/%Y/%m/%d/", default=None, blank=True, verbose_name="Аудио файл")
    status = models.CharField(max_length=50, choices=STATUS_BELL, default="PENDING", verbose_name="Статус")
    image = models.ImageField(upload_to="media/bell_images/%Y/%m/%d/", default=None, blank=True, verbose_name="Картинка")
    belltower = models.ForeignKey(
        Belltower, on_delete=models.CASCADE, related_name="bells", verbose_name="Колоколня"
    )

    class Meta:
        verbose_name = "Колокол"
        verbose_name_plural = "Колоколы"

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, phone_number, user_type, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, phone_number=phone_number, user_type=user_type, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, phone_number, user_type, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email, phone_number, user_type, password, **extra_fields
        )


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Админ"),
        ("church_operator", "Оператор храма"),
        ("moderator", "Moderator"),
    )

    email = models.EmailField(unique=True, verbose_name="Эл. почта")
    phone_number = models.CharField(max_length=15, unique=False, verbose_name="Номер телефона")
    user_type = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=False, verbose_name="Роль пользователя")
    is_key_keeper = models.BooleanField(default=False, verbose_name="Хранитель ключа")
    is_bell_ringer = models.BooleanField(default=False, verbose_name="Звонитель")

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "user_type"]

    def __str__(self):
        return self.email


class BellMovementRequest(models.Model):
    requester = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="requested_bell_movements",
    )
    reason = models.TextField()
    bell = models.ForeignKey(Bell, on_delete=models.CASCADE, default=None)
    temple_from = models.ForeignKey(
        Temple,
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Храм откуда передаём",
        related_name="bell_movement_requests_from",
    )
    temple_to = models.ForeignKey(
        Temple,
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Храм куда передаём",
        related_name="bell_movement_requests_to",
    )
    belltowerfrom = models.ForeignKey(
        Belltower,
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Колокольня откуда",
        related_name="bell_movement_tower_from",
    )
    belltowerto = models.ForeignKey(
        Belltower,
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Колокольня куда",
        related_name="bell_movement_tower_to",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Перемещение колокола"
        verbose_name_plural = "Перемещение колоколов"

    def __str__(self):
        return f"Обращение от{self.requester.get_full_name()} для {self.bell}"
