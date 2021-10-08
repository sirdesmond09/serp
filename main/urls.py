from django.urls import path
from . import views


app_name = 'main'



urlpatterns = [
    path('users/', views.users),
    path('users/<int:user_id>', views.user_detail),
    path('users/login/', views.user_login),
    path('employees/', views.employees),
    path('employees/<int:employee_id>/', views.employee_detail),
    path('designation/', views.designation),
    path('designation/<int:designation_id>/', views.designation_detail),
    path('customers/', views.customer),
    path('customers/<int:customer_id>/', views.customer_detail),
    path('services/', views.service),
    path('services/<int:service_id>/', views.service_detail),
    path('invoices/', views.invoice),
    path('invoices/<int:invoice_id>/', views.invoice_detail),
    path('invoices/<int:invoice_id>/services/<int:service_rendered_id>/', views.invoice_item_edit),
]
