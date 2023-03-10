from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import Group, RegistrationCode, User
from core.models import Point
from django.utils import timezone
from pprint import pprint

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    

class GroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = '__all__'
        


class PointAsStaffSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Point
        fields = ('id', 'value', 'head', 'month', 'year',)


class UserSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    get_full_name = serializers.CharField(read_only=True)
    point = serializers.IntegerField(read_only=True)
    group = GroupSerializer(many=False)
    
    
    class Meta:
        model = User
        fields = '__all__'
        
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context['request']
        year = request.GET.get('year', int(timezone.now().strftime('%Y')))
        month = request.GET.get('month', int(timezone.now().strftime('%m')))
        if request.user.is_authenticated:
            points_as_staff = Point.objects.filter(
                year=year, month=month, staff=instance, head=request.user)
        
            if points_as_staff.exists():
                serializer = PointAsStaffSerializer(points_as_staff.first(), many=False)
                point_as_staff = serializer.data
            else: 
                point_as_staff = None
        else: 
            point_as_staff = None
     
        ret.setdefault('point_as_staff', point_as_staff)
        return ret        
      
        
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
        