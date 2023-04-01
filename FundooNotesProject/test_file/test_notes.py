from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

class TestSetUp(APITestCase):

    def setUp(self):
        self.notes_url = reverse('Notes')
        self.labels_url = reverse('Labels')
        self.jwt_token = reverse('token_obtain_pair')
        self.register_url = reverse('register')
        self.archive_url = reverse('Notes_Archive')
        self.trash_url = reverse('Notes_Trash')
        self.client = APIClient()

        self.data = {
            "username": "User1",
            "email": "testuser@gmail.com",
            "password": "1234"
        }

        self.proper_label = {
            "label_name": "TrialLabel10"
        }

        self.improper_label = {
            "label_name": 1234
        }

        self.proper_note = {
            "title":"TrialNote1",
            "description":"Used for checking Notes"
        }

        self.improper_note = {
            "description": "1234"
        }

        self.note_archive = {
            "title": "TrialNote1",
            "description": "Used for checking Notes",
            "isArchive": True
        }

        self.note_archive_fail = {
            "title": "TrialNote1",
            "description": "Used for checking Notes",
            "isArchive": False
        }

        self.note_trash = {
            "title": "TrialNote1",
            "description": "Used for checking Notes",
            "isTrash": True
        }
    def tearDown(self):
        return super().tearDown()

    def get_token(self):
        self.client.post(self.register_url, data=self.data)
        self.login_info = {'username': 'User1', 'password': '1234'}
        response = self.client.post(self.jwt_token, self.login_info, format='json')
        self.assertEqual(response.status_code, 200)
        return response.data['access']