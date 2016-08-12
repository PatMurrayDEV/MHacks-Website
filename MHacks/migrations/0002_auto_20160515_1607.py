# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-15 21:07
from __future__ import unicode_literals

from django.db import migrations


def create_groups(apps, schema_editor):
    # create_permissions(apps.get_app_config('MHacks'))

    group_model = apps.get_model('auth', model_name='group')
    permission_model = apps.get_model('auth', model_name='permission')

    from MHacks.globals import groups
    group_model.objects.bulk_create(map(lambda g: group_model(name=g), (groups.HACKER,
                                                                        groups.SPONSOR,
                                                                        groups.APP_READER,
                                                                        groups.STATS)))

    def add_permissions(group_name, permission_list):
        group = group_model.objects.get(name=group_name)
        permissions = map(lambda p: permission_model.objects.get(codename=p), permission_list)
        for x in permissions:
            group.permissions.add(x)

    add_permissions(groups.HACKER, ['add_pushtoken', 'change_pushtoken', 'add_application', 'change_application'])
    add_permissions(groups.SPONSOR, ['add_event', 'add_announcement'])
    add_permissions(groups.APP_READER, ['add_application', 'change_application', 'delete_application'])
    add_permissions(groups.STATS, [])


class Migration(migrations.Migration):

    dependencies = [
        ('MHacks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code=create_groups)
    ]
