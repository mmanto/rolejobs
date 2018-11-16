# encoding=utf-8

from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.views import generic

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from json import loads

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from rolejobs_api.generics import StandarPagination

from utils.serializers import (
    SimpleItemSerializer,
    SlugedItemSerializer,
    ChoicesSerializer,
)

from accounts.permissions import IsEmployer, IsPostulant
from postulant.permissions import IsCompletedProfile
from employer.models import Employer

from permissions import IsOwnJob, IsOfOwnJob

from models import (
    Job,
    JobPostulation,
    Area,
    Technology,
    Hierarchy,
    Position,
    Role,
    TitleRole,
    BranchActivity,
    JOB_TYPE_CHOICES,
    JOB_STATUS_HAB,
    JOB_STATUS_CHOICES,
)

from serializers import (
    JobSerializer,
    JobListSerializer,
    JobsSimpleSerializer,
    OwnJobSerializer,
    AreaSerializer,
    DetailedAreaSerializer,
    TechnologySerializer,
    JobPostulationSerializer,
    OwnJobPostulationListSerializer,
    OwnJobPostulationDetailledSerializer,
    PostulationStatusSerializer,
    OwnJobsInfoSerializer,
    PostulationFavoriteSerializer,
)

from forms import (
    NewJobForm,
    KnowledgeRequirementForm,
    QuestionForm,
    JobQuestionsForm,
)

from filters import AdvancePublicJobsFilters, OwnJobsFilters

from accounts.models import User


class NotMoreVacanciesAvaible(Exception):
    pass


class PublicJobsViewSet(viewsets.ReadOnlyModelViewSet):
    """Public jobs viewset"""

    pagination_class = StandarPagination
    filter_class = AdvancePublicJobsFilters

    def get_queryset(self):
        queryset = Job.objects.filter(
            status=JOB_STATUS_HAB,
            owner__user__status=User.S_ENABLED,
        ).order_by(
            '-featured', '-published'
        )

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        else:
            return JobSerializer

    def resolve_list_response(self, qs=None, serializer_class=None):

        if serializer_class is None:
            serializer_class = self.get_serializer_class()

        if qs is None:
            qs = self.get_queryset()

        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    @list_route(serializer_class=JobsSimpleSerializer)
    def get_lasts(self, request):
        queryset = self.get_queryset().order_by('-created')
        return self.resolve_list_response(queryset, JobsSimpleSerializer)

    @list_route(methods=('get', ))
    def by_area(self, request, area_pk):
        queryset = self.get_queryset().filter(area=area_pk)
        return self.resolve_list_response(queryset)

    @list_route(methods=('get', ))
    def with_roles(self, request):
        queryset = self.get_queryset().filter(
            roles__isnull=False)
        return self.resolve_list_response(queryset)


class OwnJobsViewSet(viewsets.ModelViewSet):
    """Employer jobs"""

    serializer_class = OwnJobSerializer
    permission_classes = (IsAuthenticated,
                          IsEmployer,
                          IsOwnJob)
    filter_class = OwnJobsFilters

    pagination_class = StandarPagination

    def get_employer(self):
        user = self.request.user
        queryset = Employer.objects.all()
        employer = get_object_or_404(queryset, user=user)
        return employer

    def get_queryset(self):
        queryset = Job.objects.filter(
            owner=self.get_employer()
        ).order_by(
                '-created')

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.get_employer())

    @list_route(serializer_class=JobsSimpleSerializer)
    def get_lasts(self, request):
        queryset = self.get_queryset().order_by('-created')

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = JobsSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = JobsSimpleSerializer(queryset, many=True)
        return Response(serializer.data)


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """Area viewset"""

    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class DetailedAreaViewSet(viewsets.ReadOnlyModelViewSet):
    """Area viewset"""

    queryset = Area.objects.all()
    serializer_class = DetailedAreaSerializer

    @detail_route(methods=['get', ])
    def by_slug(self, request, slug):
        qs = self.get_queryset()
        area = get_object_or_404(qs, slug=slug)
        serializer = self.get_serializer_class()(area)
        return Response(serializer.data)


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    """Technology viewset"""

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class HierarchyViewSet(viewsets.ReadOnlyModelViewSet):
    """Hierarchies viewset"""

    queryset = Hierarchy.objects.all()
    serializer_class = SimpleItemSerializer


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """Roles viewset"""

    queryset = Role.objects.all()
    serializer_class = SlugedItemSerializer


class JobPostulationViewSet(viewsets.ModelViewSet):
    """Job postulation viewset"""

    serializer_class = JobPostulationSerializer
    permission_classes = (IsAuthenticated, IsPostulant, IsCompletedProfile)

    def get_job(self):
        job_id = self.kwargs.get("job_pk", None)
        job = get_object_or_404(Job.objects.all(), id=job_id)
        return job

    def get_queryset(self):
        return self.get_job().postulants.all()

    def perform_create(self, serializer):
        job = self.get_job()
        try:
            vacancies = int(job.vacancies)
        except:  #ValueError:  # is an error
            vacancies = None

        if vacancies is None or vacancies > 0:
            serializer.save(
                user=self.request.user,
                job=job)
        else:
            raise NotMoreVacanciesAvaible('Not more vacancies')


