from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project
from .serializers import ProjectSerializer


class ProjectView(APIView):
    def get(self, *args, **kwargs):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


def update_data_sharing(user):
    if user.age >= 15:
        user.can_data_be_shared = True
        user.save()
