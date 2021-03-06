# encoding=utf-8
from hashlib import sha1
import magic

from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
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
from education.models import UserEducation, UserLanguages, UserComputerknowledge, UserAdditionalknowledge, UserWorkpreference
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
    MARRIED_STATUS
)

from postulant.choices import CV_COMPLETION, TYPE_LICENCE

from postulant.forms import (
    PostulantCvForm,
    VideoCvForm,
    DocCvForm,
    NewProfieccionalExperienceForm,
    NewEducationForm,
    ExperienceReferenceForm,
    NewLanguageForm,
    NewComputerknowledgeForm,
    NewAdditionalknowledgeForm,
    NewWorkpreferenceForm,
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
    PostulantAdditionalknowledgesSerializer,
    PostulantAdditionalknowledgesDetailSerializer,
    PostulantWorkpreferencesSerializer,
    PostulantWorkpreferencesDetailSerializer,
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

from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

class Signup(generics.GenericAPIView):
    """Signup new postulant"""

    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #En caso que el usuario haya intentado registrarse y no confirmo, el correo 
        # va a aparecer mas de una vez.
        lst_email_count = Spool.objects.filter(to=request.data['email'], sent=False)
        if (len(lst_email_count) > 1):
            email = Spool.objects.filter(to=request.data['email'], sent=False)[-1]
        else:
            email = Spool.objects.filter(to=request.data['email'], sent=False)[0]
            
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.data['email'], ]
        send_mail(email.subject, email.content, email_from, recipient_list, html_message=email.content)
        email.sent = True
        email.save()
        return Response({"success": _("Postulant signup success")})


class VideoCvView(generic.View):
    
    def post(self, request):
        postulant = Postulant.objects.get(user= request.user)
        postulant.video_cv = request.FILES['video_cv']
        postulant.save()
        return HttpResponseRedirect('/postulant/cv')

class DocCvView(generic.View):
    
    def post(self, request):
        postulant = Postulant.objects.get(user= request.user)
        postulant.doc_cv = request.FILES['doc_cv']
        postulant.save()
        return HttpResponseRedirect('/postulant/cv')

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

class PostulantDownloadPdf(generic.View):

    def get(self, request):
        postulant = Postulant.objects.get(user=request.user)
        try:
            biograph = Biographic.objects.get(user=request.user).description
        except:
            biograph = ''
        template_path = 'downloadpdf.html'
        context = { 
            'first_name': postulant.user.first_name,
            'last_name': postulant.user.last_name,
            'marital_status': str( MARRIED_STATUS[postulant.marital_status - 1][1] ),
            'dni': postulant.dni,
            'date_of_birth': postulant.date_of_birth,
            'country_of_birth': postulant.country_of_birth.name,
            'postal_code': postulant.postal_code,
            'driver_license': str( TYPE_LICENCE[postulant.driver_license][1] ) if  postulant.driver_license <= 3 else str( TYPE_LICENCE[0][1] ),
            'own_vehicle': _(u'Sí') if postulant.own_vehicle else _(u'No'),
            'has_disability': _(u'Sí') if postulant.has_disability else _(u'No'),
            'biograph': biograph,
            'experience': postulant.user.experience.all()
        }
        # Create a Django response object, and specify content_type as pdf
        # response = HttpResponse(content_type='application/pdf' )
        # response['Content-Disposition'] = 'attachment; filename="cv.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(Context(context))
        # create a pdf
        # pisaStatus = pisa.CreatePDF(html, dest=response)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

        # if error then show some funy view
        # return response
        return HttpResponse(response.getvalue(), content_type='application/pdf')


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

class PostulantAdditionalknowledgesViewSet(viewsets.ModelViewSet, DeleteBulkMixing):

    table_pk = "additionalknowledge"
    lookup_field = "additionalknowledge"
    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_serializer_class(self):
        if self.request.method == "GET" or self.request.method == "POST":
            return PostulantAdditionalknowledgesSerializer
        else:
            return PostulantAdditionalknowledgesDetailSerializer

    def get_queryset(self):
        return UserAdditionalknowledge.objects.filter(
            user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.lookup_field, None)

        if pk is None:
            return super(PostulantAdditionalknowledgesViewSet, self).get_object()

        obj = get_object_or_404(queryset, additionalknowledge=pk)

        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostulantWorkpreferencesViewSet(viewsets.ModelViewSet, DeleteBulkMixing):

    table_pk = "workpreference"
    lookup_field = "workpreference"
    permission_classes = (IsAuthenticated,
                          IsPostulant)

    def get_serializer_class(self):
        if self.request.method == "GET" or self.request.method == "POST":
            return PostulantWorkpreferencesSerializer
        else:
            return PostulantWorkpreferencesDetailSerializer

    def get_queryset(self):
        res = UserWorkpreference.objects.filter(
            user=self.request.user)
        print(res)
        return res

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.lookup_field, None)

        if pk is None:
            return super(PostulantWorkpreferencesViewSet, self).get_object()
        obj = get_object_or_404(queryset, workpreference=pk)
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

class VideoCvFormView(generic.FormView):
    template_name = 'video_cv_form.html'
    form_class = VideoCvForm

class DocCvFormView(generic.FormView):
    template_name = 'doc_cv_form.html'
    form_class = DocCvForm

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

class NewAdditionalknowledgeFormView(generic.FormView):
    template_name = 'postulant_new_additionalknowledge.html'
    form_class = NewAdditionalknowledgeForm

class NewWorkpreferenceFormView(generic.FormView):
    template_name = 'postulant_new_workpreference.html'
    form_class = NewWorkpreferenceForm


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
