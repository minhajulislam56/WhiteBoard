from django.contrib import admin
from .models import Course, Content, Prerequisite, ContentAccess, Enrollment

class CourseView(admin.ModelAdmin):
    list_display = [
        'course_id',
        'title',
        'author',
        'is_approved',
        'approved_by',
        'outline',
        'prerequisites',
        'fee'
    ]
    class Meta:
        model = Course
admin.site.register(Course, CourseView)

class ContentView(admin.ModelAdmin):
    list_display = [
        'content_id',
        'course_id',
        'file',
        'file_type',
        'serial',
        'title',
        'description'
    ]
    class Meta:
        model = Content
admin.site.register(Content, ContentView)

class ContentAccessView(admin.ModelAdmin):
    list_display = [
        'user_id',
        'content_id',
        'has_unlocked',
        'has_completed'
    ]
    class Meta:
        model = ContentAccess
admin.site.register(ContentAccess, ContentAccessView)

class PrerequisiteView(admin.ModelAdmin):
    list_display = [
        'content_id',
        'preq_id'
    ]
    class Meta:
        model = Prerequisite
admin.site.register(Prerequisite, PrerequisiteView)

class EnrollmentView(admin.ModelAdmin):
    list_display = [
        'user_id',
        'course_id',
        'rating',
        'review',
        'purchased_time',
        'review_time'
    ]
    class Meta:
        model = Enrollment
admin.site.register(Enrollment, EnrollmentView)