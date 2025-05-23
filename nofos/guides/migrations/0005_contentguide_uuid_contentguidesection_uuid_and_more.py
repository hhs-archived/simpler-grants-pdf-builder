# Generated by Django 5.0.13 on 2025-05-05 19:29

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guides", "0004_alter_contentguidesubsection_comparison_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="contentguide",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name="contentguidesection",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name="contentguidesubsection",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
