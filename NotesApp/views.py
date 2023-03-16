from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LabelSerializer, NotesSerializer
from rest_framework.response import Response
from UserAuth.utils import SessionAuth
from rest_framework.permissions import IsAuthenticated
from UserAuth.models import User
from django.http import Http404
from .models import LabelsModel, NotesModel
from rest_framework.exceptions import ValidationError
from .tasks import send_mail_func

#for jwt
from rest_framework_simplejwt.authentication import JWTAuthentication

#Logger
from logger import set_logger
logger = set_logger()

class LabelAPI(APIView):
    serializer_class = LabelSerializer
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [SessionAuth]

    def post(self, request, *args, **kwargs):

        """data = dict(request.data)
        data = {x:y[0] for x,y in data.items()}
        data.update({'user':request.user.id})
        print(data)"""
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
            return Response(
                {'success': True, 'message': 'Labels got successfully', 'data': serializer.data},
                status=200)

        except labels.DoesNotExist as e:
            return Response({'success': False, 'message': 'You do not have any labels of that specifications'},
                            status=400)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    def put(self, request):

        try:
            data = dict(request.data)
            # data = {x: y[0] for x, y in data.items()}
            data.update({'user': request.user.id})

            labels = LabelsModel.objects.get(id=data.get('id'), user=data.get('user'))
            serializer = LabelSerializer(labels, data=data)
            serializer.is_valid(raise_exception=True)  # Check exception
            serializer.save()
            return Response(
                {'success': True, 'message': 'Labels updated successfully', 'data': serializer.data},
                status=200)

        except labels.DoesNotExist as e:
            return Response({'success': False, 'message': 'You do not have any labels of that specifications'},
                            status=400)
        except ValidationError as e:
            return Response({'success': False, 'message': serializer.errors}, status=400)

        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    def delete(self, request):

        try:
            labels = LabelsModel.objects.get(id=request.data.get('id'), user=request.user.id)
            labels.delete()
            return Response(
                {'success': True, 'message': 'Labels deleted successfully', 'data': {}},
                status=204)
        except labels.DoesNotExist:
            return Response({'success': False, 'message': 'You do not have any labels of that specifications'},
                            status=400)

        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)


class NotesAPI(APIView):
    serializer_class = NotesSerializer
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [SessionAuth]

    def post(self, request, *args, **kwargs):
        """data = dict(request.data)
        data = {x: y[0] for x, y in data.items()}"""
        try:
            request.data.update({'user': request.user})
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # return super(LabelAPI, self).post(request, format=None)
            return Response({'message': "Note Created Successful", "status": 200, "data": serializer.data}, status=201)

        except ValidationError as e:
            return Response({'success': False, 'message': serializer.errors}, status=400)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    def get(self, request):

        try:
            logger.info("This is with respect to Logger")
            user_id = request.user.id
            notes = NotesModel.objects.filter(user_id=user_id)
            serializer = NotesSerializer(notes, many=True)
            return Response(
                {'success': True, 'message': 'Notes got successfully', 'data': serializer.data}, status=200)

        except NotesModel.DoesNotExist as e:
            return Response({'success': False, 'message': 'You do not have any Notes of that specifications'},
                            status=400)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    def put(self, request):

        try:
            data = dict(request.data)
            data = {x: y[0] for x, y in data.items()}
            data.update({'user': request.user.id})

            notes = NotesModel.objects.get(id=data.get('id'), user=data.get('user'))
            serializer = NotesSerializer(notes, data=data)
            serializer.is_valid(raise_exception=True)  # Check exception
            serializer.save()
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


class DeleteNotesAPI(APIView): #Implement in the same class
    serializer_class = NotesSerializer
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [SessionAuth]

    def delete(self, request, *args, **kwargs):

        try:
            id = kwargs['id'] #Check for id type
            notes = NotesModel.objects.get(id=id)
            notes.delete()
            return Response(
                {'success': True, 'message': 'Notes deleted successfully', 'data': {}},
                status=204)
        except NotesModel.DoesNotExist:
            return Response({'success': False, 'message': 'You do not have any notes of that specifications'},
                            status=400)

        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)


class ArchiveNotesAPI(APIView):# Implement get API
    def post(self, request, *args, **kwargs):
        try:
            #id = kwargs['id']
            id = request.data.get("id")
            note = NotesModel.objects.get(id=id)
            note.isArchive = not note.isArchive
            note.save()
            return Response({'success': True, 'message': 'Note Archived Successfully'}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]},
                            status=400)

    def get(self, request):
        try:
            note = NotesModel.objects.filter(isArchive=True, isTrash=False, user=request.user)
            serializer = NotesSerializer(note, many=True)
            return Response({"message": "The Note is Archived", "data": serializer.data}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]}, status=400)

    def put(self, request):
        try:
            note = NotesModel.objects.get(id=request.data.get('id'), user=request.user)
            note.is_archive = False
            note.save()
            return Response({"message": "Notes Update successful", "data": {}}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': e.args[0]}, status=400)


class TrashNotesAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            #id = kwargs['id']
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
            note = NotesModel.objects.filter(is_trash=True, user=request.user)
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

# Create your views here.
#For reminders

#https://docs.python.org/3/howto/logging.html
#https://drf-yasg.readthedocs.io/en/stable/custom_spec.html
