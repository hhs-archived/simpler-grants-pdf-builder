# Generated by Django 5.0.8 on 2024-12-04 16:33

import json
import re

from django.db import migrations


def cleanup_update_print_logs(apps, schema_editor):
    # Get the audit log model
    AuditLog = apps.get_model("easyaudit", "CRUDEvent")

    # Simplified regex pattern
    live_pattern = r"PRINT: NOFO id #\d+ at (.+)"

    # Fetch all relevant audit logs
    audit_logs = AuditLog.objects.filter(changed_fields__startswith="PRINT: NOFO id")

    for log in audit_logs:
        match = re.match(live_pattern, log.changed_fields)

        if match:
            timestamp = match.group(1)  # Extract the timestamp

            # Construct the JSON structure
            log.changed_fields = json.dumps(
                {"action": "nofo_print", "print_mode": ["live"], "updated": [timestamp]}
            )

            # Save the updated log
            log.save()


class Migration(migrations.Migration):
    dependencies = [
        ("nofos", "0078_alter_nofo_designer"),
    ]

    operations = [
        migrations.RunPython(cleanup_update_print_logs),
    ]
