# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-22 07:33
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MHacks', '0010_application_decision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='reimbursement',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(limit_value=0.0)]),
        ),
    ]
