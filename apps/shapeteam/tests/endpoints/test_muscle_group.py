from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from knox.models import AuthToken


PATH = 'fixtures/shapeteam'

class MuscleGroupAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=2)
        _, token = AuthToken.objects.create(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_list_name_exercises_success(self):
        response = self.client.get(reverse('muscle-group-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_list_name_exercises_error(self):
        self.client.logout()
        response = self.client.get(reverse('muscle-group-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
