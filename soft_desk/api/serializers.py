from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User, Project, Contributor, Issue, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "age",
        ]

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError(
                "You must be at least 15 years old to register."
            )
        return value


class ProjectSerializer(ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    created_time = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "author",
            "name",
            "description",
            "type",
            "created_time",
        ]


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = "__all__"


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
            "project",
            "name",
            "description",
            "status",
            "priority",
            "tag",
            "created_time",
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "issue",
            "description",
            "created_time",
        ]
