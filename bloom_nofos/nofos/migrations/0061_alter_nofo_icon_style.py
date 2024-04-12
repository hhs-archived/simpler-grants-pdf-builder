# Generated by Django 4.2.10 on 2024-04-12 22:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nofos", "0060_alter_nofo_icon_style"),
    ]

    operations = [
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
                        "(Standard) White background, color icon, color outline",
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
