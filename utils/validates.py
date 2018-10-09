# encoding=utf-8
import os


def validate_extension(**extensions):
    pass


def validate_logo(value):
    pass


def validate_photo_profile(value):
    pass


def validate_size(fieldfile_obj):
    pass


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx']
    if ext not in valid_extensions:
        raise ValidationError('Formato no soportado!')


def validate_size(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(
            "El tamaño máximo de archivo es %sMB" % str(megabyte_limit))
