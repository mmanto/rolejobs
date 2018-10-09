# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-11 22:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0018_auto_20161111_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobModerationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.IntegerField(choices=[(20, 'Suspendido'), (30, 'Baneado'), (99, 'Borrador'), (0, 'Pendiente'), (1, 'Habilitado')], default=99, verbose_name='Cambiado de')),
                ('new_status', models.IntegerField(choices=[(20, 'Suspendido'), (30, 'Baneado'), (99, 'Borrador'), (0, 'Pendiente'), (1, 'Habilitado')], default=99, verbose_name='Cambiado a')),
                ('action_date', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(blank=True, max_length=512, null=True, verbose_name='Raz\xf3n')),
                ('action_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Moderado por')),
            ],
        ),
        migrations.AlterField(
            model_name='job',
            name='published',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.IntegerField(choices=[(20, 'Suspendido'), (30, 'Baneado'), (99, 'Borrador'), (0, 'Pendiente'), (1, 'Habilitado')], default=0),
        ),
        migrations.AddField(
            model_name='jobmoderationhistory',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderation_history', to='jobs.Job'),
        ),
    ]
