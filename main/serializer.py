from rest_framework import serializers
from .models import Designation, Employee, Customer, Invoice, InvoiceServices, Service
import uuid
from django.utils import timezone


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 200)


    
class EmployeeSerializer(serializers.ModelSerializer):
    designation_details = serializers.ReadOnlyField()
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'designation', 'designation_details', 'hour_rate', 'phone', 'email', 'address1', 'address2', 'state', 'city', 'picture_url', 'country', 'is_active', 'date_added']


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Service
        fields = '__all__'

class InvoiceServiceSerializer(serializers.ModelSerializer):
    service_detail = serializers.ReadOnlyField()
    class Meta:
        model = InvoiceServices
        fields = ['id', 'invoice', 'service', 'service_detail','quantity', 'charge', 'is_active', 'date_added']
        

class InvoiceSerializer(serializers.ModelSerializer):
    service_rendered = InvoiceServiceSerializer(many=True)
    employee_detail = serializers.ReadOnlyField()
    customer_detail = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = ['id','invoice_num' ,
    'customer','customer_detail' ,'employee', 'employee_detail',
    'sub_total','vat',
    'grand_total',
    'is_active',
    'date_added', 'service_rendered']

    # def validate_employee(self, value):
    #     if type(value) == list and len(value) != 0:
    #         return value

    def create(self, validated_data):
        employees_ = validated_data.pop('employee')
        time_ = timezone.now().strftime("%Y%m%d")
        code = str(uuid.uuid4()).split("-")[2]
        invoice_num = f'serv-{time_}{code}'
        service_data = validated_data.pop('service_rendered')
        invoice = Invoice.objects.create(invoice_num=invoice_num,**validated_data)
        invoice.employee.set(employees_)
        invoice.save()
        
        for data in service_data:
            InvoiceServices.objects.create(invoice=invoice, **data)
        return invoice
    
    def update(self, instance, validated_data):
        print(validated_data)
        instance.invoice_num = validated_data.get('invoice_num', instance.invoice_num)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.employee.set(validated_data.get('employee', instance.employee))
        instance.sub_total = validated_data.get('sub_total', instance.sub_total)
        instance.vat = validated_data.get('vat', instance.vat)
        instance.grand_total = validated_data.get('grand_total', instance.grand_total)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.date_added = validated_data.get('date_added', instance.date_added)

        instance.save()
        return instance


class DesignationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Designation
        fields = '__all__'