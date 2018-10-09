# encoding=utf-8

from django.utils.translation import gettext as _

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from utils.views import ChoicesApiView

from serializers import InstitutionSerializer, LanguageSerializer
from models import Institution, Language
from choices import EDUCATION_GRADES


class SearchInstitutionView(viewsets.ReadOnlyModelViewSet):
    """View for institution search"""

    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Institution.objects.all()

    def list(self, request):
        # @TODO add country and level filters!

        keyword = request.GET.get('s', None)

        if keyword is None:
            return Response({
                "error": _(u"Debe incluir el parametro s")
                }, status=status.HTTP_400_BAD_REQUEST)

        if len(keyword) < 3:
            return Response({
                "error": _(u"La keyword a buscar debe tener por lo menos" +
                           u"tres caracteres")
                }, status=status.HTTP_400_BAD_REQUEST)

        result = self.queryset.filter(
            name__icontains=keyword)

        serializer = self.get_serializer(result[0:10], many=True)

        return Response(serializer.data)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """Languages view"""

    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


class EducationGradesView(ChoicesApiView):
    """Education grades view"""

    data = EDUCATION_GRADES
