from django_filters import rest_framework as filters
from .models import Projects


class ProjectFilters(filters.FilterSet):

    class Meta:
        model = Projects
        fields = {
            'name': ['icontains']
        }
