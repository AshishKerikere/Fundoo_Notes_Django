from django.shortcuts import render
from rest_framework.views import APIView

from UserAuth.utils import SessionAuth
from .serializers import LabelSerializer, NotesSerializer
from rest_framework.response import Response

from .models import LabelsModel, NotesModel
from rest_framework.exceptions import ValidationError
from UserAuth.models import User
from .tasks import send_mail_func

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema 

# Logger
from logger import set_logger

from .redis_test import RedisNote

logger = set_logger()


class LabelAPI(APIView):
    serializer_class = LabelSerializer

    @swagger_auto_schema(request_body=LabelSerializer)
    def post(self, request, *args, **kwargs):

        try:
            request.data.update({"user": request.user})
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {'success': True, 'message': 'Labels created successfully!', 'data': serializer.data},
                status=201)
        except ValidationError as e:
            return Response({'success': False, 'message': serializer.errors}, status=400)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    def get(self, request):

        try:
            logger.info("This is with respect to Logger")
            user_id = request.user.id
            labels = LabelsModel.objects.filter(user_id=user_id)
            serializer = LabelSerializer(labels, many=True)
            if len(serializer.data) == 0:
                raise Exception
            return Response(
                {'success': True, 'message': 'Labels got successfully', 'data': serializer.data},
                status=200)

        except LabelsModel.DoesNotExist as e:
            return Response({'success': False, 'message': 'You do not have any labels of that specifications'},
                            status=400)
        except Exception as e:
            return Response({'success': False, 'message': 'You do not have any labels of that specifications'},
                            status=400)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'label_name': openapi.Schema(type=openapi.TYPE_STRING)},
                                                     required=['id', 'label_name']),
                         operation_summary='Update Label')
    def put(self, request):

        try:
            data = dict(request.data)

            data.update({'user': request.user.id})

            labels = LabelsModel.objects.get(id=data.get('id'), user=data.get('user'))
            serializer = LabelSerializer(labels, data=data)
            serializer.is_valid(raise_exception=True)  # Check exception
            serializer.save()
            return Response(
                {'success': True, 'message': 'Labels updated successfully', 'data': serializer.data},
                status=200)

        except LabelsModel.DoesNotExist as e:
            return Response({'success': False, 'message': 'You do not have any labels of that specifications'},
                            status=400)
        except ValidationError as e:
            return Response({'success': False, 'message': serializer.errors}, status=400)

        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER)
                                                                 },
                                                     required=['id']),
                         operation_summary='Update Label')
    def delete(self, request):

        try:
            labels = LabelsModel.objects.get(id=request.data.get('id'))
            labels.delete()
            return Response(
                {'success': True, 'message': 'Labels deleted successfully', 'data': {}},
                status=200)
        except LabelsModel.DoesNotExist:
            return Response({'success': False, 'message': 'You do not have any labels of that specifications'},
                            status=400)

        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)


class NotesAPI(APIView):
    serializer_class = NotesSerializer
    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='POSTNotes')
    def post(self, request, *args, **kwargs):
        try:
            request.data.update({'user': request.user})
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote().post_notes_redis(serializer.data, request.user.id)
            return Response({'message': "Note Created Successful", "status": 200, "data": serializer.data}, status=201)

        except ValidationError as e:
            return Response({'success': False, 'message': serializer.errors}, status=400)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    def get(self, request):

        logger.info("This is with respect to Logger")
        try:
            # redis_user_notes = RedisNote().get_notes_redis(request.user.id)
            # if redis_user_notes:
            #     return Response({"message": "note from Cache", "status": 200, "data": redis_user_notes},
            #                     status=200)

            user_id = request.user.id
            notes = NotesModel.objects.filter(user_id=user_id)
            serializer = NotesSerializer(notes, many=True)
            if len(serializer.data) == 0:
                raise Exception
            return Response(
                {'success': True, 'message': 'Notes got successfully', 'data': serializer.data}, status=200)

        except NotesModel.DoesNotExist as e:
            return Response({'success': False, 'message': 'You do not have any Notes of that specifications'},
                            status=400)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'You do not have any Notes of that specifications'},
                            status=400)

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='Update Notes')
    def put(self, request):

        try:
            # data = dict(request.data)
            # data = {x: y[0] for x, y in data.items()}
            # data.update({'user': request.user.id})

            request.data.update({'user': request.user})
            notes = NotesModel.objects.get(id=request.data.get('id'), user=request.user.id)
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)  # Check exception
            serializer.save()
            RedisNote().post_notes_redis(serializer.data, request.user.id)
            return Response(
                {'success': True, 'message': 'Notes updated successfully', 'data': serializer.data},
                status=200)

        except NotesModel.DoesNotExist as e:
            return Response({'success': False, 'message': 'You do not have any notes of that specifications'},
                            status=400)
        except ValidationError as e:
            return Response({'success': False, 'message': serializer.errors}, status=400)

        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER)
                                                                 },
                                                     required=['id']),
                         operation_summary='Delete Note')
    def delete(self, request, *args, **kwargs):
        try:
            notes = NotesModel.objects.get(id=request.data.get('id'), user = request.user)
            notes.delete()
            RedisNote().delete_note_redis(request.data.get('id'), request.user.id)
            return Response(
                {'success': True, 'message': 'Notes deleted successfully', 'data': {}},
                status=200)
        except NotesModel.DoesNotExist:
            return Response({'success': False, 'message': 'You do not have any notes of that specifications'},
                            status=400)

        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)


