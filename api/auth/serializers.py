from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import RegistrationCode, User
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
        

class RegisterUserSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True, 
            validators=[MinValueValidator(10000), MaxValueValidator(99999)])
    
    
    class Meta:
        model = User
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'code',
            'password',
            'phone',
            'email',
            'role',
            'group',
        ]
        
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def validate(self, attrs):
        code_verification = RegistrationCode.objects.filter(code=attrs['code'], role=attrs['role'])
        if not code_verification.exists():
            raise serializers.ValidationError({'code': [_('Неверный код или не существует')]})
        return attrs
         
    def create(self, validated_data):
        changed_data = validated_data
        changed_data.pop('code', None)
        user = User.objects.create(**changed_data)
        
        user.set_password(validated_data['password'])
        user.save()

        return user
        

        

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
        