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
