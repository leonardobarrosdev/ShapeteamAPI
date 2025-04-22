import datetime
from random import random
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from knox.models import AuthToken
from apps.shapeteam.models import Exercise, DayTraining


PATH = 'apps/shapeteam/fixtures'

class DayTrainingAPITest(APITestCase):
    fixtures = [
        'apps/user/fixtures/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        F'{PATH}/week_routine_fixture.json',
        f'{PATH}/day_training_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(id=6)
        _, token = AuthToken.objects.create(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.list_url = reverse('day-training-list')
        self.detail_url = reverse('day-training-detail', kwargs={'pk': 7})
        self.day_training = self.client.get(self.detail_url, {'weekday': 'sunday'}, format='json')

    def test_list_day_training(self):
        """Test retrieving list of day trainings"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for data in response.data:
            self.assertEquals(data['week_routine']['user'], self.user.id)

    def test_create_day_training(self):
        """Test creating a new day training"""
        data = {
            'weekday': 'tuesday',
            'muscle_group': [5, 7],
            'week_routine': 7
        }
        response = self.client.post(reverse('day-training-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['weekday'], 'tuesday')
        self.assertIn(7, response.data['muscle_group'])

    def test_create_day_training_invalid_weekday(self):
        """Test creating a day training with invalid weekday"""
        data = {
            'weekday': 'invalid_day',
            'muscle_group': [3, 6],
        }
        response = self.client.post(reverse('day-training-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_day_training(self):
        """Test retrieving a specific day training"""
        response = self.client.get(
            self.detail_url,
            {'weekday': 'sunday'},
            format='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['weekday'], 'sunday')

    def test_partial_update_day_training(self):
        """Test partially updating a day training"""
        data = {'muscle_group': [4, 6]}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(4 and 6, response.data['muscle_group'])

    def test_delete_day_training(self):
        """Test deleting a day training"""
        response_wr = self.client.post(reverse('week-routine-list'), format='json')
        self.assertEqual(response_wr.status_code, 201)
        response_dt = self.client.post(
            reverse('day-training-create'),
            data={'weekday': 'sunday', 'muscle_group': [2, 9], 'week_routine': response_wr.data['id']},
            format='json'
        )
        self.assertEqual(response_dt.status_code, 201)
        detail_url = reverse(
            'day-training-detail',
            kwargs={'weekday': response_dt.data['weekday']}
        )
        day_training = DayTraining.objects.filter(weekday=response_dt.data['weekday']).last()
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DayTraining.objects.filter(id=day_training.id).exists())

    def test_add_exercises_to_day_training(self):
        """Test adding multiple exercises to a day training"""
        new_exercises = [
            Exercise.objects.create(
                muscle_group_id=random.randint(1, 10),
                name=f"Exercise {i}",
                repetition=random.randint(5, 60),
                section=random.randint(3, 6),
                duration=datetime.timedelta(
                    seconds=random.randint(65, 360)
                )
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
