from django.test import TestCase
from rest_framework.test import APITestCase
# Create your tests here.

class SignupTestCase(APITestCase):
    def test_signup_success(self):
        url = 'http://localhost:8000/api/v1/accounts/signup/'
        data = {
            'username': 'hjnee1102',
            'password1': 'teshan3823@@',
            'password2': 'teshan3823@@',
            'email': 'hjnee1102@gmail.com',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_signup_email_failure(self):
        url = 'http://localhost:8000/api/v1/accounts/signup/'
        data = {
            'username': 'kyong0409',
            'password1': 'ssafy1234',
            'password2': 'ssafy1234',
            'email': 'kyong0409gmail.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)


    def test_signup_password_failure(self):
        url = 'http://localhost:8000/api/v1/accounts/signup/'
        data = {
            'username': 'kyong0409',
            'password1': 'ssafy1234',
            'password2': 'ssafy2345',
            'email': 'kyong0409@gmail.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)