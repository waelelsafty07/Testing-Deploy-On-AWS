# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .models import Users
from .serializers import UserSerializer
from Utils.checkauth import Checkauth
from Utils.RespnseMessage import RespnseMessage
from Utils.unauthorizationSend import unauthorizationSend
from Utils.serializerData import serializerData


class usersDetailView(APIView, RespnseMessage):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def SendResposne(self, message, status):
        if message:
            return Response(message, status)
        else:
            return Response(status)

    def get(self, request, pk):
        print(pk)
        try:
            unAuthSend = unauthorizationSend(Checkauth().check(request, pk), self.SendResposne(
                {"message": "unauthorized"}, 401))
            if unAuthSend.check():
                return unAuthSend.Send()
            user = Users.objects.get(pk=pk)
            user = UserSerializer(user)
            return self.SendResposne(user.data, 200)
        except Users.DoesNotExist:
            return self.SendResposne(404)

    def put(self, request, pk):
        try:
            unAuthSend = unauthorizationSend(Checkauth().check(request, pk), self.SendResposne(
                {"message": "unauthorized"}, 401))
            if unAuthSend.check():
                return unAuthSend.Send()
            user = Users.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Return Response
            print(serializer)
            return self.SendResposne({"data": serializer.data}, 200)
        except Users.DoesNotExist:
            self.SendResposne(404)

    def patch(self, request, pk):
        try:
            unAuthSend = unauthorizationSend(Checkauth().check(request, pk), self.SendResposne(
                {"message": "unauthorized"}, 401))

            if unAuthSend.check():
                return unAuthSend.Send()

            Users.objects.filter(pk=pk).update(is_active=False)
            return self.SendResposne({"message": "Account will be deleted in  29 days, and you can't retreive it again \n\tYou can login again to active your account in 29 days"}, 200)
        except Users.DoesNotExist:
            self.SendResposne(404)


class usersView(APIView, RespnseMessage):
    def SendResposne(self, message, status):
        if message:
            return Response(message, status)
        else:
            return Response(status)

    def get(self, request):
        users = UserSerializer(
            Users.objects.all(), many=True)
        serializer = serializerData(users).Get()
        return self.SendResposne({"users": serializer.data}, 200)
