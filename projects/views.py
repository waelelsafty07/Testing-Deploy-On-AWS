from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from .serializers import ProjectSerializer
from .models import Projects
from .filters import ProjectFilters

import sys


class ProjectView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):

    queryset = Projects.objects.filter()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = ProjectFilters

    def get(self, request):
        return self.list(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # create a new album

    def post(self, request):
        if not hasattr(request, "user"):
            return Response(status=403, data={'message': 'You must be artist'})
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
