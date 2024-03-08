# Generated by Django 4.2.10 on 2024-03-08 20:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nofos", "0048_nofo_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nofo",
            name="theme",
            field=models.CharField(
                choices=[
                    ("landscape-cdc-blue", "CDC Landscape (Default)"),
                    ("landscape-cdc-white", "CDC Landscape (Light)"),
                    ("portrait-cdc-dop", "CDC Portrait (DOP)"),
                    ("portrait-cdc-orr", "CDC Portrait (ORR)"),
                    ("portrait-cdc-blue", "CDC Portrait (Default)"),
                    ("portrait-cdc-white", "CDC Portrait (Light)"),
                    ("portrait-acf-white", "ACF (Light)"),
                    ("portrait-acl-white", "ACL (Default)"),
                    ("portrait-cms-white", "CMS (Light)"),
                    ("portrait-hrsa-blue", "HRSA (Default)"),
                    ("portrait-hrsa-white", "HRSA (Light)"),
                    ("portrait-ihs-white", "IHS (Light)"),
                ],
                default="portrait-hrsa-blue",
                help_text="The theme sets the orientation and colour pallete for this NOFO.",
                max_length=32,
            ),
        ),
    ]
