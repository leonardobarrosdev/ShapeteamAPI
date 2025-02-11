import json, ipdb

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from knox.models import AuthToken
from apps.shapeteam.serializers import *
from django.contrib.auth import get_user_model


User = get_user_model()

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
        _, token = AuthToken.objects.create(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_get_all_pending_requests(self):
        Connection.objects.create(sender=self.user2, receiver=self.user1)
        response = self.client.get(reverse('training-partners-pending'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sender'], self.user2.id)

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
