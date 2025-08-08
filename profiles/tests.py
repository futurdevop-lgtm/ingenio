from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from profiles.models import EngineerProfile

User = get_user_model()


class TestsProfils(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username='manager', email='m@m.com', password='passmanager', role='MANAGER')
        self.user = User.objects.create_user(username='user', email='u@u.com', password='passuser')
        self.profile = EngineerProfile.objects.create(user=self.user, title='Dev', years_of_experience=3)

    def _token(self, username, password):
        url = reverse('obtenir_jeton')
        return self.client.post(url, {'username': username, 'password': password}, format='json').data['access']

    def test_lecture_profils_auth(self):
        token = self._token('user', 'passuser')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('profil-ingenieur-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_modification_propre_profil(self):
        token = self._token('user', 'passuser')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('profil-ingenieur-detail', args=[self.profile.id])
        resp = self.client.patch(url, {'title': 'Dev Senior'}, format='json')
        self.assertIn(resp.status_code, [200, 202])

    def test_modification_profil_autrui_refuse(self):
        autre = User.objects.create_user(username='autre', password='pass')
        autre_profile = EngineerProfile.objects.create(user=autre, title='Autre', years_of_experience=1)
        token = self._token('user', 'passuser')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('profil-ingenieur-detail', args=[autre_profile.id])
        resp = self.client.patch(url, {'title': 'Hack'}, format='json')
        self.assertEqual(resp.status_code, 403)

    def test_manager_peut_creer_profil(self):
        token = self._token('manager', 'passmanager')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('profil-ingenieur-list')
        resp = self.client.post(url, {'user': self.manager.id, 'title': 'Lead', 'years_of_experience': 8}, format='json')
        self.assertEqual(resp.status_code, 201)
