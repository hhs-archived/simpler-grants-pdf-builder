# Generated by Django 5.0.8 on 2024-11-04 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nofos", "0074_alter_nofo_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nofo",
            name="cover",
            field=models.CharField(
                choices=[
                    ("nofo--cover-page--hero", "Full coverage with image"),
                    ("nofo--cover-page--medium", "Standard image"),
                    ("nofo--cover-page--text", "Text only"),
                ],
                default="nofo--cover-page--medium",
                help_text="The cover style for the NOFO.",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="nofo",
            name="icon_style",
            field=models.CharField(
                choices=[
                    (
                        "nofo--icons--border",
                        "(Filled) Color background, white icon, white outline",
                    ),
                    (
                        "nofo--icons--solid",
                        "(Outlined) White background, color icon, color outline",
                    ),
                    (
                        "nofo--icons--thin",
                        "(Thin) Thin icons with white background, color icon, color outline",
                    ),
                ],
                default="nofo--icons--border",
                help_text="Defines the icon style on section cover pages.",
                max_length=32,
            ),
        ),
    ]
