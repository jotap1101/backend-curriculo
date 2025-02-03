from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Candidate
from .serializers import CandidateSerializer
import json

class GetCandidates(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            candidates = Candidate.objects.all()
            serializer = CandidateSerializer(candidates, many=True)
            data = {
                'status': 'success',
                'count': candidates.count(),
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

        print(json.dumps(request.data, indent=4))
        
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

            print(json.dumps(data, indent=4))

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

            print(json.dumps(request.data, indent=4))

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