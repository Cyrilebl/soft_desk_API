from rest_framework.permissions import BasePermission
from .models import Project, Contributor


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or Contributor.objects.filter(user=request.user, project=obj).exists()
        )


class IsProjectAuthorOrContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.project.author == request.user
            or Contributor.objects.filter(
                user=request.user, project=obj.project
            ).exists()
        )


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        project_id = request.data.get("project")
        project = Project.objects.filter(id=project_id).first()
        return project and project.author == request.user

    def has_object_permission(self, request, view, obj):
        return obj.project.author == request.user
