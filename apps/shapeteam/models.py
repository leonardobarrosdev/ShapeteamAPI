from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum, Avg
from django.core.validators import MinValueValidator, MaxValueValidator
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


class WeekRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(db_default=get_current_date())
    
    class Meta:
        verbose_name = _("Week Routine")
        verbose_name_plural = _("Week Routines")


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
    week_routine = models.ForeignKey(WeekRoutine, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Day Training")
        verbose_name_plural = _("Day Trainings")


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


class UserPerformanceMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    muscle_group = models.ForeignKey('MuscleGroup', on_delete=models.CASCADE)
    total_volume = models.IntegerField(default=0)
    frequency = models.IntegerField(default=0)
    completion_rate = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    streak = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'muscle_group']
        indexes = [
            models.Index(fields=['user', 'muscle_group']),
            models.Index(fields=['updated_at'])
        ]

    def update_metrics(self):
        # Calculate total volume from exercises
        exercises = Exercise.objects.filter(
            weekroutine__user=self.user,
            muscle_group=self.muscle_group,
            finished=True
        )
        self.total_volume = exercises.aggregate(
            total=Sum(models.F('repetition') * models.F('section'))
        )['total'] or 0
        # Calculate weekly frequency
        week_start = timezone.now() - timezone.timedelta(days=7)
        self.frequency = DayTraining.objects.filter(
            weekroutine__user=self.user,
            muscle_group=self.muscle_group,
            weekroutine__created_at__gte=week_start
        ).count()
        # Calculate completion rate
        total_exercises = Exercise.objects.filter(
            weekroutine__user=self.user,
            muscle_group=self.muscle_group
        ).count()
        completed = exercises.count()
        self.completion_rate = (completed / total_exercises * 100) if total_exercises > 0 else 0
        # Update streak
        self.update_streak()
        self.save()

    def update_streak(self):
        current_date = timezone.now().date()
        last_exercise = Exercise.objects.filter(
            weekroutine__user=self.user,
            finished=True
        ).order_by('-weekroutine__created_at').first()
        if not last_exercise:
            self.streak = 0
            return
        last_date = last_exercise.weekroutine.created_at
        if (current_date - last_date).days <= 1:
            self.streak += 1
        else:
            self.streak = 0


class Achievement(models.Model):
    TYPES = [
        ('VOLUME', 'Total Volume'),
        ('STREAK', 'Training Streak'),
        ('FREQUENCY', 'Weekly Frequency'),
        ('MUSCLE', 'Muscle Group Mastery')
    ]
    LEVELS = [
        ('BRONZE', 'Bronze'),
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPES)
    level = models.CharField(max_length=10, choices=LEVELS)
    muscle_group = models.ForeignKey('MuscleGroup', null=True, on_delete=models.CASCADE)
    value = models.IntegerField()
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'type', 'muscle_group']),
            models.Index(fields=['achieved_at'])
        ]

    @classmethod
    def check_achievements(cls, user, performance_metrics):
        # Volume achievements
        volume_thresholds = {
            'BRONZE': 1000,
            'SILVER': 5000,
            'GOLD': 10000,
            'PLATINUM': 50000
        }
        
        for level, threshold in volume_thresholds.items():
            if performance_metrics.total_volume >= threshold:
                cls.objects.get_or_create(
                    user=user,
                    type='VOLUME',
                    level=level,
                    muscle_group=performance_metrics.muscle_group,
                    value=threshold
                )

        # Streak achievements
        streak_thresholds = {
            'BRONZE': 7,
            'SILVER': 30,
            'GOLD': 90,
            'PLATINUM': 180
        }
        
        for level, threshold in streak_thresholds.items():
            if performance_metrics.streak >= threshold:
                cls.objects.get_or_create(
                    user=user,
                    type='STREAK',
                    level=level,
                    value=threshold
                )

        # Frequency achievements
        frequency_thresholds = {
            'BRONZE': 2,
            'SILVER': 3,
            'GOLD': 4,
            'PLATINUM': 5
        }
        
        for level, threshold in frequency_thresholds.items():
            if performance_metrics.frequency >= threshold:
                cls.objects.get_or_create(
                    user=user,
                    type='FREQUENCY',
                    muscle_group=performance_metrics.muscle_group,
                    level=level,
                    value=threshold
                )


class UserRanking:
    @staticmethod
    def calculate_overall_score(user):
        performances = UserPerformanceMetrics.objects.filter(user=user)
        achievements = Achievement.objects.filter(user=user)
        # Base score from performance metrics
        score = sum([
            (p.total_volume * 0.4) +  # 40% weight for volume
            (p.streak * 100) +        # Points per day of streak
            (p.frequency * 200) +     # Points per weekly workout
            (p.completion_rate * 10)  # Points for completion rate
            for p in performances
        ])
        # Additional points from achievements
        achievement_points = {
            'BRONZE': 1000,
            'SILVER': 2500,
            'GOLD': 5000,
            'PLATINUM': 10000
        }
        score += sum([achievement_points[a.level] for a in achievements])
        return score


class ExerciseRanking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Exercise Ranking")
        verbose_name_plural = _("Exercise Rankings")

    def update(self):
        self.score = UserRanking.calculate_overall_score(self.user)
        self.updated_at = datetime.now()
        self.save()


class Gym(models.Model):
    name = models.CharField(max_length=120)
    location = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Gym")
        verbose_name_plural = _("Gyms")


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)