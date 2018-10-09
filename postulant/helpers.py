# encoding=utf-8

from rolejobs_api.media import resolve_media_path


def get_attachcv_directory(obj, filename):
    first_letter = obj.user.email[0]
    path = 'attach_cv/{}/{}/{}'.format(first_letter, obj.user.id, filename)
    return resolve_media_path(path)
