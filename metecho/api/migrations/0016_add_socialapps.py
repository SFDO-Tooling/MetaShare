# Generated by Django 2.2.5 on 2019-09-16 19:37

from os import environ

from django.db import migrations


def forwards(apps, schema_editor):
    client_id = environ.get("SFDX_CLIENT_ID")
    secret = environ.get("SFDX_CLIENT_SECRET")
    if client_id and secret:
        SocialApp = apps.get_model("socialaccount", "SocialApp")
        SocialApp.objects.get_or_create(
            provider="salesforce-production",
            defaults=dict(
                name="Salesforce Production",
                key="https://login.salesforce.com/",
                client_id=client_id,
                secret=secret,
            ),
        )


def backwards(apps, schema_editor):
    SocialApp = apps.get_model("socialaccount", "SocialApp")
    SocialApp.objects.filter(provider="salesforce-production").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_scratchorg_config_encoder"),
        ("socialaccount", "0003_extra_data_default_dict"),
    ]

    operations = [migrations.RunPython(forwards, backwards)]
