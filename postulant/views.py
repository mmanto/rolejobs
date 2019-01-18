# encoding=utf-8
from hashlib import sha1
import magic

from django.views import generic
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route

from utils.views import DeleteBulkMixing
from utils.serializers import SlugedItemSerializer, PkListSerializer
from accounts.permissions import IsPostulant
from education.models import UserEducation, UserLanguages, UserComputerknowledge
from jobs.models import Role, JobPostulation
from jobs.views import OwnJobPostulationsViewSet
from jobs.serializers import PostulantPostulationDetailSerializer
from rolejobs_api.parsers import UriDataParser

from django.core.mail import send_mail
from django.conf import settings
from emailspool.models import Spool

from postulant.models import (
    Postulant,
    Biographic,
    ProfessionalExperience,
    PostulantRoles,
    PostulantAttachCV,
)

from postulant.choices import CV_COMPLETION

from postulant.forms import (
    PostulantCvForm,
    NewProfieccionalExperienceForm,
    NewEducationForm,
    ExperienceReferenceForm,
    NewLanguageForm,
    NewComputerknowledgeForm,
    NewCertificationForm
)

from postulant.serializers import (
    SignupSerializer,
    PostulantSerializer,
    BiographicSerializer,
    ProfessionalExperienceSerializer,
    PostulantEducationSerializer,
    PostulantLanguagesSerializer,
    PostulantLanguagesDetailSerializer,
    PostulantComputerknowledgesSerializer,
    PostulantComputerknowledgesDetailSerializer,
    PostulationsListSerializer,
    # CompletedItemsSerializer,
    CompletedProfileSerializer,
    CompleteProfileSerializer,
    CVRequestPostulantSerializer,
    PostulantAttachCVListSerializer,
    FavoriteSerializer
)

from postulant.permissions import IsCompletedProfile

from jobs.models import FavoriteJob
from rolejobs_api.generics import StandarPagination

class Signup(generics.GenericAPIView):
    """Signup new postulant"""

    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email = Spool.objects.filter(to=request.data['email'], sent=False)[-1]
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.data['email'], ]
        send_mail(email.subject, email.content, email_from, recipient_list, html_message=email.content)
        email.sent = True
        email.save()
        return Response({"success": _("Postulant signup success")})


