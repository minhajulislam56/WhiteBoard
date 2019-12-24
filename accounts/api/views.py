from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics, status, mixins
from django.contrib.auth import authenticate, get_user_model
from .serializers import ProfileSerializer, ProfileUpdateSerializer, ProfilePictureSerializer
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
from django.db.models import Q
from ProjectBeta.settings import COMMON_URL
import json
from .permissions import AnonymousPermissionOnly

User = get_user_model()

# class ProfileLoad(generics.ListAPIView):
#
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get_queryset(self, *args, **kwargs):
#         username = self.kwargs.get('username', None)
#         if username is not None:
#             x= User.objects.filter(username=username)
#             return x
#         return User.objects.none

class ProfileLoad(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, *args, **kwargs):
        username = self.kwargs.get('username', None)
        if username is not None:
            qu = User.objects.filter(Q(username__iexact=username) | Q(id__iexact=username))

            if qu.count() == 0:
                return Response({"Error": "Profile Not Found"}, status=404)     # User Not Found in Database

            serializer = ProfileSerializer(qu, many=True)
            if serializer.data[0]['profile_pic'] is not None:
                serializer.data[0]['profile_pic'] = COMMON_URL + serializer.data[0]['profile_pic']
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return Response({"Error": "Profile Not Found"}, status=status.HTTP_404_NOT_FOUND)




class UpdateProfile(generics.ListAPIView, generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'username'

    def list(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        if username != str(self.request.user):
            return Response({"Invalid Request"}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset().filter(username=self.request.user)
        serializer = ProfileUpdateSerializer(queryset, many=True)
        return Response(serializer.data[0], status=200)

    def patch(self, request, *args, **kwargs):
        x = self.update(request, *args, **kwargs)
        if not x:
            return Response({"Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)



class ProfilePictureUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePictureSerializer
    lookup_field = 'username'

    def patch(self, request, *args, **kwargs):
        x = self.update(request, *args, **kwargs)
        response_data = {}
        if not x:
           return Response({"Error": "Error Occurred"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    # permission_classes = [AnonymousPermissionOnly]

    def post(self, request, *args, **kwargs):

        # print(request.user)
        if request.user.is_authenticated:
            print(request.headers)
            return Response({"detail" : "You are already authenticated"})

        data = request.data
        username = data.get('email')
        password = data.get('password')
        # user = authenticate(username = username, password = password)
        # print(user)
        qs = User.objects.filter(
            Q(username__iexact = username)|
            Q(email__iexact = username)
        ).distinct()
        # print(qs)
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj

                #Creating a new token manually
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request= request)
                return Response(response, status = status.HTTP_200_OK)
            else:
                return Response({"Error": "Password Not Matched"}, status=401)
        else:
            return Response({"Detail" : "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)




class RegisterAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return Response({"Detail" : "You are already authenticated"})

        data = request.data

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username') # username or email address
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('confirmPassword')

        qs = User.objects.filter(
            Q(username__iexact = username)
            #Q(email__iexact = email)
        )
        response_data = {}
        data = {}
        flag = False
        if password != password2:
            flag = True
            data.update({"password":"Passwords not matched"})
            #return Response({"Password": "Passwords don't matched"})
        if qs.exists():
            flag = True
            data.update({"username":"username already exists"})
            #return Response(response_data)

        qe = User.objects.filter(
            Q(email__iexact = email)
        )
        if qe.exists():
            flag = True
            data.update({"email":"email already exists"})

        if flag:
            response_data['data'] = {}
            response_data['errors'] = data
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create(username = username, email = email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            response = jwt_response_payload_handler(token, user, request=request)

            #Formatting
            response_data = {}
            response_data['data'] = response
            response_data['errors'] = {}

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"Detail": "Invalid request"}, status=status.HTTP_404_NOT_FOUND)


from.serializers import UpdateSerializer
class Test(mixins.UpdateModelMixin, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateSerializer
    lookup_field = 'username'

    def list(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        if username != str(self.request.user):
            return Response({"Invalid Request"}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset().filter(username=self.request.user)
        serializer = UpdateSerializer(queryset, many=True)
        return Response(serializer.data[0], status=200)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
