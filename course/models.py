from django.db import models
from django.conf import settings
import uuid

def gen_pic_path(instance, filename):
    return "CoursePic/{course_id}/{filename}".format(course_id=instance.course_id, filename=filename)
def contents_file_path(instance, filename):
    return "Content/{course_id}/{filename}".format(course_id=instance.course_id, filename=filename)

class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_author')
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='course_approved_by')
    outline = models.TextField()
    prerequisites = models.TextField()
    banner = models.ImageField(upload_to=gen_pic_path, null=True, blank=True)
    private = models.BooleanField(default=True)
    tags = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    rating = models.FloatField(default=0.00)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    fee = models.FloatField()
    language = models.CharField(max_length=100, default="English")
    length = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=100, default="Beginner")

    def __str__(self):
        return str(self.course_id)



class Content(models.Model):
    content_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to=contents_file_path, blank=False, null=False)
    file_type = models.BooleanField(blank=False, null=False)    # content/attachment
    serial = models.IntegerField()
    preview = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['serial']

    def __str__(self):
        return str(self.content_id)


class ContentAccess(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE)
    has_completed = models.BooleanField(default=False)
    has_unlocked = models.BooleanField(default=False)

class Prerequisite(models.Model):
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='course_content_id')
    preq_id = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='prerequisite_id')

    def __str__(self):
        return str(self.preq_id)



class Enrollment(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    review = models.TextField(default=None)
    purchased_time = models.DateTimeField(auto_now_add=True)
    review_time = models.DateTimeField(auto_now=True)






