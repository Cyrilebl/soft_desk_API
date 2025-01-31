from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied,
    MethodNotAllowed,
)
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    def get_permissions(self):
        """
        Disable PUT / PATCH.
        """
        if self.action in ["update", "partial_update"]:
            raise MethodNotAllowed(
                "PUT and PATCH methods are not allowed for contributors."
            )
        return super().get_permissions()

    def perform_create(self, serializer):
        user_id = self.request.data.get("user")
        project_id = self.request.data.get("project")

        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)

        if project.author != self.request.user:
            raise PermissionDenied(
                "You are not allowed to add contributors to this project."
            )
        if user == project.author:
            raise ValidationError(
                ({"user": "The project author cannot add themselves as a contributor."})
            )

        serializer.save(user=user, project=project)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueDetailSerializer
    queryset = Issue.objects.all()

    def perform_create(self, serializer):
        project_id = self.request.data.get("project")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise PermissionDenied("Invalid project ID.")

        if (
            not Contributor.objects.filter(
                user=self.request.user, project=project
            ).exists()
            and project.author != self.request.user
        ):
            raise PermissionDenied(
                "You must be a contributor or the author of the project to create an issue."
            )

        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        issue_id = self.request.data.get("issue")
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise PermissionDenied("Invalid issue ID.")

        project = issue.project
        if (
            not Contributor.objects.filter(
                user=self.request.user, project=project
            ).exists()
            and project.author != self.request.user
        ):
            raise PermissionDenied(
                "You must be a contributor or the author of the issue to create an issue."
            )

        serializer.save(author=self.request.user)
