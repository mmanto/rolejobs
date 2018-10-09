# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 22:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidades.Departamento')),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Localidades',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Paises',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('pais', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='localidades.Pais')),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Provincias',
            },
        ),
        migrations.AddField(
            model_name='localidad',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidades.Provincia'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidades.Provincia'),
        ),
    ]
