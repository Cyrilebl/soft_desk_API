from django.contrib import admin
from django.urls import path, include
from api.views import ProjectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/project/", ProjectView.as_view()),
]
