from rest_framework import serializers
from account.models import User
from api.auth.serializers import UserSerializer
from core.models import Point


class PointSerializer(serializers.ModelSerializer):
    
    head_detail = UserSerializer(many=False, read_only=True, source='head')
    staff_detail = UserSerializer(many=False, read_only=True, source='staff')
    
    class Meta: 
        model = Point
        fields = '__all__'
        
    def validate(self, attrs):
        head = attrs['head']
        staff = attrs['staff']
        year = attrs['year']
        month = attrs['month']
        value = attrs['value']
        
        if head.role != User.HEAD:
            raise serializers.ValidationError({'head': f'{head} должен быть {User.HEAD_TITLE}'})
        
        if staff.role != User.STAFF:
            raise serializers.ValidationError({'staff': f'{staff} должен быть {User.STAFF_TITLE}'})
        
        point = Point.objects.filter(month=month, year=year, head=head, staff=staff)
        if point.exists():
            raise serializers.ValidationError({'year': f'Балл в {month}-{year} с {head} уже существует'})
        
        if head.point - value < 0:
            raise serializers.ValidationError({'value': f'У советника "{head}" не достаточно баллов для выдиления'})
        head.point -= value
        head.save()
        
        return attrs
        
        
class UpdatePointSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Point
        fields = ('value',)
    
    def update(self, instance, validated_data):
  
        value = validated_data['value']
        
        if value > instance.value:
            avarage_point = value - instance.value
            if avarage_point > instance.head.point:
                raise serializers.ValidationError({'value': f'У советника "{instance.head}" не достаточно баллов для выдиления'})
            instance.head.point -= avarage_point
            instance.head.save()
        else:
            avarage_point = instance.value - value
            instance.head.point += avarage_point
            instance.head.save()

        return super().update(instance, validated_data)       
        
    
        