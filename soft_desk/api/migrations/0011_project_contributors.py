# Generated by Django 5.1.5 on 2025-02-12 10:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(through='api.Contributor', to=settings.AUTH_USER_MODEL),
        ),
    ]
