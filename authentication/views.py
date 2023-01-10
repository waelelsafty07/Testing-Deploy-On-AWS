from Utils.RespnseMessage import RespnseMessage
from django.contrib.auth import login
from knox.auth import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from .serializers import ChangePasswordSerializer, ConfirmEmailSerializer, LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication


class RegisterView(APIView, RespnseMessage):
    permission_classes = [AllowAny]

    def SendResposne(self, user, status):
        message = user
        return Response(message, status=status)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.SendResposne(serializer.data, 201)


class LoginView(KnoxLoginView, RespnseMessage):
    permission_classes = [AllowAny]

    def SendResposne(self, message, status):
        return Response(message, status)

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.validated_data
        user, message = serializer
        _, token = AuthToken.objects.create(user)

        login(request, user)
        user = UserSerializer(user)
        message = {"token": token, "message": message, "user": user.data}
        return self.SendResposne(message, 200)


class ChangePasswordView(APIView, RespnseMessage):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def SendResposne(self, user, status):
        message = user
        return Response(message, status=status)

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data,
                                              instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.SendResposne({"message": "Change password successfully"}, 200)


class activateView(APIView, RespnseMessage):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def SendResposne(self, user, status):
        message = user
        return Response(message, status=status)

    def post(self, request):
        serializer = ConfirmEmailSerializer(data=request.data,
                                            instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.SendResposne({"message": "Activate Account Done"}, 200)
