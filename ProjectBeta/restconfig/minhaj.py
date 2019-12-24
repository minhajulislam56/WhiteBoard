from uuid import UUID
from ProjectBeta.settings import COMMON_URL
from rest_framework import pagination

def CourseResponseFormat(request, serializer):

    for i in range(0, len(serializer.data)):
        gen_tags = serializer.data[i].get("tags").split("#")
        print(gen_tags)
        try:
            gen_tags.remove("")
        except ValueError:
            pass
        bannerDir = None
        if serializer.data[i]['banner'] is not None:
            bannerDir = COMMON_URL + str(serializer.data[i].get("banner"))
        serializer.data[i]["tags"] = gen_tags
        serializer.data[i]["banner"] = bannerDir
    return serializer


def validate_uuid4(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False
    return True


class FuckboyPaginagion(pagination.PageNumberPagination):
    page_size_query_param = 'limit'