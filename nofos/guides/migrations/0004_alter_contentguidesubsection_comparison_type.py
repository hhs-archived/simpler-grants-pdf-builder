# Generated by Django 5.0.13 on 2025-04-14 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guides", "0003_contentguidesection_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contentguidesubsection",
            name="comparison_type",
            field=models.CharField(
                choices=[
                    ("none", "Do not compare"),
                    ("name", "Compare name"),
                    ("body", "Compare name and all text"),
                    ("diff_strings", "Compare name and required strings"),
                ],
                default="name",
                max_length=20,
            ),
        ),
    ]
