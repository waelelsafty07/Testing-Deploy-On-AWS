from users.serializers import UserSerializer
from rest_framework import serializers
from .models import Projects


class ProjectSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        default='Project', max_length=100, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Projects
        fields = "__all__"
