from datetime import date
import uuid
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError


# For testing model validation
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10mb

def file_validation(file):
    """
    For regular upload, we get UploadedFile instance, so we can validate it.
    When using direct upload from the browser, here we get an instance of the CloudinaryResource
    and file is already uploaded to Cloudinary.
    Still can perform all kinds on validations and maybe delete file, approve moderation, perform analysis, etc.
    """
    if not file:
        raise ValidationError("No file selected.")
    if isinstance(file, UploadedFile):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 10MB.")

def upload_thumbnail(instance, filename):
    path = f'thumbnails/{instance.username}'
    extension = filename.split('.')[-1]
    if extension:
        path = path + '.' + extension
    return path

def username_generator(instance):
    username = f"{instance.first_name}{str(uuid.uuid4().int)[:4]}"
    if len(username) > 30:
        username = username[:26] + str(uuid.uuid4().int)[:4]
    return username


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


class Goal(models.Model):
    GOALS = (
        (1, 'Hipertrofia Muscular '),
        (2, 'Perda de Peso '),
        (3, 'Definição Muscular '),
        (4, 'Ganho de Resistência'),
        (5, 'Aumento de Força '),
        (6, 'Saúde e Bem-estar '),
        (7, 'Melhora da Mobilidade e Flexibilidade '),
        (8, 'Reabilitação Física '),
        (9, 'Condicionamento Esportivo'),
    )
    name = models.SmallIntegerField(choices=GOALS, blank=True, null=True)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDERS = ((1, 'male'), (2, 'female'), (3, 'other'))
    LEVELS = ((1, 'basic'), (2, 'medium'), (3, 'advanced'))
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    thumbnail = CloudinaryField(default='profile.png', validators=[file_validation])
    email = models.EmailField(max_length=254, unique=True)
    gender = models.SmallIntegerField(choices=GENDERS, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
    level = models.SmallIntegerField(choices=LEVELS, default=1)
    goal = models.ManyToManyField(Goal)
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
            today = date.today()
            age = today.year - self.date_birth.year - (
                (today.month, today.day) < (self.date_birth.month, self.date_birth.day)
            )
            return age
        return 0

    def get_imc(self):
        if self.height and self.weight:
            imc = self.weight / (self.height ** 2)
            return round(imc)
        return 0.0
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = username_generator(self)
        super().save(*args, **kwargs)
    
    def __unicode__(self):
        """Informative name for model"""
        try:
            public_id = self.thumbnail.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.username, public_id)


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, default='Brazil')
    zipcode = models.IntegerField()
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=200)
    neighborhood = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    number = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.city}, {self.state}, {self.country}'
