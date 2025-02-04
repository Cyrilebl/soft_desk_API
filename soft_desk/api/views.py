from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User, Project, Contributor, Issue, Comment
from .serializers import (
    UserSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
    IssueDetailSerializer,
    CommentDetailSerializer,
)
from .permissions import IsAuthor, IsProjectAuthor, CanCreateIssue, CanCreateComment


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Any user can create an account
        """
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save()


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    """
    Every authenticated users can create.
    Only author and contributors can read.
    Only author can update/delete.
    """

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthor()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(author=user) | Project.objects.filter(
            contributors=user
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        user = self.request.user
        return Contributor.objects.filter(project__author=user)

    def perform_create(self, serializer):
        user_id = self.request.data.get("user")
        project_id = self.request.data.get("project")

        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)

        if user == project.author:
            raise ValidationError(
                ({"user": "The project author cannot add themselves as a contributor."})
            )

        serializer.save(user=user, project=project)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueDetailSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsAuthenticated, CanCreateIssue]
    """
    Every author or contributor of the project can create/read.
    Only author can update/delete.
    """

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthor()]

        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(
            Q(author=user) | Q(project__author=user) | Q(project__contributors=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, CanCreateComment]
    """
    Every author or contributor of the project can create/read.
    Only author can update/delete.
    """

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthor()]

        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(
            Q(author=user)
            | Q(issue__project__author=user)
            | Q(issue__project__contributors=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
