# Generated by Django 3.0.6 on 2020-05-28 19:49

import sfdo_template_helpers.fields.string
from django.db import migrations


def forwards(apps, schema_editor):
    Task = apps.get_model("api", "Task")
    Task.objects.update(org_config_name="dev")


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0076_merge_20200528_1808"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="org_config_name",
            field=sfdo_template_helpers.fields.string.StringField(blank=True),
        ),
        migrations.AlterField(
            model_name="scratchorg",
            name="org_type",
            field=sfdo_template_helpers.fields.string.StringField(
                choices=[("Dev", "Dev"), ("QA", "QA")]
            ),
        ),
        # Set default values on org_config_name
        migrations.RunPython(forwards, backwards),
        # Remove blank=True on org_config_name
        migrations.AlterField(
            model_name="task",
            name="org_config_name",
            field=sfdo_template_helpers.fields.string.StringField(),
        ),
    ]
