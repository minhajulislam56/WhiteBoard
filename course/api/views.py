from uuid import UUID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics, mixins, status, pagination
from django.contrib.auth import authenticate, get_user_model
from .serializers import (
    CourseSerializer, CourseSerializer2, serializerUser, ContentSerializer, PrerequisiteSerializer,
    ContentAccessSerializer, UlalaSerializer, CourseUpdateSerializer, CourseBannerUpdateSerializer,
    ContentPreviewSerializer, ContentAddSerializer,
)
from course.models import Course, Content, Prerequisite, ContentAccess as Ulala
from accounts.models import User
from ProjectBeta.restconfig.minhaj import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from ProjectBeta.settings import COMMON_URL
from django.db.models import Q
from ProjectBeta.restconfig.pagination import PaginationHandlerMixin
from accounts.api.serializers import ProfileSerializer

class CourseView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        qs = Course.objects.all()
        serializer = CourseSerializer(qs, many=True)
        response = CourseResponseFormat(request, serializer)
        # course_list = []
        # for i in serializer.data:
        #     gen_tags = i.get("tags").split("#")
        #     try:
        #         gen_tags.remove("")
        #     except ValueError:
        #         pass
        #     bannerDir = None
        #     if i['banner'] is not None:
        #         bannerDir = COMMON_URL + str(i.get("banner"))
        #
        #     context = {
        #         "course_id": i["course_id"],
        #         "author": i["author"],
        #         "is_approved": i["is_approved"],
        #         "approved_by": i['approved_by'],
        #         "outline": i["outline"],
        #         "prerequisites": i["prerequisites"],
        #         "banner": bannerDir,
        #         "private": i["private"],
        #         "tags": gen_tags,
        #         "title": i["title"],
        #         "rating": i["rating"],
        #         "date_created": i["date_created"],
        #         "date_updated": i["date_updated"],
        #         "fee": i["fee"],
        #         "length": i["length"],
        #         "language": i["language"],
        #         "difficulty": i["difficulty"]
        #     }
        #     course_list.append(context)

        return Response(response.data, status=status.HTTP_200_OK)


class CourseViewUser(APIView):

    def get(self, request, *args, **kwargs):
        user = self.kwargs.get('user_id')
        if not validate_uuid4(user):
            if not User.objects.filter(username=user).exists():
                return Response({"Error": "User not found"}, status=404)
            author = User.objects.get(username=user)
        else:
            if not User.objects.filter(id=user).exists():
                return Response({"Error": "User not found"}, status=404)
            author = User.objects.get(id=user)
        qs = Course.objects.filter(author=author).order_by('-date_created')
        slzr = CourseSerializer(qs, many=True)
        response = CourseResponseFormat(request, slzr)
        # course_list = []
        #
        # for i in slzr.data:
        #
        #     gen_tags = i.get("tags").split("#")
        #     try:
        #         gen_tags.remove("")
        #     except ValueError:
        #         pass
        #     bannerDir = None
        #     if i['banner'] is not None:
        #         bannerDir = COMMON_URL + str(i.get("banner"))
        #
        #     context = {
        #         "course_id": i["course_id"],
        #         "author": i["author"],
        #         "is_approved": i["is_approved"],
        #         "approved_by": i['approved_by'],
        #         "outline": i["outline"],
        #         "prerequisites": i["prerequisites"],
        #         "banner": bannerDir,
        #         "private": i["private"],
        #         "tags": gen_tags,
        #         "title": i["title"],
        #         "rating": i["rating"],
        #         "date_created": i["date_created"],
        #         "date_updated": i["date_updated"],
        #         "fee": i["fee"],
        #         "length": i["length"],
        #         "language": i["language"],
        #         "difficulty": i["difficulty"]
        #     }
        #     course_list.append(context)

        return Response(response.data, status=200)


