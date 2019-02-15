# encoding=utf-8

import logging

from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route

from accounts.models import User
from accounts.permissions import IsEmployer
from jobs.views import OwnJobPostulationsViewSet
from jobs.models import JobPostulation, JobPostulationNote
from rolejobs_api.generics import StandarPagination

from django.core.mail import send_mail
from django.conf import settings
from emailspool.models import Spool


from serializers import (
    SignupSerializer,
    EmployerSerializer,
    PostulationsListSerializer,
    CVRequestListSerializer,
    CVRequestStatusSerializer,
    EmployerPublicInformation,
    JobPostulationNoteSerializer,
    CVTagsSerializer,
)

from models import Employer, CVRequest, CVTags
from forms import NgSignupForm, EmployerDataForm

from postulant.models import Postulant


logger = logging.getLogger(__name__)


class Signup(generics.GenericAPIView):
    """Signup new employer"""

    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email = Spool.objects.filter(to=request.data['email'], sent=False).last()
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.data['email'], ]
        send_mail(email.subject, email.content, email_from, recipient_list, html_message=email.content)
        email.sent = True
        email.save()
        return Response({"success": _("Employer signup success")})


class EmployerViewSet(viewsets.ModelViewSet):
    serializer_class = EmployerSerializer
    permission_classes = (IsAuthenticated,
                          IsEmployer)

    def get_employer(self):
        user = self.request.user
        queryset = Employer.objects.all()
        employer = get_object_or_404(queryset, user=user)
        return employer

    def get_object(self):
        return self.get_employer()


class PostulationsViewSet(OwnJobPostulationsViewSet):

    serializer_class = PostulationsListSerializer
    permission_classes = (IsAuthenticated,
                          IsEmployer)

    def get_queryset(self):
        owner = self.get_employer()

        queryset = JobPostulation.objects.filter(
            job__owner=owner)

        filter_status = self.request.query_params.get('status', None)

        if filter_status:
            queryset = queryset.filter(status=int(filter_status))

        return queryset


class CVRequestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CVRequestListSerializer
    pagination_class = StandarPagination
    permission_classes = (IsAuthenticated, IsEmployer)

    def get_queryset(self):
        queryset = CVRequest.objects.filter(employer=self.request.user.profile)
        return queryset

    @detail_route(methods=['put'], serializer_class=CVRequestStatusSerializer)
    def set_status(self, request, pk):
        """Set cvrequest status"""

        data = CVRequestStatusSerializer(data=request.data)

        if data.is_valid():
            obj = self.get_object()
            try:
                obj.set_status(data.data['status'])
            except Exception, e:
                logger.exception(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=200)
        else:
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerTopTenViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = EmployerPublicInformation
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # TODO change this queryset when the client define the concept
        queryset = Employer.objects.all()[:10]
        return queryset


class JobPostulationNoteViewSet(viewsets.ModelViewSet):

    queryset = JobPostulationNote.objects.all()
    serializer_class = JobPostulationNoteSerializer
    permission_classes = (IsAuthenticated, IsEmployer)

    def list(self, request, postulation_pk):
        queryset = JobPostulationNote.objects.filter(
            postulation=postulation_pk)
        serializer = JobPostulationNoteSerializer(queryset, many=True)
        return Response(serializer.data)


class CVTagsViewSet(viewsets.ModelViewSet):
    serializer_class = CVTagsSerializer
    pagination_class = StandarPagination
    permission_classes = (IsAuthenticated, IsEmployer)

    def get_queryset(self):
        queryset = CVTags.objects.filter(employer=self.request.user.profile)
        return queryset

    def create(self, request):
        user = User.objects.get(
            id=request.data.get('user'))
        employer = request.user.profile
        cvtags = CVTags.objects.create(employer=employer, user=user)
        tags = request.data.get('tags')
        if tags:
            [cvtags.tags.add(tag) for tag in tags.split(u' ')]
        try:
            cvtags.save()
        except Exception, e:
            logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=200)

    def update(self, request, pk):
        cvtags = get_object_or_404(self.get_queryset(), pk=pk)
        tags = request.data.get('tags')

        if tags:
            [cvtags.tags.add(tag) for tag in tags.split(u' ')]
        try:
            cvtags.save()
        except Exception, e:
            logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=200)

    def list_tags_by_employer(self, request):
        queryset = self.get_queryset()
        tags = set([
            (tag.id, tag.name)
            for obj in queryset for tag in obj.tags.all()])
        return Response({"tags": list(tags)})

    def delete_tags(self, request, pk):
        cvtags = get_object_or_404(self.get_queryset(), pk=pk)
        tags = request.data.get('tags')

        if tags:
            [cvtags.tags.remove(tag) for tag in tags.split(u' ')]
        try:
            cvtags.save()
        except Exception, e:
            logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=200)



class Companies(generic.View):
    
    def get(self, request):
        serializer = EmployerSerializer(Employer.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)

class Globalstats(generic.View):
    
    def get(self, request):
        # serializer = EmployerSerializer(Employer.objects.all(), many=True)
        # return JsonResponse(serializer.data, safe=False)
        return JsonResponse( {

            'curriculums': len(Postulant.objects.all()),
                'administration': '-',
                'sales': '-',
                'engineering': '-',
                'managers': '-'
                })


##########
# FORMS
#########


class SignupFormView(generic.FormView):
    template_name = 'employer_signup.html'
    form_class = NgSignupForm


class EmployerFormView(generic.FormView):
    template_name = 'employer_form.html'
    form_class = EmployerDataForm


class HomeView(generic.TemplateView):
    """Employer home view"""

    template_name = 'employer_home.html'
