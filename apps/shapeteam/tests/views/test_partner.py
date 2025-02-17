import json
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from knox.models import AuthToken
from apps.shapeteam.serializers import *
from django.contrib.auth import get_user_model


User = get_user_model()

class TrainingPartnersAPITest(APITestCase):
    fixtures = [
        'apps/user/fixtures/user_fixture.json',
        'apps/shapeteam/fixtures/connection_fixture.json'
    ]
    
    def setUp(self):
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)
        self.user3 = User.objects.get(id=3)
        _, self.token1 = AuthToken.objects.create(self.user1)
        _, self.token2 = AuthToken.objects.create(self.user2)
        _, self.token3 = AuthToken.objects.create(self.user3)

    def test_get_all_pending_request(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse('training-partner-pending'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_training_partner_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(reverse('training-partner-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for partner in response.data:
            self.assertTrue(partner['accepted'])

    def test_accept_request(self):
        user = User.objects.get(id=7)
        _, token = AuthToken.objects.create(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post(
            reverse('training-partner-accept', kwargs={'pk':8})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['accepted'])

    def test_reject_request(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.delete(
            reverse('training-partner-reject', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Connection.DoesNotExist):
            Connection.objects.get(sender=self.user2, receiver_id=1)


    def test_unauthorized_access(self):
        """Test unauthorized access to training partners URLs"""
        self.client.logout()
        response = self.client.get(reverse('training-partner-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_connection_request(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        data = {'receiver': self.user3.id}
        response = self.client.post(
            reverse('training-partner-create'),
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
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.post(
            reverse('training-partner-create'),
            {'receiver': self.user2.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
