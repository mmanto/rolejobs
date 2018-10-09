# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import os

from utils.migrations import LoadFixtureDir


@LoadFixtureDir
def load_fixture():
    return os.path.abspath(os.path.join(
                           os.path.dirname(__file__), '../fixtures/0015'))


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_knowledgerequirement'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
