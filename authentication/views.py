import json

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers import TokenSerializer, RegisterSerializer, UserSerializer
from authentication.utils import send_activation_email


class TokenView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return TokenSerializer


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        # lang = self.request.query_params.get('lang')

        if User.objects.filter(email=data['email']).exists():
            obj = User.objects.get(email=data['email'])
            temp_password = BaseUserManager().make_random_password()
            obj.set_password(temp_password)
            obj.save()

            send_activation_email(obj, request, temp_password)  # TODO add lang after english prepared
            return Response(data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        data = json.loads(request.body.decode('utf-8'))

        if not user.check_password(data.get("oldPassword")):
            return Response({"message": ["Old password is incorrect."]}, status=status.HTTP_400_BAD_REQUEST)

        if data.get("newPassword1") == data.get("newPassword2"):
            user.set_password(data.get("newPassword1"))
            user.save()
        else:
            return Response({"message": ["Passwords don't match."]}, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': ['Password changed successfully!'],
            'data': []
        }

        return Response(response)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UsersView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_paginated_response(self, data):
        return Response(data)
