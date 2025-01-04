import json

import ipdb
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from knox.models import AuthToken
from apps.shapeteam.serializers import *


PATH = 'fixtures/shapeteam'

class MuscleGroupAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=2)
        self.client.force_authenticate(user=self.user)

    def test_list_name_exercises_success(self):
        response = self.client.get(reverse('muscle-group-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_list_name_exercises_error(self):
        self.client.logout()
        response = self.client.get(reverse('muscle-group-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ExerciseAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        self.data = {
            "muscle_group": 3,
            "name": "Legs",
            "description": "Quadriceps, hamstrings, calves, and glutes.",
            "repetition": 20,
            "section": 3,
            "duration": "00:07:00",
            "finished": False
        }

    def test_create_exercise_success(self):
        response = self.client.post(
            reverse('exercise-list'),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 11)
    
    def test_create_exercise_error(self):
        data = self.data.copy()
        del data['name']
        response = self.client.post(
            reverse('exercise-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_exercise_success(self):
        exercise = Exercise.objects.get(pk=1)
        data = self.data.copy()
        data['section'] = 5
        response = self.client.put(
            reverse('exercise-detail', kwargs={'pk': str(exercise.pk)}),
            data=json.dumps(data),
            content_type='application/json'
        )
        exercise.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(exercise.section, 5)
    
    def test_update_exercise_error(self):
        exercise = Exercise.objects.get(pk=1)
        data = self.data.copy()
        del data['name']
        response = self.client.put(
            reverse('exercise-detail', kwargs={'pk': str(exercise.pk)}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_exercise_success(self):
        exercise = Exercise.objects.get(pk=1)
        response = self.client.delete(
            reverse('exercise-detail', kwargs={'pk': str(exercise.pk)}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exercise.objects.count(), 9)
    
    def test_delete_exercise_error(self):
        response = self.client.delete(
            reverse('exercise-detail', kwargs={'pk': '1000'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_list_exercises_success(self):
        response = self.client.get(reverse('exercise-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
    
    def test_list_exercises_error(self):
        self.client.logout()
        response = self.client.get(reverse('exercise-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class WeekRoutineAPITest(APITestCase):
    fixtures = [
        f'{PATH}/user_fixture.json',
        f'{PATH}/day_training_fixture.json',
        f'{PATH}/week_routine_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model()
        self.week_routine = WeekRoutine.objects.get(id=3)


class ExerciseRankingAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/exercise_ranking_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=7)
        self.client.force_authenticate(user=self.user)
        self.data = {
            'user': self.user.pk,
            'muscle_group': 1,
            'score': 6
        }

    def test_create_exercise_ranking_success(self):
        response = self.client.post(
            reverse('exerciseranking-list'),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExerciseRanking.objects.count(), 4)
    
    def test_create_exercise_ranking_error(self):
        data = self.data.copy()
        del data['user']
        response = self.client.post(
            reverse('exerciseranking-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_exercise_ranking_success(self):
        response = self.client.get(reverse('exerciseranking-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_list_exercise_ranking_error(self):
        ''' Has a error because the return is 404 '''
        response = self.client.get(reverse('exerciseranking-list') + '?user=1000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exercise_ranking_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('exerciseranking-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_exercise_ranking_error(self):
        response = self.client.get(reverse('exerciseranking-detail', kwargs={'pk': '1000'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_exercise_ranking_success(self):
        exercise_ranking = ExerciseRanking.objects.get(pk=1)
        data = self.data.copy()
        data['score'] = 8
        response = self.client.patch(
            reverse('exerciseranking-detail', kwargs={'pk': str(exercise_ranking.pk)}),
            data=json.dumps(data),
            content_type='application/json'
        )
        exercise_ranking.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(exercise_ranking.score, 8)
    
    def test_update_exercise_ranking_error(self):
        exercise_ranking = ExerciseRanking.objects.get(pk=1)
        data = self.data.copy()
        del data['score']
        response = self.client.put(
            reverse('exerciseranking-detail', kwargs={'pk': str(exercise_ranking.pk)}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_exercise_ranking_success(self):
        exercise_ranking = ExerciseRanking.objects.get(pk=1)
        response = self.client.delete(
            reverse('exerciseranking-detail', kwargs={'pk': str(exercise_ranking.pk)}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExerciseRanking.objects.count(), 2)
    
    def test_delete_exercise_ranking_error(self):
        response = self.client.delete(
            reverse('exerciseranking-detail', kwargs={'pk': '1000'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TrainingPartnersAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith'
        )
        self.user3 = User.objects.create_user(
            username='testuser3',
            email='testuser3@example.com',
            password='testpass123',
            first_name='Alice',
            last_name='Johnson'
        )
        self.client.login(username='testuser1', password='testpass123')
        self.client.force_authenticate(user=self.user1)

    def test_training_partners_list(self):
        Connection.objects.create(sender=self.user1, receiver=self.user2)
        Connection.objects.create(sender=self.user2, receiver=self.user1, accepted=True)
        response = self.client.get(reverse('training-partners-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user1.id in response.data[0].values())

    def test_accept_request(self):
        connection = Connection.objects.create(
            sender=self.user2,
            receiver=self.user1,
            accepted=False
        )
        url = reverse('training-partners-accept', kwargs={'pk': connection.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        connection.refresh_from_db()
        self.assertTrue(connection.accepted)

    def test_reject_request(self):
        connection = Connection.objects.create(
            sender=self.user2,
            receiver=self.user1,
            accepted=False
        )
        url = reverse('training-partners-reject', kwargs={'pk': connection.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Connection.DoesNotExist):
            Connection.objects.get(id=connection.id)

    def test_potential_partners(self):
        """Test the potential partners URL"""
        Connection.objects.create(sender=self.user1, receiver=self.user2, accepted=True)
        url = reverse('training-partners-potential')
        response = self.client.get(url, {'search': 'Alice'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response contains potential partner
        self.assertTrue(any(
            partner['username'] == 'testuser3' for partner in response.data
        ))

    def test_unauthorized_access(self):
        """Test unauthorized access to training partners URLs"""
        self.client.logout()
        urls = [
            reverse('training-partners-list'),
            reverse('training-partners-potential'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_connection_request(self):
        data = {'receiver': self.user3.id}
        response = self.client.post(
            reverse('training-partners-create'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Connection.objects.filter(
            sender=self.user1,
            receiver=self.user3
        ).exists())

    def test_duplicate_connection_request(self):
        """Test preventing duplicate connection requests"""
        Connection.objects.create(sender=self.user1, receiver=self.user3)
        url = reverse('training-partners-create')
        response = self.client.post(url, {'receiver': self.user3.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WeekRoutineAPITest(APITestCase):
    fixtures = [
        f'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/day_training_fixture.json',
        f'{PATH}/week_routine_fixture.json'
    ]

    def setUp(self):
        self.user = User.objects.get(id=4)
        self.other_user = User.objects.get(id=9)
        self.day_training = DayTraining.objects.get(id=3)
        self.week_routine = WeekRoutine.objects.filter(user=self.user).first()
        # Knox authentication
        _, token = AuthToken.objects.create(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.list_url = reverse('week-routine-list')
        self.detail_url = reverse('week-routine-detail', kwargs={'pk': self.week_routine.pk})

    def test_list_week_routines_authenticated(self):
        """Verify authenticated user can list their week routines"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)

    def test_list_week_routines_unauthenticated(self):
        """Verify unauthenticated access is denied"""
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_own_week_routine(self):
        """Verify user can retrieve their own week routine"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_retrieve_others_week_routine(self):
        """Verify user cannot retrieve another user's week routine"""
        other_routine = WeekRoutine.objects.create(user=self.other_user)
        other_url = reverse('week-routine-detail', kwargs={'pk': other_routine.pk})
        response = self.client.get(other_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_week_routine(self):
        """Verify user can update their week routine"""
        day_training1 = DayTraining.objects.get(id=8)
        day_training2 = DayTraining.objects.get(id=2)
        data = {
            'days_training': [
                day_training1.id,
                day_training2.id
            ],
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(day_training2.id, response.data['days_training'])

    def test_partial_update_week_routine(self):
        """Verify user can partially update their week routine"""
        new_day = DayTraining.objects.create(name="Another Day")
        data = {'days_training': [new_day.id]}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(new_day.id, [day['id'] for day in response.data['days_training']])

    def test_delete_week_routine(self):
        """Verify user can delete their week routine"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WeekRoutine.objects.filter(pk=self.week_routine.pk).exists())

    def test_token_expiration(self):
        """Verify expired token cannot access endpoints"""
        token = AuthToken.objects.get(user=self.user)
        token.delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token(self):
        """Verify invalid token cannot access endpoints"""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_multiple_day_training_assignment(self):
        """Verify multiple days can be assigned to a week routine"""
        data = {'days_training': [5, 1]}
        response = self.client.patch(
            self.detail_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['days_training']), 2)


class DayTrainingAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/day_training_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(id=6)
        self.exercise = Exercise.objects.first()
        self.day_training = DayTraining.objects.create(weekday='monday')
        self.day_training.exercises.add(self.exercise)
        _, token = AuthToken.objects.create(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.list_url = reverse('day-training-list')
        self.detail_url = reverse('day-training-detail', kwargs={'pk': self.day_training.pk})

    def test_list_day_trainings(self):
        """Test retrieving list of day trainings"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_day_training(self):
        """Test creating a new day training"""
        data = {
            'weekday': 'tuesday',
            'exercises': [self.exercise.id]
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['weekday'], 'tuesday')
        self.assertIn(self.exercise.id, response.data['exercises'])

    def test_create_day_training_invalid_weekday(self):
        """Test creating a day training with invalid weekday"""
        data = {
            'weekday': 'invalid_day',
            'exercises': [self.exercise.id]
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_day_training(self):
        """Test retrieving a specific day training"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['weekday'], self.day_training.weekday)

    def test_update_day_training(self):
        """Test updating a day training"""
        new_exercise = Exercise.objects.create(
            muscle_group_id=1,
            name="New Exercise",
            repetition=10,
            section=1,
            duration="00:30:00"
        )
        data = {
            'weekday': 'wednesday',
            'exercises': [new_exercise.id]
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['weekday'], 'wednesday')
        self.assertIn(new_exercise.id, response.data['exercises'])

    def test_partial_update_day_training(self):
        """Test partially updating a day training"""
        data = {'weekday': 'friday'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['weekday'], 'friday')

    def test_delete_day_training(self):
        """Test deleting a day training"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DayTraining.objects.filter(pk=self.day_training.pk).exists())

    def test_add_exercises_to_day_training(self):
        """Test adding multiple exercises to a day training"""
        new_exercises = [
            Exercise.objects.create(
                muscle_group_id=1,
                name=f"Exercise {i}",
                repetition=10,
                section=1,
                duration="00:30:00"
            ) for i in range(3)
        ]
        data = {
            'exercises': [ex.id for ex in new_exercises]
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['exercises']), 3)

    def test_unauthenticated_access(self):
        """Test access to endpoints without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_without_exercises(self):
        """Test creating a day training without exercises"""
        data = {'weekday': 'thursday'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['exercises']), 0)

    def test_update_with_invalid_exercise(self):
        """Test updating with non-existent exercise"""
        data = {
            'weekday': 'monday',
            'exercises': [99999]  # Non-existent exercise ID
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)