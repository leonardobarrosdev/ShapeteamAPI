from datetime import datetime

from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


def upload_thumbnail(instance, filename):
    path = f'thumbnails/{instance.username}'
    extension = filename.split('.')[-1]
    if extension:
        path = path + '.' + extension
    return path


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDERS = ((1, 'male'), (2, 'female'), (3, 'other'))
    LEVELS = ((1, 'basic'), (2, 'medium'), (3, 'advanced'))
    username = models.CharField(max_length=30, default="name")
    first_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=upload_thumbnail, default='profile.png')
    email = models.EmailField(max_length=254, unique=True)
    gender = models.SmallIntegerField(choices=GENDERS, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
    level = models.SmallIntegerField(choices=LEVELS, default=1)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_age(self):
        if self.date_birth:
            current_year = int(datetime.strftime(datetime.now(), '%Y'))
            return current_year - self.date_birth.year
        return 0

    def get_imc(self):
        if self.height and self.weight:
            imc = self.weight / (self.height ** 2)
            return round(imc)
        return 0.0


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, null=True, blank=True)
    number = models.PositiveSmallIntegerField(default=0)
    neighborhood = models.CharField(max_length=220, null=True, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()

    def __str__(self):
        return f'{self.city} - {self.state}'
