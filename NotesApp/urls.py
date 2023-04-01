from NotesApp.views import LabelAPI, NotesAPI, ArchiveNotesAPI, TrashNotesAPI, CollaboratorAPI
from django.urls import path

urlpatterns = [
    path('labelapi/', LabelAPI.as_view(), name='Labels'),
    path('notesapi/', NotesAPI.as_view(), name='Notes'),
    #path('notes/<id>', DeleteNotesAPI.as_view(), name='Notes_Delete'),
    path('notesarchive/', ArchiveNotesAPI.as_view(), name='Notes_Archive'),
    path('notestrash/', TrashNotesAPI.as_view(), name='Notes_Trash'),
    path('collaboratorapi/', CollaboratorAPI.as_view(), name='Collaborator'),
]