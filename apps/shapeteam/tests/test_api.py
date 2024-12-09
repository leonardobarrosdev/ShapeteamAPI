import json
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.shapeteam.serializers import *

PATH = 'fixtures/shapeteam'

class ExerciseAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/name_exercise_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        self.data = {"name_exe": 1, "default_sets": 3, "default_reps": 10}

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
        del data['name_exe']
        response = self.client.post(
            reverse('exercise-list'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_exercise_success(self):
        exercise = Exercise.objects.get(pk=1)
        data = self.data.copy()
        data['default_sets'] = 5
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
        del data['name_exe']
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


class NameExerciseAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/name_exercise_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=2)
        self.client.force_authenticate(user=self.user)

    def test_list_name_exercises_success(self):
        response = self.client.get(reverse('nameexercise-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 16)
    
    def test_list_name_exercises_error(self):
        self.client.logout()
        response = self.client.get(reverse('nameexercise-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_name_exercise_success(self):
        response = self.client.post(
            reverse('nameexercise-list'),
            data=json.dumps({"name": "New Name"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NameExercise.objects.count(), 17)

    def test_create_name_exercise_error(self):
        response = self.client.post(
            reverse('nameexercise-list'),
            data=json.dumps({"name": ""}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
