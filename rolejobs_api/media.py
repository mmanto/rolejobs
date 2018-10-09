# encoding=utf-8

from os import path

from django.conf import settings


def resolve_media_path(upath):
    return path.join(settings.MEDIA_ROOT, upath)


def resolve_media_url(upath):
    rpath = path.relpath(upath, settings.MEDIA_ROOT)
    return u"%s%s" % (settings.MEDIA_URL, rpath)