class CourseViewSingle(APIView):
    serializer_class = CourseSerializer

    def get(self, *args, **kwargs):
        course_id = self.kwargs.get('course_id', None)
        if course_id is not None:
            if not validate_uuid4(course_id):
                return Response({"Error": "Course Not Found"}, status=status.HTTP_404_NOT_FOUND)
            if not Course.objects.filter(course_id=course_id).exists():
                return Response({"Error": "Course Not Found"}, status=status.HTTP_404_NOT_FOUND)
            qu = Course.objects.filter(course_id=course_id)
            serializer = CourseSerializer(qu, many=True)

            gen_tags = serializer.data[0]["tags"].split("#")
            try:
                gen_tags.remove("")
            except ValueError:
                pass

            if serializer.data[0]['banner'] is not None:
                serializer.data[0]['banner'] = COMMON_URL + serializer.data[0]['banner']
            serializer.data[0]['tags'] = gen_tags
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return Response({"Error": "Course Not Found"}, status=status.HTTP_404_NOT_FOUND)


class UpdateCourseView(generics.ListAPIView, generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseUpdateSerializer
    lookup_field = 'course_id'

    def list(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')

        if not validate_uuid4(course_id):
            return Response({"Course Not Found"}, status=404)

        if not Course.objects.filter(course_id=course_id).exists():
            return Response({"Course Not Found"}, status=404)

        queryset = self.get_queryset().filter(course_id=course_id)
        serializer = CourseUpdateSerializer(queryset, many=True)
        return Response(serializer.data[0], status=200)

    def patch(self, request, *args, **kwargs):
        x = self.update(request, *args, **kwargs)
        if not x:
            return Response({"Invalid Request"}, status=400)


class UpdateCourseBannerView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseBannerUpdateSerializer
    lookup_field = 'course_id'

    def patch(self, request, *args, **kwargs):
        x = self.update(request, *args, **kwargs)
        if not x:
            return Response({"Error": "An Error Occurred"}, status=status.HTTP_400_BAD_REQUEST)


class CourseAdd(generics.ListAPIView, mixins.CreateModelMixin):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer2

    def post(self, request, *args, **kwargs):
        retData = self.create(request, *args, **kwargs)

        response_data = {}
        response_data["data"] = retData.data
        response_data["errors"] = retData.exception  # Exception Handling...
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContentAdd(generics.CreateAPIView, mixins.CreateModelMixin):
    queryset = Content.objects.all()
    serializer_class = ContentAddSerializer

    def post(self, request, *args, **kwargs):
        saveData = self.create(request, *args, **kwargs)
        id = self.kwargs.get("course_id")
        course = Course.objects.get(course_id=id)
        if course.author == self.request.user:
            response_data = {}
            response_data["data"] = saveData.data
            response_data["errors"] = {}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {}
            response_data["data"] = {}
            response_data["errors"] = {"Authorization Failed"}
            return Response(response_data, status=401)

    def perform_create(self, serializer):
        id = self.kwargs.get("course_id")
        course = Course.objects.get(course_id=id)
        print(course.author)
        print(self.request.user)
        if course.author != self.request.user:
            return
        content_query = Content.objects.filter(file_type=True, course_id=course)
        slzr = ContentSerializer(content_query, many=True)
        number = len(slzr.data)
        file_type = self.request.data["file_type"]
        if file_type == "True":
            serializer.save(course_id=course, serial=number+1)
        else:
            serializer.save(course_id=course, serial=-1)


class SetPrerequisites(APIView):

    def post(self, request, *args, **kwargs):
        content_id = request.data['content_id']
        preq_id = request.data['preq_id']
        response_data = {}

        if not (validate_uuid4(content_id) and validate_uuid4(preq_id)):
            response_data['data'] = {}
            response_data['errors'] = {"Content ID or Prerequisite ID Error"}
            return Response(response_data, status=400)

        slzr = PrerequisiteSerializer(data=request.data)
        if slzr.is_valid():
            is_exists1 = Content.objects.filter(content_id=content_id).exists()
            is_exists2 = Content.objects.filter(content_id=preq_id).exists()
            if not (is_exists1 and is_exists2):
                response_data['data'] = {}
                response_data['errors'] = {"Content ID or Prerequisite ID not found"}
                return Response(response_data, status=404)
            if not IsCourseAuthor(self):  # Checking authorization...
                response_data['data'] = {}
                response_data['error'] = {"Request user is not course author"}
                return Response(response_data, status=401)
            content_serial = (Content.objects.get(content_id=content_id)).serial
            preq_serial = (Content.objects.get(content_id=preq_id)).serial
            content_preview = (Content.objects.get(content_id=content_id)).preview
            if content_preview:
                response_data['data'] = {}
                response_data['errors'] = {"Prerequisite condition is not satisfied"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            if (preq_serial < content_serial):
                slzr.save()
                response_data['data'] = slzr.data
                response_data['errors'] = {}
            else:
                response_data['data'] = {}
                response_data['errors'] = {"Prerequisite condition is not satisfied"}
                return Response(response_data, status=400)

        return Response(response_data, status=status.HTTP_200_OK)


@csrf_exempt
def deleteFile(self, request):  # DELETE USING CUSTOM FUNCTION
    id = request.data['content_id']
    is_exists = Content.objects.filter(content_id=id).exists()
    if is_exists:
        file = Content.objects.get(content_id=id)
        file.delete()
        return True
    else:
        return False


def UpdatingContentSerial(self, request, id):
    qu = Content.objects.get(content_id=id)
    course_id = qu.course_id
    del_serial = qu.serial
    # print(del_serial)
    query = Content.objects.filter(course_id=course_id)
    slr = ContentSerializer(query, many=True)
    # print(slr.data)

    for i in slr.data:
        if (i['serial'] > del_serial):
            model = Content.objects.get(serial=i['serial'])
            data = {
                "content_id": model.content_id,
                "course_id": model.course_id,
                "file": model.file,
                "file_type": model.file_type,
                "serial": model.serial - 1,
                "title": model.title,
                "description": model.description
            }
            serializer = ContentSerializer(model, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()


class DeleteCourseContent(APIView):
    lookup_field = 'id'

    def get(self, request, id, *args, **kwargs):
        response_data = {}
        if not validate_uuid4(id):
            response_data['data'] = {}
            response_data['errors'] = {"Content Not Found"}
            return Response(response_data, status=404)

        is_exists = Content.objects.filter(content_id=id).exists()
        if is_exists:
            if not IsCourseAuthor(self):  # Checking authorization...
                response_data['data'] = {}
                response_data['error'] = {"Request user is not course author"}
                return Response(response_data, status=401)
            file = Content.objects.get(content_id=id)
            UpdatingContentSerial(self, request, id)  # Updating Contents Serial
            file.delete()
            response_data['data'] = {"Content Deleted Successfully"}
            response_data['errors'] = {}
        else:
            response_data['data'] = {}
            response_data['errors'] = {"Content Not Found"}
            return Response(response_data, status=404)

        return Response(response_data, status=200)

    # def post(self, request, *args, **kwargs):   # For request data
    #     x = deleteFile(self, request)   # Calling custom function...
    #     response_data = {}
    #     if x:
    #         response_data['data'] = {"Content Deleted Successfully"}
    #     else:
    #         response_data['error'] = {"Content Not Found"}
    #     return Response(response_data, status=200)


def get_prerequisites(self, request, content_id):
    pass
    query = Prerequisite.objects.filter(content_id=content_id)
    serializer = PrerequisiteSerializer(query, many=True)
    data = []
    for i in serializer.data:
        data.append(i['preq_id'])
    return data


class ContentAccess(APIView):
    def get(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')

        if not validate_uuid4(course_id):  # Validating the Course_id(uuid4)
            return Response({"Error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        is_exists_course = Course.objects.filter(course_id=course_id).exists()
        is_exists = Content.objects.filter(course_id=course_id).exists()
        if not is_exists_course:
            return Response({"Error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        elif not is_exists:
            return Response([], status=200)

        cQuery = Content.objects.filter(course_id=course_id)  # Getting all contents related to Course
        cSerializer = ContentAccessSerializer(cQuery, many=True)
        response_data = []
        for i in cSerializer.data:
            content_id = i['content_id']
            i.update({"has_completed": Ulala.objects.filter(content_id=content_id, user_id=self.request.user).exists()})
            i['file'] = COMMON_URL + i['file']
            aQuery = Prerequisite.objects.filter(
                content_id=content_id).exists()  # Checking if content has prerequisite or not
            if aQuery:
                preq_subjects = get_prerequisites(self, request, content_id)  # Getting all Prerequisite contents
                i.update({"prerequisites": preq_subjects})
                preq_id = Prerequisite.objects.get(content_id=content_id)  # Getting the prerequisite id
                preq_id = str(preq_id)
                contentQuery = Ulala.objects.filter(content_id=preq_id, user_id=self.request.user).exists()
                if not contentQuery:
                    i['file'] = None
            else:
                i.update({"prerequisites": None})
            response_data.append(i)

        return Response(response_data, status=200)


class ContentDetailView(APIView):

    def get(self, request, *args, **kwargs):
        content_id = self.kwargs.get('content_id')

        if not validate_uuid4(content_id):
            return Response({"Error": "Content Not Found"}, status=404)

        is_exists = Content.objects.filter(content_id=content_id).exists()
        if not is_exists:
            return Response({"Error": "Content Not Found"}, status=404)
        query = Content.objects.filter(content_id=content_id)
        serializer = ContentAccessSerializer(query, many=True)
        serializer.data[0]['file'] = COMMON_URL + serializer.data[0]['file']
        # Adding Extra Parameters...(Has_Completed, Prerequisites)
        serializer.data[0].update(
            {"has_completed": Ulala.objects.filter(content_id=content_id, user_id=self.request.user).exists()})
        if Prerequisite.objects.filter(content_id=content_id).exists():
            preq_subjects = get_prerequisites(self, request, content_id)  # Getting all Prerequisite contents
            serializer.data[0].update({"prerequisites": preq_subjects})
        else:
            serializer.data[0].update({"prerequisites": None})
        return Response(serializer.data[0], status=status.HTTP_200_OK)


class ContentCompleted(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Ulala.objects.all()
    serializer_class = UlalaSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        content_id = request.data['content_id']
        if not validate_uuid4(content_id):
            response_data['data'] = {}
            response_data['errors'] = {"Content Not Found"}
            return Response(response_data, status=404)

        is_exists = Content.objects.filter(content_id=content_id).exists()
        if is_exists:
            if not IsCourseAuthor(self):        # Checking authorization...
                response_data['data'] = {}
                response_data['error'] = {"Request user is not course author"}
                return Response(response_data, status=401)
            data = self.create(request, *args, kwargs)
            response_data['data'] = data.data
            response_data['errors'] = {}
            return Response(response_data, status=201)
        else:
            response_data['data'] = {}
            response_data['errors'] = {"Content Not Found"}
            return Response(response_data, status=404)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class SetContentPreview(APIView):

    def get(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        is_exists = validate_uuid4(course_id) and Content.objects.filter(course_id=course_id).exists()
        data_context = {}
        if not is_exists:
            data_context['data'] = {}
            data_context['errors'] = {"No Contents Found"}
            return Response(data_context, status=404)
        if not IsCourseAuthor(self):
            data_context['data'] = {}
            data_context['error'] = {"Request user is not course author"}
            return Response(data_context, status=401)
        qs = Content.objects.filter(course_id=course_id, file_type=True)
        slzr = ContentPreviewSerializer(qs, many=True)
        data_context['data'] = slzr.data
        data_context['error'] = {}
        return Response(data_context, status=200)

    def post(self, request, *args, **kwargs):
        data_context = {}
        if not IsCourseAuthor(self):
            data_context['data'] = {}
            data_context['error'] = {"Request user is not course author"}
            return Response(data_context, status=401)
        for data in request.data:
            content_id = data['content_id']
            qs = Prerequisite.objects.filter(Q(content_id=content_id)).exists()
            is_valid = validate_uuid4(content_id)
            if qs or not is_valid:
                data_context['data'] = {}
                data_context['error'] = {"Content ID is not valid"}
                return Response(data_context, status=404)
        for data in request.data:
            content_id = data['content_id']
            model = Content.objects.get(content_id=content_id)
            req_data = {
                "content_id": content_id,
                "preview": "True"
            }
            slzr = ContentPreviewSerializer(model, data=req_data, partial=True)
            if slzr.is_valid():
                slzr.save()
            else:
                data_context['data'] = {}
                data_context['error'] = {"Invalid Request"}
                return Response(data_context, status=400)
        data_context['data'] = {"Contents marked for preview successfully"}
        data_context['error'] = {}
        return Response(data_context, status=200)




class TopFiveRated(APIView):

    def get(self, request):
        qs = Course.objects.all().order_by('-rating')[:6]
        serializer = CourseSerializer(qs, many=True)
        response = CourseResponseFormat(request, serializer)
        return Response(response.data, status=200)




class NewCourse(APIView):

    def get(self, request):
        qs = Course.objects.all().order_by('-date_created')[:6]
        serializer = CourseSerializer(qs, many=True)
        response = CourseResponseFormat(request, serializer)
        return Response(response.data, status=200)




class SearchView(generics.ListAPIView, PaginationHandlerMixin):
    pagination_class = FuckboyPaginagion
    serializer_class = CourseSerializer

    def get_queryset(self):
        qs = Course.objects.all()
        query = self.request.GET.get('q')
        search_item = query.split(" ")
        filtered_data = qs.filter(Q(title__icontains=search_item[0]) | Q(tags__icontains=search_item[0]))
        for item in search_item[1:]:
            filtered_data = filtered_data | qs.filter(Q(title__icontains=item) | Q(tags__icontains=item))
        # SEARCHING USING AUTHOR NAME...
        second_qs = User.objects.all()
        second_filtered_data = second_qs.filter(Q(first_name__icontains=search_item[0]) | Q(last_name__icontains=search_item[0]))
        for item in search_item[1:]:
            second_filtered_data = second_filtered_data | second_qs.filter(Q(first_name__icontains=item) | Q(last_name__icontains=item))
        second_serializer = ProfileSerializer(second_filtered_data, many=True)
        for data in second_serializer.data:
            author_id = data['id']
            if Course.objects.filter(author=author_id).exists():
                filtered_data = filtered_data | qs.filter(author=author_id)
        return filtered_data

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)  # Custom Pagination...
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(queryset, many=True, context={"request": self.request})

            if "count" in serializer.data:  # Checking Dict or Tuple
                serializer.data = serializer.data["results"]

            for data in serializer.data:
                gen_tags = data.get("tags").split("#")
                try:
                    gen_tags.remove("")
                except Exception:
                    pass
                bannerDir = None
                if data['banner'] is not None:
                    substr = str(data.get("banner"))
                    pos = substr.find("/media")
                    substr = substr[pos:]
                    bannerDir = COMMON_URL + substr
                data["banner"] = bannerDir
                data["tags"] = gen_tags
            return Response(serializer.data, status=200)
        except Exception as E:
            return Response({'error': str(E)}, status=status.HTTP_408_REQUEST_TIMEOUT, content_type='application/json')




class TopPurchased(APIView):
    pass




class FreeCourseView(APIView):

    def get(self, request):
        qs = Course.objects.filter(fee=0.0).order_by('-rating')[:6]
        serializer = CourseSerializer(qs, many=True)
        response = CourseResponseFormat(request, serializer)
        return Response(response.data, status=200)



