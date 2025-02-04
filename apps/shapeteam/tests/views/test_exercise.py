import json
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from knox.models import AuthToken
from apps.shapeteam.serializers import *


PATH = 'fixtures/shapeteam'

class ExerciseAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
    ]

    def setUp(self):
        user = get_user_model().objects.get(pk=1)
        self.data = {
            "muscle_group": [3, 2, 5],
            "name": "Legs",
            "description": "Quadriceps, hamstrings, calves, and glutes.",
            "repetition": 20,
            "section": 3,
            "duration": "00:07:00",
            "finished": False
        }
        _, token = AuthToken.objects.create(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

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
