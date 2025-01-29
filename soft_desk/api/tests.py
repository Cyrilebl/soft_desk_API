from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from .models import User, Project, Issue, Comment


class TestUser(APITestCase):
    url = reverse_lazy("user")

    def test_create(self):
        self.assertFalse(User.objects.exists())

        response = self.client.post(
            self.url,
            data={
                "username": "testuser",
                "password": "password123",
                "email": "test@exemple.fr",
                "age": 30,
            },
        )
        self.assertEqual(response.status_code, 201)
        user = User.objects.first()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@exemple.fr")
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(user.age, 20)


class TestProject(APITestCase):
    def setUp(self):
        self.url = reverse_lazy("project-list")
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            age=18,
        )
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(
            name="Project test",
            description="Ceci est une description",
            type="Back-end",
            author=self.user,
        )

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        excepted = {
            "id": self.project.pk,
            "name": self.project.name,
            "description": self.project.description,
            "type": self.project.type,
            "created_time": self.format_datetime(self.project.created_time),
        }
        self.assertEqual(excepted, response.json())

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


"""class TestIssue(APITestCase):
    def test_create_issue(self):
        project = Project.objects.create(name="Test Project", author=self.user)

        response = self.client.post(
            "/api/issues/",
            data={
                "title": "Bug critique",
                "description": "Un bug important",
                "project": project.id,
            },
        )

        self.assertEqual(response.status_code, 201)
        issue = Issue.objects.get()
        self.assertEqual(issue.author, self.user)"""


# Un utilisateur non autorisé ne peut pas ajouter d'issues.
# L'auteur d'un projet peut ajouter des issues.
# Un contributeur peut ajouter des issues.


class TestComment(APITestCase):
    pass
