import json
from django.conf import settings
import redis

class RedisNote:
    redis_instance = redis.Redis(host='localhost',
                                 port=6379)

    def get_key(self, key):
        return self.redis_instance.get(key)

    def set_key_value(self, key, value):
        return self.redis_instance.set(key, value)

    def post_notes_redis(self, notes, user_id):
        user_id = str(user_id)
        note_dict = self.get_key(user_id)
        if note_dict is not None:
            note_dict = json.loads(note_dict)
        else:
            note_dict = {}
        note_id = notes.get('id')

        note_dict.update({str(note_id): notes})
        n_dict = json.dumps(note_dict)
        self.set_key_value(user_id, n_dict)

    def get_notes_redis(self, user_id):
        user_id = str(user_id)
        notes = self.get_key(user_id)
        dict_of_note = json.loads(notes)
        if dict_of_note is not None:
            return dict_of_note
        return {}

    def update_note_redis(self, data, user_id):
        dict_of_note = self.redis_instance.get(str(user_id))
        if dict_of_note is not None:
            dict_of_note = json.loads(dict_of_note)
            note_id = data.get('id')
            note_id = str(note_id)
            if note_id in dict_of_note.keys():
                dict_of_note.update({note_id: data})
                self.redis_instance.set(user_id, json.dumps(dict_of_note))

    def delete_note_redis(self, note_id, user_id):
        user_id = str(user_id)
        note_dict = self.get_key(user_id)
        if note_dict is not None:
            note_dict = json.loads(note_dict)
            if str(note_id) in note_dict.keys():
                note_dict.pop(str(note_id))
        n_dict = json.dumps(note_dict)
        self.set_key_value(user_id, n_dict)