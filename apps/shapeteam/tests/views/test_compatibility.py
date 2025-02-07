import pdb
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken


PATH = 'apps/shapeteam/fixtures'

class UserCompatibilityAPITest(APITestCase):
    fixtures = [
        'apps/user/fixtures/user_fixture.json',
        f'{PATH}/user_metrics_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        'apps/user/fixtures/address_fixture.json',
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(id=5)
        _, token = AuthToken.objects.create(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.url = reverse('user-compatibility')

    def test_user_compatibility_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
    
    def test_user_compatibility_failure(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token 12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
