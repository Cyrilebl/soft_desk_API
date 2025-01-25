from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from .models import User, Project


class TestUser(APITestCase):
    url = reverse_lazy("user")

    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser", password="password123", age=25
        )
        self.assertEqual(user.username, "testuser")


class TestProject(APITestCase):
    def setUp(self):
        self.url = reverse_lazy("project-list")
        self.user = User.objects.create(
            username="testuser",
            password="password123",
            age=18,
        )
        self.client.force_authenticate(user=self.user)

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):
        project = Project.objects.create(
            name="Super App",
            description="Test description",
            type="Back-end",
            author=self.user,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        expected = [
            {
                "id": project.pk,
                "name": project.name,
                "description": project.description,
                "type": project.type,
                "created_time": self.format_datetime(project.created_time),
                "author": self.user.id,
            }
        ]
        self.assertEqual(expected, response.json())

    def test_create(self):
        self.assertFalse(Project.objects.exists())

        response = self.client.post(
            self.url,
            data={
                "name": "Nouveau projet",
                "description": "Test description",
                "type": "BACKEND",
            },
        )
        self.assertEqual(response.status_code, 201)
        project = Project.objects.first()
        self.assertIsNotNone(project)
        self.assertEqual(project.name, "Nouveau projet")
        self.assertEqual(project.author, self.user)


class TestContributor(APITestCase):
    pass


class TestIssue(APITestCase):
    pass


# Un utilisateur non autorisé ne peut pas ajouter d'issues.
# L'auteur d'un projet peut ajouter des issues.
# Un contributeur peut ajouter des issues.


class TestComment(APITestCase):
    pass
