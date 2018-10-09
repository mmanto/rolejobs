# encoding: utf-8
from django.utils import timezone
from django.views import generic

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsEmployer, IsPostulant
from rolejobs_api.generics import StandarPagination

from models import Course, CoursePostulation
from serializers import (
    CourseSerializer, CoursePostulationEmployerSerializer,
    CourseEmployerSerializer
)
from forms import (
    NewCourseForm
)

class CourseView(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandarPagination
    permission_class = [IsAuthenticated]


class CourseEmployerView(viewsets.ModelViewSet):
    serializer_class = CourseEmployerSerializer
    pagination_class = StandarPagination
    permission_class = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        queryset = Course.objects.filter(owner=self.request.user)
        return queryset

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course = Course(**serializer.data)
            course.owner = request.user
            course.save()
            return Response(status=201)
        return Response(serializer.errors, status=400)


class CoursePostulationEmployerView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CoursePostulationEmployerSerializer
    pagination_class = StandarPagination
    permission_class = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        queryset = CoursePostulation.objects.filter(
            course__owner=self.request.user)
        return queryset

    def retrieve(self, request, pk):
        queryset = self.get_queryset()
        queryset = queryset.filter(id=pk)
        serializer = self.serializer_class(queryset, many=False)
        # mark read the postulation
        try:
            course_postulation = CoursePostulation.objects.get(id=pk)
        except CoursePostulation.DoesNotExist:
            return Response(status=404)

        course_postulation.readed_at = timezone.now()
        course_postulation.save()
        return Response(serializer.data)


class CoursePostulationPostulantView(viewsets.ViewSet):
    permission_class = [IsAuthenticated, IsPostulant]

    def create(self, request, pk):
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response(status=404)

        course_postulation = CoursePostulation(
            course=course, user=request.user)
        course_postulation.save()
        if course.notify_by_email:
            request.user.send_courses_postulation_notification(course)
        return Response(status=201)


class NewCourseFormView(generic.FormView):

    template_name = 'new_course.html'
    form_class = NewCourseForm
