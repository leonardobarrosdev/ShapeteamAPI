import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class RegisterAPITest(APITestCase):
    fixtures = ['fixtures/user/user_fixture.json']
    data = {
        "first_name": "wedley",
        "last_name": "Doe",
        "email": "wedley@company.com",
        "password": "p4ssM0rd",
        "password2": "p4ssM0rd"
    }
    User = get_user_model()

    def test_create_user_success(self):
        response = self.client.post(
            reverse('user:register'),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.User.objects.count(), 11)
        self.assertEqual(response.data['user']['email'], self.data['email'])

    def test_create_user_error(self):
        data = self.data.copy()
        del data['email']
        response = self.client.post(
            reverse('user:register'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginAPITest(APITestCase):
    fixtures = ['fixtures/user/user_fixture.json']

    def test_login_success(self):
        data = {"email": "fulano@company.com", "password": "password123", }
        response = self.client.post(
            reverse('user:login'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_error(self):
        data = {"email": "fulano@company.com", "password": "wrongPassword"}
        response = self.client.post(
            reverse('user:login'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateUserAPITest(APITestCase):
    fixtures = ['fixtures/user/user_fixture.json']

    def setUp(self):
        self.user = get_user_model().objects.get(id=4)
        self.client.force_authenticate(user=self.user)

    def test_update_user_success(self):
        response = self.client.patch(
            reverse('user:update', kwargs={'pk': str(self.user.pk)}),
            data=json.dumps({'last_name': 'Doe'}),
            content_type='application/json'
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['last_name'], 'Doe')

    def test_update_user_error(self):
        response = self.client.put(
            reverse('user:update', kwargs={'pk': str(self.user.pk)}),
            data=json.dumps({'email': ''}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPITest(APITestCase):
    fixtures = ['fixtures/user/user_fixture.json']

    def setUp(self):
        self.user = get_user_model().objects.get(id=5)
        self.client.force_authenticate(user=self.user)
        self.valid_data = {
            'old_password': '123456',
            'password': 'NewSecurePassword123!',
            'password2': 'NewSecurePassword123!'
        }
        self.invalid_data = {
            'old_password': 'wrongpassword',
            'password': 'newpassword',
            'password2': 'differentpassword'
        }

    def test_change_password_success(self):
        response = self.client.put(
            reverse('user:change-password', kwargs={'pk': self.user.id}),
            data=self.valid_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        # Verify the password was actually changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.valid_data['password']))

    def test_change_password_validation_errors(self):
        response = self.client.put(
            reverse('user:change-password', kwargs={'pk': self.user.id}),
            data=self.invalid_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('old_password', response.data)


class SearchUserAPITest(APITestCase):
    fixtures = ['fixtures/user/user_fixture.json']

    def setUp(self):
        self.user = get_user_model().objects.get(id=5)
        self.client.force_authenticate(user=self.user)

    def test_search_user(self):
        response = self.client.get(
            reverse('user:search-users'),
            data={'search': 'darty'},
            content_type='application/json'
        )
        self.assertEqual('darty', json.loads(response.content)[0]['first_name'])
