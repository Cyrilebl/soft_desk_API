from rest_framework.permissions import BasePermission
from .models import Project, Contributor, Issue


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


# For Contributor
class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        if view.action == "list":
            return True

        # Request with URL ID
        contributor_id = view.kwargs.get("pk")
        if contributor_id:
            contributor = (
                Contributor.objects.filter(id=contributor_id)
                .select_related("project")
                .first()
            )
            return contributor.project.author == request.user

        # Requst with no URL ID
        project_id = request.data.get("project")
        if project_id:
            project = Project.objects.filter(id=project_id).first()
            return project and project.author == request.user

        return False

    def has_object_permission(self, request, view, obj):
        return obj.project.author == request.user


# For Issue
class CanCreateIssue(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            project_id = request.data.get("project")
            project = Project.objects.get(id=project_id)

            user = request.user

            return (
                user == project.author
                or Contributor.objects.filter(user=user, project=project).exists()
            )
        return True


# For Comment
class CanCreateComment(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            issue_id = request.data.get("issue")
            issue = Issue.objects.select_related("project").get(id=issue_id)

            project = issue.project
            user = request.user

            return (
                user == project.author
                or Contributor.objects.filter(user=user, project=project).exists()
            )
        return True
