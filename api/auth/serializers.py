from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from account.models import User
from core.models import Point

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    

class PointAsStaffSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Point
        fields = ('id', 'value', 'head', 'month', 'year',)


class UserSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    get_full_name = serializers.CharField(read_only=True)
    point = serializers.IntegerField(read_only=True)
    points_as_staff = PointAsStaffSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = User
        fields = '__all__'
        
        extra_kwargs = {
            'password': {'write_only': True},
        }
        

class ProfileSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = (
            'avatar',
            'first_name',
            'last_name',
            'group',
            'email',
        )
        