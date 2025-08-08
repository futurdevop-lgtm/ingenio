from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestsTableau(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='passuser')

    def test_kpis(self):
        token = self.client.post(reverse('obtenir_jeton'), {'username': 'user', 'password': 'passuser'}, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.get(reverse('tableau-manager'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('kpis', resp.data)