class OwnJobPostulationsViewSet(viewsets.ReadOnlyModelViewSet):
    """View postulations to jobs (owns)"""

    serializer_class = OwnJobPostulationListSerializer
    pagination_class = StandarPagination
    permission_classes = (
        IsAuthenticated,
        IsEmployer,
        IsOfOwnJob)

    def get_employer(self):
        user = self.request.user
        queryset = Employer.objects.all()
        employer = get_object_or_404(queryset, user=user)
        return employer

    def get_queryset(self):
        owner = self.get_employer()
        jobs = Job.objects.filter(owner=owner)

        job_id = self.kwargs.get("job_pk", None)
        job = get_object_or_404(jobs, id=job_id)

        queryset = job.postulants.all()

        filter_status = self.request.query_params.get('status', None)

        if filter_status:
            queryset = queryset.filter(status=int(filter_status))

        return queryset

    @detail_route(
        method="GET",
        serializer_class=OwnJobPostulationDetailledSerializer)
    def retrieve(self, *args, **kwargs):
        obj = self.get_object()
        obj.mark_read()
        serializer = OwnJobPostulationDetailledSerializer(obj)
        return Response(serializer.data)

    @detail_route(
        methods=["put"],
        serializer_class=PostulationStatusSerializer)
    def set_status(self, request, *args, **kwargs):
        """Set postulation status"""

        data = PostulationStatusSerializer(data=request.data)

        if data.is_valid():
            obj = self.get_object()
            try:
                obj.set_status(data.data['status'])
            except Exception, e:
                # TODO log e
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=200)
        else:
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(
        methods=["put"],
        serializer_class=PostulationFavoriteSerializer)
    def set_favorite(self, request, *args, **kwargs):
        """Mark postulation favorite"""

        data = PostulationFavoriteSerializer(data=request.data)

        if data.is_valid():
            obj = self.get_object()
            try:
                obj.favorite = data.data['favorite']
                obj.save()
            except Exception, e:
                # TODO log e
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=200)
        else:
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnJobsInfoView(APIView):

    serializer_class = OwnJobsInfoSerializer
    permission_classes = (
        IsAuthenticated,
        IsEmployer)

    def get(self, request, *args, **kwargs):

        total_postulants = JobPostulation.objects.filter(
            job__owner__user=request.user).count()

        data = {
            "total_postulants": total_postulants,
            "aviable_status": ChoicesSerializer.parse_data(JOB_STATUS_CHOICES)
        }

        result = OwnJobsInfoSerializer(data)

        return Response(result.data)


class AdvanceSearchFiltersChoices(APIView):

    def get(self, request, *args, **kwargs):

        title_roles = SimpleItemSerializer(
            TitleRole.objects.all(),
            many=True)

        roles = SimpleItemSerializer(
            Role.objects.all(),
            many=True)

        positions = SimpleItemSerializer(
            Position.objects.all(),
            many=True)

        hierarchies = SimpleItemSerializer(
            Hierarchy.objects.all(),
            many=True)

        branch_activities = SimpleItemSerializer(
            BranchActivity.objects.all(),
            many=True)

        job_types = ChoicesSerializer(
            ChoicesSerializer.parse_data(JOB_TYPE_CHOICES),
            many=True)

        return Response({
            "title_role": title_roles.data,
            "roles": roles.data,
            "position": positions.data,
            "hierarchy": hierarchies.data,
            "branch_activity": branch_activities.data,
            "job_type": job_types.data,
        })


class RelatedJobsViewSet(viewsets.ReadOnlyModelViewSet):
    """Public jobs viewset"""

    serializer_class = JobsSimpleSerializer
    pagination_class = StandarPagination

    def list(self, request, job_pk=None):
        job = get_object_or_404(Job, id=job_pk)

        queryset = Job.objects.filter(
            role=job.role,
            area=job.area,
            subarea=job.subarea
        ).order_by(
                '-featured', '-published'
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = JobsSimpleSerializer(queryset, many=True)
        return Response(serializer.data)

    def mretrieve(self, request, pk=None):
        queryset = Job.objects.all()
        job = get_object_or_404(queryset, id=pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

# template


class JobQuestionsFormView(generic.View):
    """View for job questions dinamic form"""

    def get(self, request, job_pk):
        job = get_object_or_404(Job.objects.all(), id=job_pk)
        question_form = JobQuestionsForm(job)

        return render(request, "job_postulate.html", {
            "job": job,
            "questions_form": question_form
        })


# Admin


class JobModerateView(generic.View):
    """View for moderation"""

    def get(self, request, pk):
        return render(request, "moderate_job.html", {
            "pk": pk
        })


# Forms


class NewJobFormView(generic.FormView):

    template_name = 'new_job.html'
    form_class = NewJobForm


class KnowledgeRequirementFormView(generic.FormView):

    template_name = 'new_knowledge_requirement.html'
    form_class = KnowledgeRequirementForm


class QuestionFormView(generic.FormView):
    template_name = "new_question.html"
    form_class = QuestionForm


class UserPostulationsJobs(generic.View):
    
    @method_decorator(csrf_protect)
    def post(self, request):
        pks = loads(request.body)['pks']
        postulationjobs = []
        if request.user.is_authenticated:
            for mpk in pks:
                try:
                    mjob = Job.objects.get(pk = mpk)
                    JobPostulation.objects.get(user = request.user, job = mjob)
                    postulationjobs.append(mpk)
                except Exception:
                    continue
        return JsonResponse({'postulationjobs': postulationjobs})

class EnterpriceJobs(generic.View):
    
    @method_decorator(csrf_protect)
    def post(self, request):
        mpk = loads(request.body)['pk']
        mjob = Job.objects.get(pk = mpk)
        similarJobs = Job.objects.filter(owner = mjob.owner).exclude(pk = mpk)
        postulationjobs = []
        if request.user.is_authenticated:
            for sJob in similarJobs:
                try:
                    JobPostulation.objects.get(user = request.user, job = sJob)
                except Exception:
                    postulationjobs.append(sJob)
        serializer = JobSerializer(postulationjobs, many=True)
        return JsonResponse(serializer.data, safe=False)
        

