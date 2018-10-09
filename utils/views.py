# encoding=utf-8

from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from serializers import ChoicesSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class DeleteBulkMixing(object):

    ids_field = "ids"
    table_pk = "id"

    @list_route(methods=['DELETE'])
    def delete_bulk(self, request):
        ids = request.GET.get(self.ids_field, None)

        if ids is None:
            return Response("No elements passed",
                            status=status.HTTP_400_BAD_REQUEST)

        filters = {
            "%s__in" % self.table_pk: [int(id) for id in ids.split(',')]
        }

        objs = self.get_queryset().filter(**filters)

        for obj in objs:
            self.check_object_permissions(self.request, obj)

        objs.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChoicesApiView(APIView):
    """List choices as API"""

    data = None
    serializer_class = ChoicesSerializer
    response_serializer = ChoicesSerializer

    def get(self, request, format=None):
        if not self.data:
            raise Exception("Data not defined")

        result = [{"name": c[1], "value": c[0]} for c in self.data]

        return Response(result)
