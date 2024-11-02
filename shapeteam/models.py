from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.conf import settings
from django.utils import timezone

def upload_thumbnail(instance, filename):
	path = f'thumbnails/{instance.username}'
	extension = filename.split('.')[-1]
	if extension:
		path = path + '.' + extension
	return path

def upload_photos(instance, filename):
	path = f'photos/{instance.name}'
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
    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female'),
        (3, 'other')
    )
    username = models.CharField(max_length=30, default="name")
    thumbnail = models.ImageField(upload_to=upload_thumbnail,null=True,blank=True)
    email = models.EmailField(max_length=254, unique=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender']

    objects = UserManager()

    def __str__(self):
        return f"{self.email} - {self.username}"


class Connection(models.Model):
	sender = models.ForeignKey(
		CustomUser,
		related_name='sent_connections',
		on_delete=models.CASCADE
	)
	receiver = models.ForeignKey(
		CustomUser,
		related_name='received_connections',
		on_delete=models.CASCADE
	)
	accepted = models.BooleanField(default=False)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username + ' -> ' + self.receiver.username

   
class NameExercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    muscle_group = models.CharField(max_length=50, default="muscle_group")
    photo = models.ImageField(upload_to=upload_photos, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Exercise(models.Model):
    name_exe = models.ForeignKey(NameExercise, related_name='exercises', on_delete=models.CASCADE)   
    default_reps = models.IntegerField()
    default_sets = models.IntegerField()


class DayTraining(models.Model):
    routine = models.ForeignKey('WeekRoutine', on_delete=models.CASCADE)
    weekday = models.CharField(max_length=120, default='monday')
    exercises = models.ManyToManyField(Exercise)
    
    class Meta:
        verbose_name = "Day Training"
        verbose_name_plural = "Day Trainings"


class DayExercise(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField()
    sets = models.IntegerField()
    duration = models.DurationField()

    class Meta:
        verbose_name = "Day Exercise"
        verbose_name_plural = "Day Exercises"


class WeekRoutine(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    monday = models.ManyToManyField(DayTraining, related_name='monday_routine', blank=True)
    tuesday = models.ManyToManyField(DayTraining, related_name='tuesday_routine', blank=True)
    wednesday = models.ManyToManyField(DayTraining, related_name='wednesday_routine', blank=True)
    thursday = models.ManyToManyField(DayTraining, related_name='thursday_routine', blank=True)
    friday = models.ManyToManyField(DayTraining, related_name='friday_routine', blank=True)
    saturday = models.ManyToManyField(DayTraining, related_name='saturday_routine', blank=True)
    sunday = models.ManyToManyField(DayTraining, related_name='sunday_routine', blank=True)
    
    class Meta:
        verbose_name = "Week Routine"
        verbose_name_plural = "Week Routines"
        

class Chat(models.Model):
	connection = models.ForeignKey(Connection,related_name='messages',on_delete=models.CASCADE)
	user = models.ForeignKey(CustomUser,related_name='my_messages',on_delete=models.CASCADE)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username + ': ' + self.text


class ExerciseRanking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    score = models.IntegerField()
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Exercise Ranking"
        verbose_name_plural = "Exercise Rankings"


class Gym(models.Model):
    name = models.CharField(max_length=120) 
    location = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Gym"
        verbose_name_plural = "Gyms"
