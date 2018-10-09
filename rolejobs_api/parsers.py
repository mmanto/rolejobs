# encoding=utf-8

import re
from base64 import decodestring

from django.core.files.base import ContentFile

from rest_framework.parsers import BaseParser


class UriDataParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    uriExp = re.compile(
        r"^data:(?P<type>[^;]*);(?P<encoding>[^,]*),(?P<data>.*)$")

    def parse(self, stream, media_type=None, parser_context=None):
        content = self.uriExp.match(stream.read())

        if content is None:
            raise Exception("Invalid content")

        encoding = content.group("encoding")
        data = content.group("data")

        if encoding.lower() == "base64":
            return ContentFile(decodestring(data))
        else:
            raise Exception("Unknow type")
