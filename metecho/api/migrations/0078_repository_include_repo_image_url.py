# Generated by Django 3.0.6 on 2020-05-28 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0077_merge_20200528_1806"),
    ]

    operations = [
        migrations.AddField(
            model_name="repository",
            name="include_repo_image_url",
            field=models.BooleanField(default=True),
        ),
    ]
