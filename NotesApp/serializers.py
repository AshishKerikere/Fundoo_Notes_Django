from rest_framework import serializers
from .models import LabelsModel, NotesModel
from django.http import Http404

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
        fields = ['user', 'title', 'description', 'label', 'collaborator']
        read_only_fields = ['collaborator', 'label', 'user']

    def create(self, validated_data):

        validated_data.update({"user": self.initial_data.get("user")})
        new_note = NotesModel.objects.create(**validated_data)
        labels = self.initial_data.get("label")
        if labels:
            for label in labels:
                try:
                    label_add = LabelsModel.objects.get(label_name=label, user=validated_data.get("user"))
                except:
                    label_add = LabelsModel.objects.create(label_name=label, user=validated_data.get("user"))
                new_note.label.add(label_add)
        return new_note

