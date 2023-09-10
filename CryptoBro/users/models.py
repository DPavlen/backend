from django.contrib.auth.models import AbstractUser
from django.db import models

# from users.validators import UsernameValidatorRegex 



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    is_answered = models.BooleanField(default=False)


class User(AbstractUser):
    """Модель переопределенного юзера."""
    class RoleChoises(models.TextChoices):
        """Выбор роли у юзера."""
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    username = models.CharField(
        'Имя пользователя',
        # validators=(UsernameValidatorRegex()),
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(
        blank=True,
        max_length=254,
        unique=True,
        verbose_name="email address",
    )
    role = models.CharField(
        verbose_name="Пользовательская роль",
        # Определение полей из класса RoleChoises
        choices=RoleChoises.choices,
        default=RoleChoises.USER,
        max_length=50,
    )
    bio = models.TextField("Биография", null=True)
    confirmation_code = models.CharField(
        "Код подтверждения пользователя",
        max_length=100, null=True
    )

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELDS = "email"

    @property
    def is_admin(self):
        return self.role == User.RoleChoises.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.RoleChoises.MODERATOR

    @property
    def is_user(self):
        return self.role == User.RoleChoises.USER

    class Meta(AbstractUser.Meta):
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-id"]


    def __str__(self):
        return str(self.username)