import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class User(AbstractUser):
    age = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(100)],
        default=0,
    )
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)


class Project(models.Model):
    BACKEND = "BACKEND"
    FRONTEND = "FRONTEND"
    IOS = "IOS"
    ANDROID = "ANDROID"
    TYPES_CHOICES = (
        (BACKEND, "Back-end"),
        (FRONTEND, "Front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    )

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    type = models.CharField(max_length=8, choices=TYPES_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Issue(models.Model):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    STATUS_CHOICES = (
        (TODO, "To Do"),
        (IN_PROGRESS, "In Progress"),
        (FINISHED, "Finished"),
    )
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    PRIORITY_CHOICES = (
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    )
    BUG = "BUG"
    FEATURE = "FEATURE"
    TASK = "TASK"
    TAG_CHOICES = (
        (BUG, "Bug"),
        (FEATURE, "Feature"),
        (TASK, "Task"),
    )

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=7, choices=TAG_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"


class Comment(models.Model):
    comment_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    linked_to = models.ForeignKey(to="Issue", on_delete=models.CASCADE)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on Issue {self.linked_to}"
