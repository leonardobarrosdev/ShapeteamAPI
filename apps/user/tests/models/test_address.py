from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError
from apps.user.models import Address


class AddressTest(TestCase):
    fixtures = [
        'apps/user/fixtures/user_fixture.json',
        'apps/user/fixtures/address_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.address = Address.objects.get(pk=1)

    def test_address_success(self):
        self.assertIsInstance(self.address, Address)
        self.assertEqual(self.address.user, self.user)
        self.assertEqual(self.address.city, "New York")
        self.assertEqual(self.address.state, "NY")
        self.assertEqual(self.address.country, "USA")
    
    def test_address_obj_field(self):
        field_label = self.address._meta.get_field('city').verbose_name
        self.assertEqual(field_label, 'city')
        self.assertEqual(str(self.address), "New York, NY, USA")
    
    def test_address_str(self):
        self.assertEqual(str(self.address), "New York, NY, USA")
    
    def test_address_error(self):
        with self.assertRaises(IntegrityError):
            Address.objects.create(user=self.user)
    
    def test_field_user_prefetch_related(self):
        address = Address.objects.prefetch_related('user').get(pk=1)
        self.assertTrue(hasattr(address, 'user'))
        self.assertEqual(address.user.first_name, self.user.first_name)
        self.assertEqual(address.user.last_name, self.user.last_name)
        self.assertEqual(address.user.level, self.user.level)
        self.assertEqual(str(address.user), self.user.email)