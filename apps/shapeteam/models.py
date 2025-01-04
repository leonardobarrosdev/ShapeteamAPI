from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.user.models import Address


User = get_user_model()

def upload_photos(instance, filename):
    path = f'muscle_groups/{instance.name}.'
    extension = filename.split('.')[-1]
    path += extension if extension else 'webp'
    return path

def upload_image(instance, filename):
    path = f'images/{instance.name}.'
    extension = filename.split('.')[-1]
    path += extension if extension else 'webp'
    return path

def get_current_date():
    return timezone.now().date()


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to=upload_photos, null=True, blank=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_image, null=True, blank=True)
    repetition = models.IntegerField()
    section = models.IntegerField()
    duration = models.DurationField()
    finished = models.BooleanField(default=False)


class DayTraining(models.Model):
    WEEKDAYS = (
        ('sunday', _('sunday')),
        ('monday', _('monday')),
        ('tuesday', _('tuesday')),
        ('wednesday', _('wednesday')),
        ('thursday', _('thursday')),
        ('friday', _('friday')),
        ('saturday', _('saturday'))
    )
    weekday = models.CharField(choices=WEEKDAYS, max_length=9, default='monday')
    muscle_group = models.ManyToManyField(MuscleGroup)
    
    class Meta:
        verbose_name = _("Day Training")
        verbose_name_plural = _("Day Trainings")


class WeekRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days_training = models.ManyToManyField(DayTraining, verbose_name=_("Days training"))
    created_at = models.DateField(db_default=get_current_date())
    
    class Meta:
        verbose_name = _("Week Routine")
        verbose_name_plural = _("Week Routines")


class ExerciseRanking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)
    score = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Exercise Ranking")
        verbose_name_plural = _("Exercise Rankings")


class Gym(models.Model):
    name = models.CharField(max_length=120) 
    location = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Gym")
        verbose_name_plural = _("Gyms")


class Connection(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    accepted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = ' pendding '
        if self.accepted == True:
            status = ' is patner of '
        return self.sender.first_name + status + self.receiver.first_name


class Goal(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)

