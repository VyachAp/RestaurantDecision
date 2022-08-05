from django.contrib.auth.models import User
from restdecision.serializers import CreateUserSerializer, RegisterSerializer
from restdecision.utils.password import generate_password
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from collections import OrderedDict


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        # Crutch to obtain password in response
        data = OrderedDict()
        data.update(request.data)
        data["password"] = generate_password()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
