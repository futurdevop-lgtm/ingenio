from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from profiles.models import EngineerProfile, Skill, EngineerSkill

User = get_user_model()


class TestsRecherche(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='passuser')
        self.p1 = EngineerProfile.objects.create(user=self.user, title='Dev Web', years_of_experience=4, location='Paris', availability='remote')
        self.react = Skill.objects.create(name='React', category='FRAMEWORK')
        EngineerSkill.objects.create(profile=self.p1, skill=self.react, years_experience=3, level='Intermédiaire')

    def _token(self):
        url = reverse('obtenir_jeton')
        return self.client.post(url, {'username': 'user', 'password': 'passuser'}, format='json').data['access']

    def test_recherche_par_competence(self):
        token = self._token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('recherche-ingenieurs') + '?competence=React'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data), 1)

    def test_recherche_par_localisation(self):
        token = self._token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('recherche-ingenieurs') + '?localisation=Par'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data), 1)
