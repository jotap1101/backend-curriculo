from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeSerializer

class GetEmployees(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            data = {
                'status': 'success',
                'count': employees.count(),
                'data': {
                    'employees': serializer.data
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
    
class CreateEmployee(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        
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
        
class DetailEmployee(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(id=pk)
            serializer = EmployeeSerializer(employee)
            data = {
                'status': 'success',
                'data': {
                    'employee': serializer.data
                }
            }

            return response.Response(data=data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Funcionário não encontrado.'
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
        
class UpdateEmployee(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data, partial=False)

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
        except Employee.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Funcionário não encontrado.'
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
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)

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
        except Employee.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Funcionário não encontrado.'
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
        
class DeleteEmployee(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()

            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            data = {
                'status': 'error',
                'errors': [
                    'Funcionário não encontrado.'
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