class ArchiveNotesAPI(APIView):# Implement get API
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'isArchive': openapi.Schema(
                                                                     type=openapi.TYPE_BOOLEAN)},
                                                     required=['id', 'isArchive']),
                         operation_summary='Add notes to archive')
    def post(self, request, *args, **kwargs):
        try:
            # id = kwargs['id']
            id = request.data.get("id")
            note = NotesModel.objects.get(id=id)
            note.isArchive = not note.isArchive
            note.save()
            return Response({'success': True, 'message': 'Note Archived Successfully', 'data': NotesSerializer(note).data}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    def get(self, request):
        try:
            note = NotesModel.objects.filter(isArchive=True, isTrash=False, user=request.user)
            serializer = NotesSerializer(note, many=True)
            if len(serializer.data) == 0:
                raise Exception
            return Response({"message": "The Note is Archived", "data": serializer.data}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': "The note does not exist"}, status=400)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'isArchive': openapi.Schema(
                                                                     type=openapi.TYPE_BOOLEAN)},
                                                     required=['id', 'isArchive']),
                         operation_summary='Update archived notes')
    def put(self, request):
        try:
            note = NotesModel.objects.get(id=request.data.get('id'), user=request.user)
            note.isArchive = False
            note.save()
            return Response({"message": "Notes Update successful", "data": NotesSerializer(note).data}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]}, status=400)


class TrashNotesAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # id = kwargs['id']
            id = request.data.get("id")
            note = NotesModel.objects.get(id=id)
            note.isTrash = not note.isTrash
            note.save()
            return Response({'success': True, 'message': 'Note is Trash status changed successfully Successfully'},
                            status=200)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    def get(self, request):
        try:
            note = NotesModel.objects.filter(isTrash=True, user=request.user)
            serializer = NotesSerializer(note, many=True)
            return Response({"message": "The Deleted Notes are ", "data": serializer.data}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]}, status=400)

    def put(self, request):
        note = NotesModel.objects.get(id=request.data.get('id'), user=request.user)
        note.isTrash = False
        note.save()
        return Response({"message": "successfully restored data from trash",
                         "status": 200, "data": {}}, status=200)

class CollaboratorAPI(APIView):

    def post(self, request):
        try:
            note = NotesModel.objects.get(id=request.data.get('id'), user=request.user.id)
            for collaborator_name in request.data.get('collaborator'):
                try:
                    collaborator = User.objects.get(username=collaborator_name)
                    if collaborator_name != request.user.username:
                        note.collaborator.add(collaborator)
                    else:
                        raise Exception
                except:
                    pass

            return Response({"message": "A new Collaborator was added", "status": 200, "data": {}},
                            status=200)
        except Exception as e:
            return Response({"message": e.args[0], "status": 400, "data": {}},
                            status=400)

    def delete(self, request): #Refactor and compress the activity, lookup in django ORM, ORM queries  and for consume time
        try:
            note = NotesModel.objects.get(id=request.data.get('id'), user=request.user.id)
            error_list = []
            for collaborator_name in request.data.get('collaborator'):
                collaborator = User.objects.filter(username=collaborator_name)
                if collaborator.exists():
                    if collaborator in note.collaborator.all():
                        note.collaborator.remove(collaborator)
                    else:
                        error_list.append(collaborator_name)
                else:
                    error_list.append(collaborator_name)

            if len(error_list) == 0:
                return Response({"message": "collaborator removed  successfully", "status": 200, "data": {}},
                                    status=200)

            return Response({"message": f"All Collaborator removed except {','.join(error_list)}", "status": 404, "data": {}},
                                    status=404)
        except Exception as e:
            return Response({"message": e.args[0], "status": 400, "data": {}},
                            status=400)

# get method use combination of filter and or, wrt to user and collaborator
# https://docs.python.org/3/howto/logging.html
# https://drf-yasg.readthedocs.io/en/stable/custom_spec.html

#
# https://www.scottbrady91.com/aspnet-identity/improving-the-aspnet-core-identity-password-hasher#:~:text=Alternatives%20to%20PBKDF2&text=Argon2%20(winner%20of%20the%20Password,in%20the%20Password%20Hashing%20Competition)
# https://medium.com/@cjainn/top-password-hashing-schemes-to-employ-today-98d270f48802
# https://auth0.com/blog/hashing-passwords-one-way-road-to-security/
# https://www.loginradius.com/blog/engineering/jwt-signing-algorithms/

