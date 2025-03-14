# Generated by Django 5.1.5 on 2025-01-24 13:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_contributor_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='linked_to',
        ),
        migrations.AddField(
            model_name='comment',
            name='issue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.issue'),
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='api.project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
