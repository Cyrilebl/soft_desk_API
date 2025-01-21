from rest_framework.serializers import ModelSerializer

from .models import Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["author", "name", "description", "type", "created_time"]
