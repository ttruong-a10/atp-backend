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
from .models.others import Student, AccessToken, VmSize
from . import serializers
from . import azure
from . import azure_wrapper
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
    lookup_field = 'slug'
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            # delete RG in Azure
            resource_client = azure.get_client('resource')
            rg = kwargs.get('slug')
            azure.delete_resource_group(resource_client, rg)
        except:
            print('rg: ' + rg)
            return Response(
                { 'Fail to delete resource Group "{}".'.format(rg) }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return super(CourseViewSet, self).destroy(request, *args, **kwargs)


    @detail_route(methods=['get'], url_path='pods',)
    def pods(self, request, slug, pk=None, pod_number=None):
        course = self.get_object()
        serializer_context = {
            'request': request,
        }
        serializer = serializers.PodSerializer(
            course.pods.all(), many=True, context=serializer_context
        )
        return Response(serializer.data)

    @list_route(methods=['post'], url_path='check-name-exists')
    def checkNameExists(self, request, pk=None):
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

    @detail_route(methods=['post'], url_path='action/start')
    def startCourse(self, request, slug ):
        course = get_object_or_404(Course, slug=slug)

        pods_queryset = course.get_pods_list()
        try:
            for pod in pods_queryset:
                azure_wrapper.startPod(pod)
        except BaseException as e:
            print(e)
            return Response(
                { 'Fail to start course "{}".'.format(course.name) },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(status=status.HTTP_202_ACCEPTED)


    @detail_route(methods=['post'], url_path='action/stop')
    def stopCourse(self, request, slug ):
        course = get_object_or_404(Course, slug=slug)

        pods_queryset = course.get_pods_list()
        try:
            for pod in pods_queryset:
                azure_wrapper.stopPod(pod)
        except:
            return Response(
                { 'Fail to stop course "{}".'.format(course.name) },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(status=status.HTTP_202_ACCEPTED)

    @detail_route(methods=['post'], url_path='action/restart')
    def restartCourse(self, request, slug ):
        course = get_object_or_404(Course, slug=slug)

        pods_queryset = course.get_pods_list()
        try:
            for pod in pods_queryset:
                azure_wrapper.restartPod(pod)
        except:
            return Response(
                { 'Fail to restart course "{}".'.format(course.name) },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(status=status.HTTP_202_ACCEPTED)

      

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


class ListImage(APIView):
    def get(self, request, format=None, *args, **kwargs):
        location = kwargs.get('location')
        compute_client = azure.get_client('compute')
        images = azure.get_images(compute_client)
        if location:
            images = list(filter(lambda x: x.location==location, images))
        serializer = serializers.ImageSerializer(images, many=True)
        return Response(serializer.data)


class ListVmSize(APIView):
    def get(self, request, format=None, *args, **kwargs):
        location = kwargs.get('location')
        queryset = VmSize.objects.all()
        if location:
            queryset = queryset.filter(location=location)

        serializer = serializers.VmSizeSerializer(queryset, many=True)
        return Response(serializer.data)
