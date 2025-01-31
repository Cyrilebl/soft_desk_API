from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    UserViewSet,
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)


app_name = "api"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"contributors", ContributorViewSet, basename="contributor")
router.register(r"issues", IssueViewSet, basename="issue")
router.register(r"comments", CommentViewSet, basename="comment")

api_patterns = (router.urls, app_name)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(api_patterns, namespace=app_name)),
]
