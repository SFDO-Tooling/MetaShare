# Generated by Django 3.0.5 on 2020-04-14 16:48

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0067_cascade_slug_deletion"),
    ]

    operations = [
        migrations.AddField(
            model_name="scratchorg",
            name="ignored_changes",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                encoder=django.core.serializers.json.DjangoJSONEncoder,
            ),
        ),
    ]
