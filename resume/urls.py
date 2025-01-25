from django.urls import path
from .views import *

urlpatterns = [
    path('', GetResumes.as_view(), name='get_resumes'),
    path('create/', CreateResume.as_view(), name='create_resume'),
    path('<uuid:pk>/detail/', DetailResume.as_view(), name='detail_resume'),
    path('<uuid:pk>/update/', UpdateResume.as_view(), name='update_resume'),
    path('<uuid:pk>/delete/', DeleteResume.as_view(), name='delete_resume'),
]