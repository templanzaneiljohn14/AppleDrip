from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from core.authentication import create_access_token, JWTAuthentication, create_refresh_token, decode_refresh_token
from rest_framework.authentication import get_authorization_header
from core.models import User, Posts, UserGallery
from .serializers import PostsSerializer, UserGalleriesSerializer, UserSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException("Password not match")
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserApiView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class LoginApiView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid credentials")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid credentials")
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }
        return response

class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })

class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message': 'success'
        }
        return response


# Post to wall insert sample
class PostsAPIView(APIView): 
    # def post(self, request):
    #     data = request.data
    #     if data['content'] == '':
    #         raise exceptions.APIException("Content is required.")
    #     serializer = PostsSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    parser_classes = [MultiPartParser, FormParser]


    def post(self, request, format=None):
        print(request.data)
        data = request.data
        serializer = PostsSerializer(data=data)
        serializer1 = UserGalleriesSerializer(data=data)
        
        if serializer.is_valid() and serializer1.is_valid():
            serializer.save()
            serializer1.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
             return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
         
    def get(self, request):
        post_lists = Posts.objects.all()
        serializer = PostsSerializer(post_lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGalleriesAPIView(APIView):
    def get(self, request):
        list_galleries = UserGallery.objects.all()
        serializer = UserGalleriesSerializer(list_galleries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#     pass

# API TO CREATE

# NEIL
# DATABASE : core_posts
# FETCH POSTS DATA
# UPDATE POSTS DATA BY POST_ID
# DELETE POSTS DATA BY POST_ID

# DATABASE : core_user
# FETCH USER BY ID

# DATABASE : core_usergallery
# INSERT POST IMAGE . IF POST DATA HAS IMAGE THEN SAVE IT
# FETCH ALL IMAGE DATA
# DELETE IMAGE DATA BY POST_ID

#///////////////////////////////
# VINCENT
# DATABASE : core_groups
# INSERT GROUP DATA
# FETCH ALL GROUPS DATA
# FETCH GROUP BY ID
# UPDATE GROUP NAME
# DELETE GROUP BY ID

# DATABASE : core_groupmember
# INSERT GROUP MEMBER TO GROUP
# DELETE MEMBER TO GROUP BY USER_ID AND GROUP ID

# ///////////////////////////////
# RONALD
# DATABASE : core_message
# INSERT MESSAGE DATA
# FETCH USER MESSAGE BY SENDER_ID AND RECEIVER_ID
# UPDATE MESSAGE CONTENT BY MESSAGE_ID
# DELETE MESSAGE BY MESSAGE_ID

# DATABASE : core_userfollowers
# INSERT FOLLOWER DATA
# FETCH ALL FOLLOWERS
# FETCH FOLLOWING BY USER_ID
# DELETE FOLLOWER DATA
