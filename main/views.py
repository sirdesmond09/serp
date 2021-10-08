from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsManagerPermission, IsOwnerPermission
from users.models import User
from users.serializer import UserSerializer

from .models import Designation, Employee, Customer, Invoice, InvoiceServices, Service
from .serializer import DesignationSerializer, EmployeeSerializer, CustomerSerializer, InvoiceSerializer, InvoiceServiceSerializer, ServiceSerializer, LoginSerializer

import random
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth import authenticate
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from django.conf import settings
from django.contrib.auth.signals import user_logged_in

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(method='post', request_body=UserSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsOwnerPermission])
def users(request):
    if request.method == 'GET':
        users =User.objects.filter(is_active=True)
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            numbers = [str(i) for i in range(10)]
            password = ''.join(random.choice(numbers) for i in range(8))
            created_user = User.objects.create(**serializer.validated_data)
            created_user.set_password(password)
            created_user.save()

            print(f"{created_user.email}\n{password}")
            serializer = UserSerializer(created_user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=UserSerializer())
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsOwnerPermission])
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    try:
        obj = User.objects.get(id=user_id )
    except User.DoesNotExist:
        return Response(data={'detail':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj.delete()

        return Response(data = {'message':'successful'}, status=status.HTTP_204_NO_CONTENT)


#Login as a user or customer
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
))
@api_view([ 'POST'])
def user_login(request):
    
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(request, email = serializer.validated_data['email'], password = serializer.validated_data['password'])
            if user is not None:

                if user.is_active:
                    try:
                        payload = jwt_payload_handler(user)
                        token = jwt.encode(payload, settings.SECRET_KEY)
                        user_details = {}
                        user_details['id']   = user.id
                        user_details['first_name'] = user.first_name
                        user_details['last_name'] = user.last_name
                        user_details['email'] = user.email
                        user_details['gender'] = user.gender
                        user_details['is_receptionist'] = user.is_receptionist
                        user_details['is_manager'] = user.is_manager
                        user_details['is_admin'] = user.is_admin
                        user_details['date_added'] = user.date_added
                        user_details['token'] = token
                        user_logged_in.send(sender=user.__class__,
                                            request=request, user=user)

                        return Response(user_details, status=status.HTTP_200_OK)


                    except Exception as e:
                        raise e

                else:
                    
                    return Response({'errors': 'Does not have permission or the account has been deactivated'}, status=status.HTTP_403_FORBIDDEN)
                    

            else:
                return Response({'message': 'Please provide valid a email and a password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=EmployeeSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsManagerPermission])
def employees(request):
    if request.method == 'GET':
        obj = Employee.objects.filter(is_active=True)
        serializer = EmployeeSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=EmployeeSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsManagerPermission])
def employee_detail(request, employee_id):
    try:
        obj = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response(data={'detail':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = EmployeeSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj.delete()

        return Response(data = {'message':'successful'}, status=status.HTTP_204_NO_CONTENT)





@swagger_auto_schema(method='post', request_body=CustomerSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def customer(request):
    if request.method == 'GET':
        obj = Customer.objects.filter(is_active=True)
        serializer = CustomerSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=CustomerSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def customer_detail(request, customer_id):
    try:
        obj = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response(data={'detail':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj.delete()

        return Response(data = {'message':'successful'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='post', request_body=ServiceSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def service(request):
    if request.method == 'GET':
        obj = Service.objects.filter(is_active=True)
        serializer = ServiceSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=ServiceSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsManagerPermission])
def service_detail(request, service_id):
    try:
        obj = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return Response(data={'detail':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ServiceSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj.delete()

        return Response(data = {'message':'successful'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='post', request_body=InvoiceSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def invoice(request):
    if request.method == 'GET':
        obj = Invoice.objects.filter(is_active=True)
        serializer = InvoiceSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=InvoiceSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def invoice_detail(request, invoice_id):
    try:
        obj = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return Response(data={'detail':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvoiceSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = InvoiceSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj.delete()

        return Response(data = {'message':'successful'}, status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(method='put', request_body=InvoiceServiceSerializer())
@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def invoice_item_edit(request, invoice_id, service_rendered_id):
    try:
        obj = Invoice.objects.get(id=invoice_id)
        item = InvoiceServices.objects.get(invoice=obj, id=service_rendered_id)
    except Exception:
        return Response(data={'detail':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'PUT':
        serializer = InvoiceServiceSerializer(item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()

        return Response(data = {'message':'successful'}, status=status.HTTP_204_NO_CONTENT)
    

@swagger_auto_schema(method='post', request_body=CustomerSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def designation(request):
    if request.method == 'GET':
        obj = Designation.objects.filter(is_active=True)
        serializer = DesignationSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = DesignationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=DesignationSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def designation_detail(request, designation_id):
    try:
        obj = Designation.objects.get(id=designation_id)
    except Designation.DoesNotExist:
        return Response(data={'detail':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DesignationSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = DesignationSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj.delete()

        return Response(data = {'message':'successful'}, status=status.HTTP_204_NO_CONTENT)
