from rest_framework import serializers
from .models import LabelsModel, NotesModel
from UserAuth.models import User

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelsModel
        fields = ['id', 'label_name', 'user']
        read_only_fields = ['user']

    def create(self, validated_data):

        try:
            label = LabelsModel.objects.get(label_name=validated_data.get("label_name"),
                                            user=self.initial_data.get("user"))
        except:
            label = LabelsModel.objects.create(label_name=validated_data.get("label_name"),
                                               user=self.initial_data.get("user"))

        return label

class NotesSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField()

    class Meta:
        model = NotesModel
        fields = ['user', 'title', 'description', 'label', 'collaborator', 'reminder', 'image']
        read_only_fields = ['collaborator', 'label', 'user']

    def create(self, validated_data):

        validated_data.update({"user": self.initial_data.get("user")})
        new_note = NotesModel.objects.create(**validated_data)
        labels = self.initial_data.get("label")
        collaborators = self.initial_data.get('collaborator')
        if labels:
            for label in labels:
                try:
                    label_add = LabelsModel.objects.get(label_name=label, user=validated_data.get("user"))
                except:
                    label_add = LabelsModel.objects.create(label_name=label, user=validated_data.get("user"))
                new_note.label.add(label_add)

        if collaborators:
            for collaborator in collaborators:
                try:
                    user = User.objects.get(username = collaborator)
                except:
                    pass
                new_note.collaborator.add(user)
        return new_note

