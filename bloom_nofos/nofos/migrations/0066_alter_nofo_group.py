# Generated by Django 4.2.10 on 2024-07-02 16:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nofos", "0065_suggest_nofo_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nofo",
            name="group",
            field=models.CharField(
                choices=[
                    ("bloom", "Bloomworks"),
                    ("acf", "ACF: Administration for Children and Families"),
                    ("acl", "ACL: Administration for Community Living"),
                    (
                        "aspr",
                        "ASPR: Administration for Strategic Preparedness and Response",
                    ),
                    ("cdc", "CDC: Centers for Disease Control and Prevention"),
                    ("cms", "CMS: Centers for Medicare & Medicaid Services"),
                    ("hrsa", "HRSA: Health Resources and Services Administration"),
                    ("ihs", "IHS: Indian Health Service"),
                ],
                default="bloom",
                help_text="The OpDiv grouping of this NOFO. The group is used to control access to a NOFO.",
                max_length=16,
            ),
        ),
    ]
