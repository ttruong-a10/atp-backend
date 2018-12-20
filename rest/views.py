# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions 
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
from rest_framework.response import Response


from .models.pod import Pod
from .models.course import Course
from .models.blueprint import Blueprint
from .models.others import Student, AccessToken
from . import serializers
from . import azure
from . import validators


''' Class Base Views
class ListCreatePod(APIView):
    def get(self, request, format=None):
        pods = Pod.objects.all()
        serializer = serializers.PodSerializer(pods, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.PodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(Serializer.data, status=status.HTTP_201_CREATED)
'''

'''  Generic Views
class ListCreateCourse(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer


class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer


class ListCreatePod(generics.ListCreateAPIView):
    queryset = Pod.objects.all()
    serializer_class = serializers.PodSerializer

    def get_queryset(self):
        return self.queryset.filter(course_id=self.kwargs.get('course_pk'))

    def perform_create(self, serializer):
        course = get_object_or_404(
            Course, 
            pk=self.kwargs.get('course_pk')
        )
        serializer.save(course=course)


class RetrieveUpdateDestroyPod(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pod.objects.all()
    serializer_class = serializers.PodSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            course_id=self.kwargs.get('course_pk'),
            pk=self.kwargs.get('pk')
        )

'''

# View Sets
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer

    @detail_route(methods=['get'])
    def pods(self, request, pk=None):
        course = self.get_object()
        serializer = serializers.PodSerializer(
            course.pods.all(), many=True
        )
        return Response(serializer.data)

    @list_route(methods=['post'])
    def checkExists(self, request, pk=None):
        serializer = serializers.CourseNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rg = serializer.data['name']
        # resource_client = azure.get_client('resource')
        # result = azure.check_resource_group_exist(resource_client, rg)
        try:
            validators.validate_course_name(rg)
        except ValidationError:
            # Name already exists!
            return Response(True)
        else:
            # Name has not exist 
            return Response(False)

    # only show the course owned by current user IF not SuperUser
    def get_queryset(self):
        owner = self.request.user
        queryset = self.queryset.all()
        if owner.is_superuser: 
            return queryset
        else:
            return queryset.filter(owner=owner)
    
    # set current user as owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PodViewSet(viewsets.ModelViewSet):
    queryset = Pod.objects.all()
    serializer_class = serializers.PodSerializer

    # only show the course owned by current user IF not SuperUser
    def get_queryset(self):
        owner = self.request.user
        queryset = self.queryset.all()
        if owner.is_superuser: 
            return queryset
        else:
            return queryset.filter(owner=owner)


class BlueprintViewSet(viewsets.ModelViewSet):
    queryset = Blueprint.objects.all()
    serializer_class = serializers.BlueprintSerializer

    # set current user as owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class AccessTokenViewSet(viewsets.ModelViewSet):
    queryset = AccessToken.objects.all()
    serializer_class = serializers.AccessTokenSerializer