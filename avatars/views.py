# encoding=utf-8

from hashlib import sha1

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route

from rolejobs_api.parsers import UriDataParser

from models import UserAvatar


class ProfileAvatarView(generics.GenericAPIView):
    """Profile avatar view"""

    parser_classes = (UriDataParser,)

    def get_object(self, label="default"):
        return UserAvatar.objects.get(
            user=self.request.user,
            label=label)

    def get_or_create(self, label):
        return UserAvatar.objects.get_or_create(
            user=self.request.user,
            label=label)

    def get(self, request, label="default"):

        try:
            avatar = self.get_object(label)
        except UserAvatar.DoesNotExist:
            url = static('img/prof.png')
        else:
            url = avatar.url

        return HttpResponseRedirect(url)

    @detail_route(permission_classes=(IsAuthenticated,))
    def post(self, request, label="default"):

        if not isinstance(request.data, ContentFile):
            return Response(status=400)

        avatar, is_new = self.get_or_create(label)

        try:
            file_data = request.data
            csum = sha1(file_data.read(1024)).hexdigest()[:10]
            avatar.avatar_file.save("%s.png" % csum, file_data)
        except Exception, e:
            if is_new:
                avatar.delete()

            raise e
        else:
            return Response(status=201)

    def delete(self, request, label="default"):

        try:
            avatar = self.get_object(label)
        except UserAvatar.DoesNotExist:
            return Response(status=404)
        else:
            avatar.delete()
            return Response(status=204)
