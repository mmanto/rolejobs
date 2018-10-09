# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core import serializers


class LoadFixtureDir(object):

    def __init__(self, f):
        self._get_path = f

    def __call__(self, apps, schema_editor):
        fixtures_dir = self._get_path()

        files = [os.path.join(fixtures_dir, f) for f in os.listdir(
                fixtures_dir) if os.path.isfile(
                    os.path.join(fixtures_dir, f))]

        for fixture_file in files:
            self.load_fixture_file(fixture_file)

    def load_fixture_file(self, fixture_file):
        fixture = open(fixture_file, 'rb')
        objects = serializers.deserialize('json', fixture,
                                          ignorenonexistent=True)
        for obj in objects:
            obj.save()

        fixture.close()
