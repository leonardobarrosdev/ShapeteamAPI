from django.core import mail
from django.test import TestCase
from api.user.models import CustomUser


class UserModelTest(TestCase):
    fixtures = ['fixtures/user/user_fixture.json']

    def setUp(self):
        self.username = 'test'
        self.data = {
            'username': self.username,
            'thumbnail': f'thumbnails/{self.username}',
            'email': 'test@company.com',
            'gender': 1,
            'password': 'password123'
        }

    def test_create_user_success(self):
        user = CustomUser.objects.create_user(**self.data)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.__str__(), f'{user.email} - {user.username}')

    def test_create_user_error(self):
        data = self.data.copy()
        del data['email']
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(**data)

    def test_user_obj_field(self):
        user = CustomUser.objects.get(pk=10)
        field_label = user._meta.get_field('username').verbose_name
        max_length = user._meta.get_field('username').max_length
        self.assertEqual(field_label, 'username')
        self.assertEqual(max_length, 30)
        self.assertEqual(str(user), f"{user.email} - {user.username}")

    def test_create_superuser_success(self):
        user = CustomUser.objects.create_superuser(**self.data)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.thumbnail, self.data['thumbnail'])

    def test_create_superuser_error(self):
        user = CustomUser.objects.create_superuser(**self.data)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.thumbnail, self.data['thumbnail'])
