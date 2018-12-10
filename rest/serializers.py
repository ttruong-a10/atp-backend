from rest_framework import serializers

from .models.pod import Pod
from .models.course import Course
from .models.blueprint import Blueprint
from .models.others import Student, AccessToken


class PodSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'access_token': { 'write_only': True }
        }
        fields = (
            'id',
            'name',
            'slug',
            'number',
            'course',
            'access_token',
            'blueprint',
            'status',
            'public_ip',
            'hostname',
            'next_stop',
            'student',
            'created_at',
        )
        model = Pod


class CourseSerializer(serializers.ModelSerializer):
    # Shows all pod objects
    # pods = PodSerializer(many=True, read_only=True)
    # Hyperlinks
    pods = serializers.HyperlinkedRelatedField(
        many=True, 
        read_only=True,
        view_name='apiv1:pod-detail'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'short_name',
            'slug',
            'owner',
            'created_at',
            'pods',
        )
        model = Course


class BlueprintSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'cloud_region',
            'vm_size',
            'image_id',
            'allow_internet_outbound',
            'owner',
            'created_at',
        )
        model = Blueprint


class StudentSerializer(serializers.ModelSerializer):
    pods = serializers.HyperlinkedRelatedField(
        many=True, 
        read_only=True,
        view_name='apiv1:pod-detail'
    )
    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'pods',
            'created_at',
        )
        model = Student


class AccessTokenSerializer(serializers.ModelSerializer):
    pod = serializers.HyperlinkedRelatedField(
        many=True, 
        read_only=True,
        view_name='apiv1:pod-detail'
    )
    class Meta:
        fields = (
            'id',
            'name',
            'start_date',
            'end_date',
            'pod',
            'created_at',
        )
        model = AccessToken