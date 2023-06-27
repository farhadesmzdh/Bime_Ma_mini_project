from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import User
from .models import ExtendedUser
from .serializers import UserSerializer, LoginSerializer, ChangePasswordSerializer, InsuranceSerializer


class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user.user).key
            data['result'] = 'success'
            data['token'] = token
            data['status'] = status.HTTP_201_CREATED
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            theUser = None
            for user in ExtendedUser.objects.all():
                if user.user.username == serializer.data['username']:
                    theUser = user.user
                    break

            if theUser is None:
                data['result'] = 'failed'
                data[status] = status.HTTP_404_NOT_FOUND
            else:
                if theUser.check_password(serializer.data['password']):
                    data['result'] = 'success'
                    data['status'] = status.HTTP_200_OK
                    try:
                        theUser.auth_token.delete()
                    except (AttributeError, ObjectDoesNotExist):
                        pass
                    data['token'] = Token.objects.create(user=theUser).key
                else:
                    data['result'] = 'failed'
                    data['status'] = 'wrong password'
        else:
            data['result'] = 'failed'
            data[status] = status.HTTP_400_BAD_REQUEST

        return Response(data)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        data = {}
        try:
            request.user.auth_token.delete()
            data['result'] = 'success'
            data['status'] = status.HTTP_200_OK
        except (AttributeError, ObjectDoesNotExist):
            data['result'] = 'failed'
            data[status] = 'server error'

        return Response(data)


class GetInfoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        theUser = None
        for user in ExtendedUser.objects.all():
            if user.user.username == request.data['username']:
                theUser = user
                break
        data = {
            "username": request.user.username,
            "phoneNumber": theUser.phoneNumber
        }
        return Response(data, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if serializer.data.get('new_password') != serializer.data.get('new_password2'):
                return Response({"message": "new passwords are not the same!"},
                                status=status.HTTP_400_BAD_REQUEST)
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'result': 'success',
                'status': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceView(APIView):
    serializer_class = InsuranceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['result'] = 'success'
            data['status'] = status.HTTP_200_OK
        else:
            data['result'] = 'failed'
            data[status] = 'server error'
        return Response(data)
