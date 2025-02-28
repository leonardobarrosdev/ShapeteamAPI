import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from knox.models import AuthToken
from apps.shapeteam.models import ExerciseRanking


PATH = 'fixtures/shapeteam'

class ExerciseRankingAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        f'{PATH}/muscle_group_fixture.json',
        f'{PATH}/exercise_fixture.json',
        f'{PATH}/exercise_ranking_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=7)
        _, token = AuthToken.objects.create(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.data = {
            'user': self.user.pk,
            'muscle_group': 1,
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
