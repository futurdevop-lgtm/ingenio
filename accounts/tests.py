from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestsComptes(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', email='a@a.com', password='passadmin', is_staff=True)
        self.user = User.objects.create_user(username='user', email='u@u.com', password='passuser')

    def test_obtenir_jeton_jwt(self):
        url = reverse('obtenir_jeton')
        response = self.client.post(url, {'username': 'user', 'password': 'passuser'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_inscription(self):
        url = reverse('utilisateur-list') + 'inscription/'
        data = {
            'username': 'nouveau',
            'email': 'n@n.com',
            'password': 'password123',
            'first_name': 'Nouveau',
            'last_name': 'User',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(username='nouveau').count(), 1)

    def test_moi(self):
        token = self.client.post(reverse('obtenir_jeton'), {'username': 'user', 'password': 'passuser'}, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('utilisateur-list') + 'moi/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'user')
