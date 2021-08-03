from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'phone', 'email','gender',
    'password', 'is_receptionist','is_manager','is_admin' ] 