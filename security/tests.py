from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestsSecurite(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='passadmin', is_staff=True)
        self.user = User.objects.create_user(username='user', password='passuser')

    def _token(self, username, password):
        url = reverse('obtenir_jeton')
        return self.client.post(url, {'username': username, 'password': password}, format='json').data['access']

    def test_audits_reserve_admin(self):
        # utilisateur normal refusé
        token = self._token('user', 'passuser')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.get(reverse('audits-connexion'))
        self.assertEqual(resp.status_code, 403)
        # admin autorisé
        token = self._token('admin', 'passadmin')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.get(reverse('audits-connexion'))
        self.assertEqual(resp.status_code, 200)
