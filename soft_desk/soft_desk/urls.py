from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import (
    UserViewSet,
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)

router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="user")
router.register("projects", ProjectViewSet, basename="project")
router.register("contributors", ContributorViewSet, basename="contributor")
router.register("issues", IssueViewSet, basename="issue")
router.register("comments", CommentViewSet, basename="comment")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]
