from django.db.models import Q
from rest_framework.exceptions import ValidationError, PermissionDenied
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
from .permissions import (
    IsAuthor,
    IsAuthorOrContributor,
    IsProjectAuthorOrContributor,
    IsProjectAuthor,
)


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

    def get_permissions(self):
        """
        Every authenticated users can create.
        Only author and contributors can read.
        Only author can update/delete.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthorOrContributor()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthor()]

        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = [IsAuthenticated]

    http_method_names = ["get", "post", "delete"]

    def get_permissions(self):
        """
        Only authenticated users and project author can create/read/delete.
        """
        if self.action in ["create", "list", "retrieve", "destroy"]:
            return [IsProjectAuthor()]
        return super().get_permissions()

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
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Every author or contributor of the project can create/read.
        Only author can update/delete.
        """
        if self.action in ["list", "retrieve"]:
            return [IsProjectAuthorOrContributor()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthor()]

        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(Q(author=user) | Q(contributors__user=user))
        return Issue.object.filter(project__in=projects)

    def perform_create(self, serializer):
        project_id = self.request.data.get("project")
        project = Project.objects.get(id=project_id)

        user = self.request.user

        if (
            not Contributor.objects.filter(user=user, project=project).exists()
            and user != project.author
        ):
            raise PermissionDenied(
                "You must be a contributor or the author of the project to create an issue."
            )

        serializer.save(author=user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Every author or contributor of the project can create/read.
        Only author can update/delete.
        """
        if self.action in ["list", "retrieve"]:
            return [IsProjectAuthorOrContributor()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthor()]

        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(Q(author=user) | Q(contributors__user=user))
        return Comment.object.filter(project__in=projects)

    def perform_create(self, serializer):
        issue_id = self.request.data.get("issue")
        issue = Issue.objects.get(id=issue_id)

        user = self.request.user
        project = issue.project
        if (
            not Contributor.objects.filter(
                user=self.request.user, project=project
            ).exists()
            and user != project.author
        ):
            raise PermissionDenied(
                "You must be a contributor or the author of the project to create a comment."
            )

        serializer.save(author=self.request.user)
