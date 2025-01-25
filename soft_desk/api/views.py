from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.viewsets import ModelViewSet

from .models import User, Project, Contributor, Issue, Comment
from .serializers import (
    UserSerializer,
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()

        project_id = self.request.GET.get("id")
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        queryset = Contributor.objects.all()

        # Filter by project if parameter is provided
        project_id = self.request.query_params.get("project")
        if project_id:
            queryset = queryset.filter(project__id=project_id)

        return queryset

    def get_object_by_id(self, model, object_id, field_name):
        if not object_id:
            raise ValidationError({field_name: "This field is required."})
        try:
            return model.objects.get(id=object_id)
        except model.DoesNotExist:
            raise ValidationError({field_name: f"Invalid {field_name} ID."})

    def perform_create(self, serializer):
        user_id = self.request.data.get("user")
        user = self.get_object_by_id(User, user_id, "user")

        project_id = self.request.data.get("project")
        project = self.get_object_by_id(Project, project_id, "project")

        if project.author != self.request.user:
            raise PermissionDenied(
                "You are not allowed to add contributors to this project."
            )

        serializer.save(project=project, user=user)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()

        project_id = self.request.query_params.get("project")
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    def perform_create(self, serializer):
        project_id = self.request.data.get("project")
        if not project_id:
            raise ValidationError({"project": "This field is required."})
        # Vérifier que le projet existe
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValidationError({"project": "Invalid project ID."})

        # Vérifier que l'utilisateur est l'auteur ou un contributeur du projet
        if (
            project.author != self.request.user
            and not project.contributor_set.filter(user=self.request.user).exists()
        ):
            raise PermissionDenied(
                "You do not have permission to add an issue to this project."
            )
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(ModelViewSet):
    pass
