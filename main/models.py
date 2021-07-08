from django.db import models
# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=250)
    last_name  = models.CharField(max_length=250)
    designation = models.CharField(max_length=250)
    hour_rate = models.FloatField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    address1 = models.TextField()
    address2 = models.TextField()
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    picture_url = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.first_name

    def delete(self):
        self.is_active = False
        self.save()
        return 



class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, )
    address_1 = models.CharField(max_length=255, null=True, blank=True)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255,null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField( auto_now_add=True)


    def __str__(self) -> str:
        return self.name

    def delete(self) -> None:
        self.is_active = False
        self.save()
        return 




class Service(models.Model):
    service_name = models.CharField(max_length=255)
    charge = models.FloatField()
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField( auto_now_add=True)


    def __str__(self) -> str:
        return self.service_name

    def delete(self) -> None:
        self.is_active = False
        self.save()
        return 


class Invoice(models.Model):
    invoice_num = models.CharField(max_length=70, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='invoice')
    employee = models.ManyToManyField(Employee, related_name='work_done')
    sub_total = models.FloatField()
    vat = models.FloatField()
    grand_total = models.FloatField()
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField( auto_now_add=True)


    def __str__(self) -> str:
        return self.invoice_num

    def delete(self):
        self.is_active = False
        self.save()
        return

    @property
    def employee_names(self):
        employees = self.employee.all()
        return {employee.id: f"{employee.first_name} {employee.last_name}" for employee in employees} 


class InvoiceServices(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='service_rendered', on_delete=models.DO_NOTHING, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, related_name='services')
    quantity = models.IntegerField(default=1)
    charge = models.FloatField()
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField( auto_now_add=True)

    def __str__(self) -> str:
        return f"Service for {self.invoice.invoice_num}"

    def delete(self):
        self.is_active = False
        self.save()
        return

### owner@serp.co | mama2020