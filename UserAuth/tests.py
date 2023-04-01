from django.test import TestCase
from UserAuth.test_user import TestUserRegistrationSetup

class UserRegistrationTest(TestUserRegistrationSetup):
    def test_user_is_registered(self):
        response = self.client.post(self.register_url, data=self.data)
        self.assertEqual(response.status_code, 200)

    def test_user_incomplete_details_are_entered_should_not_register(self):
        response = self.client.post(self.register_url, data=self.incomplete_details)
        self.assertEqual(response.status_code, 400)

    def test_user_without_without_email_should_pass(self):
        response = self.client.post(self.register_url, data=self.blank_email)
        self.assertEqual(response.status_code, 200)


class UserLoginTest(TestUserRegistrationSetup):

    def test_user_enters_with_proper_credentials(self):
        response = self.client.post(self.register_url, data=self.data)
        response = self.client.post(self.login_url, data=self.proper_login)
        self.assertEqual(response.status_code, 200)

    def test_user_without_providing_login_credentials_should_not_enter(self):
        response = self.client.post(self.register_url, data=self.data)
        response = self.client.post(self.login_url, data=self.improper_login_without_credentials)
        self.assertEqual(response.status_code, 400)

    def test_user_with_improper_password_should_not_enter(self):
        response = self.client.post(self.register_url, data=self.data)
        response = self.client.post(self.login_url, data=self.improper_login_without_password)
        self.assertEqual(response.status_code, 400)
