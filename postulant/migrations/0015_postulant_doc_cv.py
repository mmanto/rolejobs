# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-02-13 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postulant', '0014_postulant_video_cv'),
    ]

    operations = [
        migrations.AddField(
            model_name='postulant',
            name='doc_cv',
            field=models.FileField(null=True, upload_to=b'docs/', verbose_name=b'Doc CV'),
        ),
    ]
