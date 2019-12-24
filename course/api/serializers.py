from course.models import Course, Content, Prerequisite, ContentAccess
from accounts.models import User
from rest_framework import serializers
from django.conf import settings

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'course_id',
            'author',
            'is_approved',
            'approved_by',
            'outline',
            'prerequisites',
            'banner',
            'private',
            'tags',
            'title',
            'rating',
            'date_created',
            'date_updated',
            'fee',
            'length',
            'language',
            'difficulty'
        ]


class CourseSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title',
            'outline',
            'prerequisites',
            'banner',
            'tags',
            'private',
            'fee',
            'length',
            'language',
            'difficulty'
        ]


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title',
            'outline',
            'prerequisites',
            'private',
            'tags',
            'fee',
            'length',
            'language',
            'difficulty'
        ]


class CourseBannerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['banner']


class serializerUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]

    # def validate_title(self, request):
    #     qs = Course.objects.filter(title__iexact=request)
    #     if qs:
    #         response_data = {}
    #         response_data['data'] = {}
    #         response_data['errors'] = {"Title": "Title Must be Unique"}
    #         raise serializers.ValidationError(response_data)
    #     else:
    #         return request
    #
    # def validate(self, data):
    #     banner = data.get('banner', None)
    #     banner_type = banner.content_type.split('/')[0]
    #     # print(banner.size)
    #     if banner_type in settings.CONTENT_TYPES:
    #         response_data = {}
    #         response_data['data'] = {}
    #         response_data['errors'] = {"banner": "Max size limit exceeded or File type not Matched"}
    #         raise serializers.ValidationError(response_data)
    #     else:
    #         return data

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            'title',
            'description',
            'serial',
            'file',
            'file_type',
        ]


class ContentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            'title',
            'description',
            'file',
            'file_type',
        ]


class ContentAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class UlalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentAccess
        fields = [
            'content_id',
            'has_completed'
        ]


class PrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequisite
        fields = '__all__'


class ContentPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            'content_id',
            'preview'
        ]