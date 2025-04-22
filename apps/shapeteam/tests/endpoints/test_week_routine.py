import json
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from knox.models import AuthToken
from apps.shapeteam.models import WeekRoutine, DayTraining


PATH = 'fixtures/shapeteam'

class WeekRoutineAPITest(APITestCase):
    fixtures = [
        f'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/day_training_fixture.json',
        f'{PATH}/week_routine_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(id=4)
        self.other_user = get_user_model().objects.get(id=9)
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