class PostulantViewSet(viewsets.ModelViewSet):
    serializer_class = CompleteProfileSerializer
    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_postulant(self):
        user = self.request.user
        postulant = get_object_or_404(Postulant.objects.all(), user=user)
        return postulant

    def get_object(self):
        return self.get_postulant()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostulantBiographicViewSet(viewsets.ModelViewSet):
    serializer_class = BiographicSerializer
    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_object(self):
        biographic = get_object_or_404(Biographic.objects.all(),
                                       user=self.request.user)
        return biographic

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfessionalExperienceViewSet(viewsets.ModelViewSet, DeleteBulkMixing):
    serializer_class = ProfessionalExperienceSerializer
    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_queryset(self):
        return ProfessionalExperience.objects.filter(
            user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostulantEducationViewSet(viewsets.ModelViewSet, DeleteBulkMixing):
    serializer_class = PostulantEducationSerializer
    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_queryset(self):
        return UserEducation.objects.filter(
            user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostulantLanguagesViewSet(viewsets.ModelViewSet, DeleteBulkMixing):

    table_pk = "language"
    lookup_field = "language"
    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_serializer_class(self):
        if self.request.method == "GET" or self.request.method == "POST":
            return PostulantLanguagesSerializer
        else:
            return PostulantLanguagesDetailSerializer

    def get_queryset(self):
        return UserLanguages.objects.filter(
            user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.lookup_field, None)

        if pk is None:
            return super(PostulantLanguagesViewSet, self).get_object()

        obj = get_object_or_404(queryset, language=pk)

        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostulantComputerknowledgesViewSet(viewsets.ModelViewSet, DeleteBulkMixing):

    table_pk = "computerknowledge"
    lookup_field = "computerknowledge"
    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_serializer_class(self):
        if self.request.method == "GET" or self.request.method == "POST":
            return PostulantComputerknowledgesSerializer
        else:
            return PostulantComputerknowledgesDetailSerializer

    def get_queryset(self):
        return UserComputerknowledge.objects.filter(
            user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.lookup_field, None)

        if pk is None:
            return super(PostulantComputerknowledgesViewSet, self).get_object()

        obj = get_object_or_404(queryset, computerknowledge=pk)

        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostulantRolesViewSet(viewsets.ModelViewSet):
    """Postulant roles"""

    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_queryset(self):
        postulant_roles = PostulantRoles.by_user(self.request.user)
        return postulant_roles.roles.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SlugedItemSerializer
        else:
            return PkListSerializer

    @detail_route(
        methods=['post', ],
        serializer_class=PkListSerializer)
    def set_roles(self, request):
        pks = request.data
        postulant_roles = PostulantRoles.by_user(self.request.user)
        postulant_roles.set_roles(pks)
        return Response(status=202)

    class Meta:
        model = Role
        exclude = ('description', )


class JobPostulationsViewSet(OwnJobPostulationsViewSet):

    serializer_class = PostulationsListSerializer

    # @TODO Add permission!!!!
    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_queryset(self):
        user = self.request.user

        queryset = JobPostulation.objects.filter(
            user=user)

        filter_status = self.request.query_params.get('status', None)

        if filter_status:
            queryset = queryset.filter(status=int(filter_status))

        return queryset

    @detail_route(serializer_class=PostulantPostulationDetailSerializer)
    def retrieve(self, *args, **kwargs):
        obj = self.get_object()
        serializer = PostulantPostulationDetailSerializer(obj)
        return Response(serializer.data)


class CompletedProfileViewSet(viewsets.ViewSet):
    """Completed profile"""

    permission_classes = (IsAuthenticated,
                          IsPostulant)

    serializer_class = CompletedProfileSerializer

    @detail_route()
    def retrieve(self, request, *args, **kwargs):
        user = request.user

        completed = user.calculate_complete(CV_COMPLETION)

        items = [{
            "value": k,
            "name": v,
            "is_completed": user.has_completed(k)
        } for k, v in CV_COMPLETION]

        serializer = CompletedProfileSerializer({
            "percent": completed,
            "items": items})

        return Response(serializer.data)


class CVRequestPostulantViewSet(viewsets.ModelViewSet):
    """ViewSet for create cv request"""

    serializer_class = CVRequestPostulantSerializer
    permission_classes = (IsAuthenticated, IsPostulant, IsCompletedProfile)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": _("CV request send to employer")})

        return Response(serializer.errors)


class PostulantAttachCVView(viewsets.ModelViewSet):
    """Postulant attatch cv's for postulant"""

    serializer_class = PostulantAttachCVListSerializer
    parser_classes = (UriDataParser,)
    permission_classes = (IsAuthenticated, IsPostulant)

    def retrieve(self, request, filename):
        try:
            attach = PostulantAttachCV.objects.get(
                user=self.request.user, name=filename)
        except PostulantAttachCV.DoesNotExist:
            return Response(status=400)

        return HttpResponseRedirect(attach.url)

    def list(self, request):
        queryset = PostulantAttachCV.objects.filter(user=request.user)
        serializer = PostulantAttachCVListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, filename):
        if not isinstance(request.data, ContentFile):
            return Response(status=400)

        _file = request.data
        _file_mime = magic.from_buffer(_file.read(1024), mime=True)
        try:
            _file_extension = _file_mime.split('/')[-1]
        except IndexError:
            return Response({'error': 'cant get filetype'}, status=400)

        csum = sha1(_file.read(1024)).hexdigest()[:10]

        attach = PostulantAttachCV(user=request.user, name=filename)
        attach.attach.save('{}.{}'.format(csum, _file_extension), _file)
        attach.save()

        return Response(status=201)

    def destroy(self, request, filename):
        try:
            attach = PostulantAttachCV.objects.get(
                user=request.user, name=filename)
        except PostulantAttachCV.DoesNotExist:
            return Response(status=404)
        else:
            attach.delete()
            return Response(status=200)


##########
# FORMS
#########


class PostulantCvFormView(generic.FormView):
    template_name = 'postulant_form.html'
    form_class = PostulantCvForm


class NewProfieccionalExperienceFormView(generic.FormView):
    template_name = 'postulant_new_pe.html'
    form_class = NewProfieccionalExperienceForm


class NewEducationFormView(generic.FormView):
    template_name = 'postulant_new_education.html'
    form_class = NewEducationForm


class NewReferenceFormView(generic.FormView):
    template_name = 'postulant_pe_new_reference.html'
    form_class = ExperienceReferenceForm


class NewLanguageFormView(generic.FormView):
    template_name = 'postulant_new_language.html'
    form_class = NewLanguageForm


class NewComputerknowledgeFormView(generic.FormView):
    template_name = 'postulant_new_computerknowledge.html'
    form_class = NewComputerknowledgeForm


class NewCertificationFormView(generic.FormView):
    template_name = 'postulant_education_new_cert.html'
    form_class = NewCertificationForm


class FavoritesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FavoriteJob.objects.all()
    pagination_class = StandarPagination
    serializer_class = FavoriteSerializer


    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset().filter(user = request.user)
        serializer = FavoriteSerializer(queryset, many=True)
        return Response({ 'results': serializer.data })
