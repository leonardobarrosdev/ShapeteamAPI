from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from apps.shapeteam.models import *
import datetime


PATH = 'apps/shapeteam/fixtures'

class ConnectionTest(TestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/connection_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)

    def test_connection_success(self):
        connection = Connection.objects.create(sender=self.user, receiver=self.user)
        self.assertIsInstance(connection, Connection)
        self.assertEqual(connection.sender, self.user)
        self.assertEqual(connection.receiver, self.user)

    def test_connection_error(self):
        with self.assertRaises(IntegrityError):
            Connection.objects.create(sender=self.user)

    def test_connection_obj_field(self):
        connection = Connection.objects.get(pk=1)
        field_label = connection._meta.get_field('sender').verbose_name
        self.assertEqual(field_label, 'sender')
        self.assertEqual(str(connection), f'{connection.sender.username} -> {connection.receiver.username}')


class NameExerciseTest(TestCase):
    def setUp(self):
        self.name_exercise = NameExercise.objects.create(
            name="Push Up",
            description="A basic push up exercise",
            muscle_group="Chest"
        )

    def test_name_exercise_success(self):
        self.assertIsInstance(self.name_exercise, NameExercise)
        self.assertEqual(self.name_exercise.name, "Push Up")
        self.assertEqual(self.name_exercise.description, "A basic push up exercise")
        self.assertEqual(self.name_exercise.muscle_group, "Chest")
    
    def test_name_exercise_obj_field(self):
        name_exercise = NameExercise.objects.get(pk=1)
        field_label = name_exercise._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
        self.assertEqual(str(name_exercise), "Push Up")

    def test_name_exercise_str(self):
        self.assertEqual(str(self.name_exercise), "Push Up")


class ExerciseTest(TestCase):
    fixtures = [f'{PATH}/name_exercise_fixture.json']

    def setUp(self):
        self.name_exercise = NameExercise.objects.get(pk=1)
        self.exercise = Exercise.objects.create(
            name_exe=self.name_exercise,
            default_reps=10,
            default_sets=3
        )

    def test_exercise_success(self):
        self.assertIsInstance(self.exercise, Exercise)
        self.assertEqual(self.exercise.name_exe, self.name_exercise)
        self.assertEqual(self.exercise.default_reps, 10)
        self.assertEqual(self.exercise.default_sets, 3)
    
    def test_exercise_error(self):
        with self.assertRaises(IntegrityError):
            Exercise.objects.create(default_reps=10, default_sets=3)
    
    def test_exercise_obj_field(self):
        exercise = Exercise.objects.get(pk=1)
        field_label = exercise._meta.get_field('name_exe').verbose_name
        self.assertEqual(field_label, 'name exe')


class GymTest(TestCase):
    def test_gym_success(self):
        gym = Gym.objects.create(name="Fitness Center", location="123 Fitness St")
        self.assertEqual(gym.name, "Fitness Center")
        self.assertEqual(gym.location, "123 Fitness St")
    
    def test_gym_obj_field(self):
        gym = Gym.objects.create(name="Fitness Center", location="123 Fitness St")
        field_label = gym._meta.get_field('name').verbose_name
        field_length = gym._meta.get_field('name').max_length
        self.assertEqual(field_label, 'name')
        self.assertEqual(field_length, 120)


class DayTrainingTest(TestCase):
    fixtures = [
        'apps/user/fixtures/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/day_training_fixture.json',
        f'{PATH}/week_routine_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.week_routine = WeekRoutine.objects.get(pk=1)
        self.day_training = DayTraining.objects.create(
            week_routine=self.week_routine,
            weekday='Monday'
        )
    
    def test_day_training_success(self):
        self.assertIn(self.exercise, self.day_training.exercises.all())
    
    def test_day_training_error(self):
        with self.assertRaises(IntegrityError):
            DayTraining.objects.create()
    
    def test_day_training_obj_field(self):
        day_training = DayTraining.objects.get(pk=1)
        field_label = day_training._meta.get_field('week_routine').verbose_name
        field_length = day_training._meta.get_field('weekday').max_length
        self.assertEqual(field_label, 'week_routine')
        self.assertEqual(field_length, 120)

    def test_day_training_str(self):
        self.assertEqual(str(self.day_training), "Monday")
    
    def test_day_training_muscle_group(self):
        day_training = DayTraining.objects.get(pk=5)
        muscle_group = day_training.muscle_group.all()
        self.assertIn("Glutes", muscle_group.values_list('name', flat=True))


class DayExerciseTest(TestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/name_exercise_fixture.json',
        f'{PATH}/day_exercise_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.exercise = Exercise.objects.get(pk=2)
        self.dt = datetime.timedelta(days =-1, seconds = 68400)
        self.day_exercise = DayExercise.objects.create(
            user=self.user,
            exercise=self.exercise,
            reps=10,
            sets=3,
            duration=self.dt
        )

    def test_day_exercise_success(self):
        self.assertEqual(self.day_exercise.user, self.user)
        self.assertEqual(self.day_exercise.exercise, self.exercise)
        self.assertEqual(self.day_exercise.reps, 10)
        self.assertEqual(self.day_exercise.sets, 3)
        self.assertEqual(self.day_exercise.duration, self.dt)
    
    def test_day_exercise_error(self):
        with self.assertRaises(IntegrityError):
            DayExercise.objects.create(reps=10, sets=3, duration=self.dt)
    
    def test_day_exercise_obj_field(self):
        day_exercise = DayExercise.objects.get(pk=1)
        field_label = day_exercise._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')


class WeekRoutineTest(TestCase):
    fixtures = ['fixtures/user/user_fixture.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.week_routine = WeekRoutine.objects.create(user=self.user)

    def test_week_routine_success(self):
        self.assertEqual(self.week_routine.user, self.user)
    
    def test_week_routine_error(self):
        with self.assertRaises(IntegrityError):
            WeekRoutine.objects.create()
    
    def test_week_routine_obj_field(self):
        field_label = self.week_routine._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
        
    def test_week_routine_days(self):
        self.day_training = DayTraining.objects.create(routine=self.week_routine)
        self.week_routine.monday.add(self.day_training)
        self.assertIn(self.day_training, self.week_routine.monday.all())


class ExerciseRankingTest(TestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/name_exercise_fixture.json',
        f'{PATH}/exercise_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.exercise = Exercise.objects.get(pk=1)
        self.ranking = ExerciseRanking.objects.create(
            user=self.user,
            exercise=self.exercise,
            score=100
        )

    def test_ranking_success(self):
        self.assertEqual(self.ranking.user, self.user)
        self.assertEqual(self.ranking.exercise, self.exercise)
        self.assertEqual(self.ranking.score, 100)
    
    def test_ranking_error(self):
        with self.assertRaises(IntegrityError):
            ExerciseRanking.objects.create(score=100)

    def test_ranking_obj_field(self):
        ranking = ExerciseRanking.objects.get(pk=1)
        field_label = ranking._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')


