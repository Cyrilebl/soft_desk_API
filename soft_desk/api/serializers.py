from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User, Project, Contributor, Issue, Comment


class UserSerializer(ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "age", "projects"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError(
                "You must be at least 15 years old to register."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_projects(self, obj):
        projects = obj.projects.all()
        request = self.context.get("request")
        serializer = ProjectListSerializer(
            projects, many=True, context={"request": request}
        )
        return serializer.data


class ProjectListSerializer(ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name="api:project-detail", read_only=True
    )

    class Meta:
        model = Project
        fields = ["id", "name", "detail"]


class ProjectDetailSerializer(ModelSerializer):
    issues = serializers.SerializerMethodField()
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "type",
            "author",
            "created_time",
            "issues",
        ]

    def get_issues(self, obj):
        issues = obj.issues.all()
        request = self.context.get("request")
        serializer = IssueListSerializer(
            issues, many=True, context={"request": request}
        )
        return serializer.data


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = "__all__"


class IssueListSerializer(ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name="api:issue-detail", read_only=True
    )
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = ["id", "author", "name", "detail"]


class IssueDetailSerializer(ModelSerializer):
    comments = serializers.SerializerMethodField()
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "project",
            "author",
            "name",
            "description",
            "status",
            "priority",
            "tag",
            "created_time",
            "comments",
        ]

    def get_comments(self, obj):
        comments = obj.comments.all()
        request = self.context.get("request")
        serializer = CommentListSerializer(
            comments, many=True, context={"request": request}
        )
        return serializer.data


class CommentListSerializer(ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name="api:comment-detail", read_only=True
    )
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "detail"]


class CommentDetailSerializer(ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "issue", "author", "description", "created_time"]
