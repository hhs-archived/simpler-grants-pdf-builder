# Generated by Django 5.0.8 on 2025-02-26 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nofos", "0090_add_public_information_subsection"),
    ]

    operations = [
        migrations.AddField(
            model_name="nofo",
            name="modifications",
            field=models.DateField(
                blank=True,
                default=None,
                help_text="If this NOFO has post-publishing modifications. Adds a message to the cover page and a “Modifications”\xa0section to the end of the NOFO.",
                null=True,
            ),
        ),
    ]
