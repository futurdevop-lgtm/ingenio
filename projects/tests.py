from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from profiles.models import EngineerProfile, Skill, EngineerSkill

User = get_user_model()


class TestsProjets(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username='manager', password='passmanager', role='MANAGER')
        self.dev = User.objects.create_user(username='dev', password='passdev')
        self.profil_dev = EngineerProfile.objects.create(user=self.dev, title='Dev', years_of_experience=5)
        self.skill_python = Skill.objects.create(name='Python', category='LANGUAGE')
        EngineerSkill.objects.create(profile=self.profil_dev, skill=self.skill_python, years_experience=5, level='Senior')

    def _token(self, username, password):
        url = reverse('obtenir_jeton')
        return self.client.post(url, {'username': username, 'password': password}, format='json').data['access']

    def test_creation_projet_par_manager(self):
        token = self._token('manager', 'passmanager')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('projet-list')
        payload = {
            'name': 'Projet Python',
            'description': 'Test',
            'requirements': [
                {'skill_id': self.skill_python.id, 'minimum_years': 3, 'level': 'Intermédiaire'}
            ]
        }
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_matching(self):
        token = self._token('manager', 'passmanager')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        # Créer projet
        url = reverse('projet-list')
        resp = self.client.post(url, {'name': 'P', 'requirements': [{'skill_id': self.skill_python.id, 'minimum_years': 3, 'level': 'Intermédiaire'}]}, format='json')
        pid = resp.data['id']
        # matching
        match_url = reverse('projet-detail', args=[pid]) + 'matching/'
        mresp = self.client.get(match_url)
        self.assertEqual(mresp.status_code, 200)
        self.assertTrue(any(r['utilisateur'] == 'dev' for r in mresp.data))
