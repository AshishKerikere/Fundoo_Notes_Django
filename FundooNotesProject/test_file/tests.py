from FundooNotesProject.test_file.test_notes import TestSetUp
from NotesApp.models import NotesModel
class TestLabelsAPI(TestSetUp):
    def test_create_label(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.labels_url, data=self.proper_label, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['label_name'], "TrialLabel10")

    def test_create_label_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.labels_url, data=self.improper_label, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_label(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.labels_url, data=self.proper_label, format='json')
        response = self.client.get(self.labels_url, data=self.proper_label, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_label_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # response = self.client.post(self.labels_url, data=self.proper_label, format='json')
        response = self.client.get(self.labels_url, data=self.proper_label, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_label(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.labels_url, data=self.proper_label, format='json')
        label_id = response.data['data']['id']
        updated_label_data = {
            "id":label_id,
            "label_name": "Updated Test Label"}
        response = self.client.put(self.labels_url, data=updated_label_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['label_name'], "Updated Test Label")

    def test_update_label_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.labels_url, data=self.proper_label, format='json')
        label_id = response.data['data']['id']
        updated_label_data_withoutid = {
            "label_name": "Updated Test Label"}
        response = self.client.put(self.labels_url, data=updated_label_data_withoutid, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_label(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.labels_url, data=self.proper_label, format='json')
        label_id = response.data['data']['id']
        delete_label_data = {
            "id": label_id}
        response = self.client.delete(self.labels_url, data=delete_label_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_label_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.labels_url, data=self.proper_label, format='json')
        label_id = response.data['data']['id']
        delete_label_data = {}
        response = self.client.delete(self.labels_url, data=delete_label_data)
        self.assertEqual(response.status_code, 400)

class TestNotesAPI(TestSetUp):

    def test_create_valid_note(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.proper_note, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_note(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.improper_note, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_note(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, data=self.proper_note, format='json')
        response = self.client.get(self.notes_url, data=self.proper_note, format='json')
        stored_note_title = response.data['data'][0]['title']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(stored_note_title, self.proper_note.get('title'))

    def test_get_note_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # response = self.client.post(self.notes_url, data=self.proper_note, format='json')
        response = self.client.get(self.notes_url, data=self.proper_note, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_note(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, data=self.proper_note, format='json')
        note_retrieved = response.data['data']
        updated_note_data = {
            "id":note_retrieved['id'],
            "title": note_retrieved['title'],
            "description": "Note after Testing Update"
        }
        response = self.client.put(self.notes_url, data=updated_note_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['description'], updated_note_data["description"])

    def test_update_note_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, data=self.proper_note, format='json')
        note_retrieved = response.data['data']
        updated_note_data = {
            "title": note_retrieved['title'],
            "description": "Note after Testing Update"
        }
        response = self.client.put(self.notes_url, data=updated_note_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_note(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, data=self.proper_note, format='json')
        label_id = response.data['data']['id']
        delete_note_data = {
            "id": label_id}
        response = self.client.delete(self.notes_url, data=delete_note_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data'], {})

    def test_delete_note_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, data=self.proper_note, format='json')
        label_id = response.data['data']['id']
        delete_note_data = {
            "id": label_id}
        response = self.client.delete(self.notes_url)
        self.assertEqual(response.status_code, 400)

class TestArchiveNotesAPI(TestSetUp):

    def test_create_archive_notes(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_archive, format='json')
        archive_note_id = response.data['data']['id']
        archive_note_data = {
            "id": archive_note_id
        }
        response = self.client.post(self.archive_url, data=archive_note_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['isArchive'], not self.note_archive["isArchive"])

    def test_create_archive_notes_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_archive, format='json')
        archive_note_data = {   }
        response = self.client.post(self.archive_url, data=archive_note_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_archive_notes(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_archive, format='json')
        response = self.client.get(self.archive_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['data'][0]['isArchive'])

    def test_get_archive_notes_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_archive_fail, format='json')
        response = self.client.get(self.archive_url)
        self.assertEqual(response.status_code, 400)

    def test_put_archive_notes(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_archive, format='json')
        archive_note_id = response.data['data']['id']
        archive_note_data = {
            "id": archive_note_id
        }
        response = self.client.put(self.archive_url, archive_note_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['data']['isArchive'])

    def test_put_archive_notes_fail(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_archive, format='json')
        archive_note_data = {        }
        response = self.client.put(self.archive_url, archive_note_data)
        self.assertEqual(response.status_code, 400)

class TestTrashNotesAPI(TestSetUp):

    def test_create_trash_notes(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_trash, format='json')
        trash_note_id = response.data['data']['id']
        trash_note_data = {
            "id": trash_note_id
        }
        response = self.client.post(self.trash_url, data=trash_note_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_trash_notes(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_trash, format='json')
        response = self.client.get(self.trash_url)
        self.assertEqual(response.status_code, 200)

    def test_put_trash_notes(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.notes_url, self.note_trash, format='json')
        trash_note_id = response.data['data']['id']
        trash_note_data = {
            "id": trash_note_id
        }
        response = self.client.put(self.trash_url, trash_note_data)
        self.assertEqual(response.status_code, 200)
