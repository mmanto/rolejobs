# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-02 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_last_profile_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='completed_items',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
