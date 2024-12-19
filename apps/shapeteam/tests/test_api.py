import json
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
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
        response = self.client.get(reverse('muscle-group'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_list_name_exercises_error(self):
        self.client.logout()
        response = self.client.get(reverse('muscle-group'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ExerciseAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        self.data = {
            "muscle_group": 3,
            "name": "Legs",
            "description": "Quadriceps, hamstrings, calves, and glutes.",
            "repetition": 20,
            "section": 3,
            "duration": "00:07:00",
            "finished": False
        }

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
        self.assertEqual(exercise.default_sets, 5)
    
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


class DayExerciseAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/name_exercise_fixture.json',
        f'{PATH}/day_exercise_fixture.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=3)
        self.client.force_authenticate(user=self.user)
        self.data = {
            "user": self.user.pk,
            "exercise": 4,
            "reps": 30,
            "sets": 2,
            "duration": "2 05:00:00"
        }

    def test_day_exercise_success(self):
        response = self.client.get(reverse('dayexercise-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
    
    def test_day_exercise_error(self):
        response = self.client.get(reverse('dayexercise-detail', kwargs={'pk': '1000'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_day_exercise_success(self):
        response = self.client.post(
            reverse('dayexercise-list'),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DayExercise.objects.count(), 4)
    
    def test_create_day_exercise_error(self):
        data = self.data.copy()
        del data['exercise']
        response = self.client.post(
            reverse('dayexercise-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_day_exercise_success(self):
        day_exercise = DayExercise.objects.get(pk=1)
        data = self.data.copy()
        data['sets'] = 3
        response = self.client.put(
            reverse('dayexercise-detail', kwargs={'pk': str(day_exercise.pk)}),
            data=json.dumps(data),
            content_type='application/json'
        )
        day_exercise.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(day_exercise.sets, 3)
    
    def test_update_day_exercise_error(self):
        day_exercise = DayExercise.objects.get(pk=1)
        data = self.data.copy()
        del data['sets']
        response = self.client.put(
            reverse('dayexercise-detail', kwargs={'pk': str(day_exercise.pk)}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_day_exercise_success(self):
        day_exercise = DayExercise.objects.get(pk=1)
        response = self.client.delete(
            reverse('dayexercise-detail', kwargs={'pk': str(day_exercise.pk)}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DayExercise.objects.count(), 2)
    
    def test_delete_day_exercise_error(self):
        response = self.client.delete(
            reverse('dayexercise-detail', kwargs={'pk': '1000'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ExerciseRankingAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/name_exercise_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/exercise_ranking_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=7)
        self.client.force_authenticate(user=self.user)
        self.data = {
            'user': self.user.pk,
            'exercise': 1,
            'score': 6
        }

    def test_create_exercise_ranking_success(self):
        response = self.client.post(
            reverse('exerciseranking-list'),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExerciseRanking.objects.count(), 4)
    
    def test_create_exercise_ranking_error(self):
        data = self.data.copy()
        del data['user']
        response = self.client.post(
            reverse('exerciseranking-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_exercise_ranking_success(self):
        response = self.client.get(reverse('exerciseranking-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_list_exercise_ranking_error(self):
        ''' Has a error because the return is 404 '''
        response = self.client.get(reverse('exerciseranking-list') + '?user=1000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exercise_ranking_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('exerciseranking-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_exercise_ranking_error(self):
        response = self.client.get(reverse('exerciseranking-detail', kwargs={'pk': '1000'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_exercise_ranking_success(self):
        exercise_ranking = ExerciseRanking.objects.get(pk=1)
        data = self.data.copy()
        data['score'] = 8
        response = self.client.patch(
            reverse('exerciseranking-detail', kwargs={'pk': str(exercise_ranking.pk)}),
            data=json.dumps(data),
            content_type='application/json'
        )
        exercise_ranking.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(exercise_ranking.score, 8)
    
    def test_update_exercise_ranking_error(self):
        exercise_ranking = ExerciseRanking.objects.get(pk=1)
        data = self.data.copy()
        del data['score']
        response = self.client.put(
            reverse('exerciseranking-detail', kwargs={'pk': str(exercise_ranking.pk)}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_exercise_ranking_success(self):
        exercise_ranking = ExerciseRanking.objects.get(pk=1)
        response = self.client.delete(
            reverse('exerciseranking-detail', kwargs={'pk': str(exercise_ranking.pk)}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExerciseRanking.objects.count(), 2)
    
    def test_delete_exercise_ranking_error(self):
        response = self.client.delete(
            reverse('exerciseranking-detail', kwargs={'pk': '1000'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
        self.client.login(username='testuser1', password='testpass123')
        self.client.force_authenticate(user=self.user1)

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