from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status


class AuthTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='existinguser', password='testpass123')
        self.token = Token.objects.create(user=self.user)

    def test_user_registration(self):
        """New users can register via Djoser"""
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            're_password': 'newpassword123',
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_password_mismatch(self):
        """Registration fails if passwords do not match"""
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            're_password': 'wrongpassword',
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_username(self):
        """Registration fails if username already exists"""
        data = {
            'username': 'existinguser',
            'password': 'testpass123',
            're_password': 'testpass123',
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token(self):
        """Users can obtain an auth token with valid credentials"""
        data = {'username': 'existinguser', 'password': 'testpass123'}
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)

    def test_obtain_token_wrong_password(self):
        """Token request fails with wrong password"""
        data = {'username': 'existinguser', 'password': 'wrongpassword'}
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token_nonexistent_user(self):
        """Token request fails for non-existent user"""
        data = {'username': 'nobody', 'password': 'testpass123'}
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_invalidates_token(self):
        """Logging out invalidates the token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/auth/token/logout/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unauthenticated(self):
        """Logout without token returns 401"""
        response = self.client.post('/auth/token/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_current_user_authenticated(self):
        """Authenticated users can retrieve their own profile"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/auth/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')

    def test_get_current_user_unauthenticated(self):
        """Unauthenticated users cannot retrieve profile"""
        response = self.client.get('/auth/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
