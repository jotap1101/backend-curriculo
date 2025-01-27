from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utils.helpers import QuerysetHelper
from .models import Candidate
from .filters import CandidateFilter
from .serializers import CandidateSerializer

class GetCandidates(APIView):
    permission_classes = [IsAuthenticated]
    filterset_class = CandidateFilter
    queryset = Candidate.objects.all()

    def get(self, request):
        try:
            queryset = self.queryset
            queryset = QuerysetHelper.apply_filters(queryset, self.filterset_class, request.GET)

            search_query = request.GET.get('search', None)
            queryset = QuerysetHelper.apply_search(queryset, search_query, ['first_name', 'last_name'])

            ordering = request.GET.get('ordering', None)
            queryset = QuerysetHelper.apply_ordering(queryset, ordering)

            serializer = CandidateSerializer(queryset, many=True)
            
            data = {
                'status': 'success',
                'count': queryset.count(),
                'data': {
                    'candidates': serializer.data
                }
            }

            return response.Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                'status': 'error',
                'errors': [
                    str(e)
                ]
            }

            return response.Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateCandidate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        
        try:
            if serializer.is_valid():
                serializer.save()

                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            
            errors = serializer.errors
            formatted_errors = {field: error_list for field, error_list in errors.items()}
            data = {
                'status': 'error',
                'errors': formatted_errors
            }

            return response.Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {
                'status': 'error',
                'errors': [
                    str(e)
                ]
            }

            return response.Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DetailCandidate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
            serializer = CandidateSerializer(candidate)
            data = {
                'status': 'success',
                'data': {
                    'candidate': serializer.data
                }
            }

            return response.Response(data=data, status=status.HTTP_200_OK)
        except Candidate.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Candidate not found.'
                ]
            }

            return response.Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            data = {
                'status': 'error',
                'errors': [
                    str(e)
                ]
            }

            return response.Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateCandidate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
            serializer = CandidateSerializer(candidate, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()

                return response.Response(serializer.data, status=status.HTTP_200_OK)
            
            errors = serializer.errors
            formatted_errors = {field: error_list for field, error_list in errors.items()}
            data = {
                'status': 'error',
                'errors': formatted_errors
            }

            return response.Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except Candidate.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Candidate not found.'
                ]
            }

            return response.Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            data = {
                'status': 'error',
                'errors': [
                    str(e)
                ]
            }

            return response.Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
            serializer = CandidateSerializer(candidate, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                return response.Response(serializer.data, status=status.HTTP_200_OK)
            
            errors = serializer.errors
            formatted_errors = {field: error_list for field, error_list in errors.items()}
            data = {
                'status': 'error',
                'errors': formatted_errors
            }

            return response.Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except Candidate.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Candidate not found.'
                ]
            }

            return response.Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            data = {
                'status': 'error',
                'errors': [
                    str(e)
                ]
            }

            return response.Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteCandidate(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)

            candidate.delete()

            data = {
                'status': 'success',
                'message': 'Candidate deleted successfully.'
            }

            return response.Response(data=data, status=status.HTTP_204_NO_CONTENT)
        except Candidate.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Candidate not found.'
                ]
            }

            return response.Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            data = {
                'status': 'error',
                'errors': [
                    str(e)
                ]
            }

            return response.Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)