# Generated by Django 2.2.5 on 2019-09-17 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api", "0016_scratchorg_currently_refreshing_changes")]

    operations = [
        migrations.AddField(
            model_name="scratchorg",
            name="delete_queued_at",
            field=models.DateTimeField(null=True),
        )
    ]
