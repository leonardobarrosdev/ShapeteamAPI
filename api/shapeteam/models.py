from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

def upload_photos(instance, filename):
    path = f'photos/{instance.name}'
    extension = filename.split('.')[-1]
    if extension:
        path = path + '.' + extension
    return path

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
        verbose_name = _("Day Training")
        verbose_name_plural = _("Day Trainings")


class DayExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField()
    sets = models.IntegerField()
    duration = models.DurationField()

    class Meta:
        verbose_name = _("Day Exercise")
        verbose_name_plural = _("Day Exercises")


class WeekRoutine(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    monday = models.ManyToManyField(DayTraining, related_name='monday_routine', blank=True)
    tuesday = models.ManyToManyField(DayTraining, related_name='tuesday_routine', blank=True)
    wednesday = models.ManyToManyField(DayTraining, related_name='wednesday_routine', blank=True)
    thursday = models.ManyToManyField(DayTraining, related_name='thursday_routine', blank=True)
    friday = models.ManyToManyField(DayTraining, related_name='friday_routine', blank=True)
    saturday = models.ManyToManyField(DayTraining, related_name='saturday_routine', blank=True)
    sunday = models.ManyToManyField(DayTraining, related_name='sunday_routine', blank=True)
    
    class Meta:
        verbose_name = _("Week Routine")
        verbose_name_plural = _("Week Routines")


class ExerciseRanking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    score = models.IntegerField()
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Exercise Ranking")
        verbose_name_plural = _("Exercise Rankings")


class Gym(models.Model):
    name = models.CharField(max_length=120) 
    location = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Gym")
        verbose_name_plural = _("Gyms")


class Connection(models.Model):
	sender = models.ForeignKey(
		User,
		related_name='sent_connections',
		on_delete=models.CASCADE
	)
	receiver = models.ForeignKey(
		User,
		related_name='received_connections',
		on_delete=models.CASCADE
	)
	accepted = models.BooleanField(default=False)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username + ' -> ' + self.receiver.username


class Level(models.Model):
    name = models.CharField(max_length=60, default='Basic')
    description = models.TextField(null=True, blank=True)


class Goal(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)

