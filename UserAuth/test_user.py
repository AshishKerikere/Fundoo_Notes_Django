from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

class TestUserRegistrationSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.jwt_token = reverse('token_obtain_pair')
        self.client = APIClient()
        self.data = {
            "username": "User1",
            "email": "testuser@gmail.com",
            "password": "1234"
        }

        self.incomplete_details = {
            "username": "User2",
            "email":"testuser2@gmail.com",
            "password":""
        }

        self.blank_email = {
            "username": "User1",
            "email": "",
            "password": "1234"
        }

        self.proper_login = {'username': "User1", 'password': "1234"}

        self.improper_login_without_credentials = {'username': "", 'password': ""}

        self.improper_login_without_password = {'username': "User1", 'password': ""}

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def get_token(self):
        # self.client.post(self.register_url, data=self.data)
        self.login_info = {'username': 'AshishK', 'password': '1234'}
        response = self.client.post(self.jwt_token, self.login_info, format='json')
        self.assertEqual(response.status_code, 200)
        return response.data['access']