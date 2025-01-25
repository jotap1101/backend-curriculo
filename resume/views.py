from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utils.helpers import QuerysetHelper
from uuid import UUID
from .models import Resume
from .serializers import ResumeSerializer

# Create your views here.
class GetResumes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            resumes = Resume.objects.all()
            serializer = ResumeSerializer(resumes, many=True)

            data = {
                'status': 'success',
                'count': resumes.count(),
                'data': {
                    'resumes': serializer.data
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
        
class CreateResume(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        
        try:
            if serializer.is_valid():
                if 'employee' in request.data:
                    employee = request.data['employee']
                    try:
                        employee_uuid = UUID(employee)
                        serializer.save(employee_id=employee_uuid)
                    except ValueError:
                        raise ValueError('Invalid employee ID. Please provide a valid UUID.')
                else:
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
        
class DetailResume(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            resume = Resume.objects.get(pk=pk)
            serializer = ResumeSerializer(resume)
            data = {
                'status': 'success',
                'data': {
                    'resume': serializer.data
                }
            }

            return response.Response(data=data, status=status.HTTP_200_OK)
        except Resume.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Resume not found.'
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
        
class UpdateResume(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            resume = Resume.objects.get(pk=pk)
            serializer = ResumeSerializer(resume, data=request.data, partial=False)

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
        except Resume.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Resume not found.'
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
            resume = Resume.objects.get(pk=pk)
            serializer = ResumeSerializer(resume, data=request.data, partial=True)

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
        except Resume.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Resume not found.'
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
        
class DeleteResume(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            resume = Resume.objects.get(pk=pk)
            
            resume.delete()

            data = {
                'status': 'success',
                'message': 'Resume deleted successfully.'
            }

            return response.Response(data=data, status=status.HTTP_204_NO_CONTENT)
        except Resume.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Resume not found.'
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