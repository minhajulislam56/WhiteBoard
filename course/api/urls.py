from django.urls import path, include
from .views import (
    CourseView,
    CourseAdd,
    CourseViewSingle,
    ContentAdd,
    SetPrerequisites,
    DeleteCourseContent,
    CourseViewUser,
    ContentAccess,
    ContentDetailView,
    ContentCompleted,
    UpdateCourseView,
    UpdateCourseBannerView,
    SetContentPreview,
    TopFiveRated,
    NewCourse,
    SearchView,
)


urlpatterns = [
    path('course/', CourseView.as_view()),
    path('course/search/', SearchView.as_view()),
    path('course/<course_id>/', CourseViewSingle.as_view()),
    path('course/<course_id>/update/', UpdateCourseView.as_view()),
    path('course/<course_id>/ban-update/', UpdateCourseBannerView.as_view()),
    path('course-add/', CourseAdd.as_view()),
    path('course/<course_id>/add/', ContentAdd.as_view()),
    path('course/<course_id>/completed/', ContentCompleted.as_view()),
    path('course/<course_id>/contents/', ContentAccess.as_view()),
    path('course/<course_id>/content-prev/', SetContentPreview.as_view()),
    path('course/<course_id>/contents/<content_id>/', ContentDetailView.as_view()),
    path('course/<course_id>/set-preq/', SetPrerequisites.as_view()),
    path('course/<course_id>/<str:id>/', DeleteCourseContent.as_view()),
    path('<user_id>/course/', CourseViewUser.as_view()),
    path('top/r/', TopFiveRated.as_view()),
    path('top/n/', NewCourse.as_view()),
]





