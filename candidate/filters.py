from django_filters import rest_framework
from .models import Candidate

class CandidateFilter(rest_framework.FilterSet):
    has_disability = rest_framework.BooleanFilter(field_name='has_disability')
    has_drivers_license = rest_framework.BooleanFilter(field_name='has_drivers_license')
    is_first_job = rest_framework.BooleanFilter(field_name='is_first_job')

    class Meta:
        model = Candidate
        fields = ['has_disability', 'has_drivers_license', 'is_first_job']