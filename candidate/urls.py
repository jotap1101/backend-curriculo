from django.urls import path
from .views import *

urlpatterns = [
    path('', GetCandidates.as_view(), name='get_candidates'),
    path('create/', CreateCandidate.as_view(), name='create_candidate'),
    path('<uuid:pk>/detail/', DetailCandidate.as_view(), name='detail_candidate'),
    path('<uuid:pk>/update/', UpdateCandidate.as_view(), name='update_candidate'),
    path('<uuid:pk>/delete/', DeleteCandidate.as_view(), name='delete_candidate'),
]