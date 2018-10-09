# encoding=utf-8
from __future__ import unicode_literals

from rolejobs_api.media import resolve_media_path


def get_company_logo_path(obj, filename):
    first_letter = obj.user.email[0]
    path = 'company/logos/{}/{}/{}'.format(
        first_letter, obj.user.id, filename)
    return resolve_media_path(path)
