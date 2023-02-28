from rest_framework import serializers
from api.auth.serializers import UserSerializer
from core.models import Point


class PointSerializer(serializers.ModelSerializer):
    
    head_detail = UserSerializer(many=False, read_only=True, source='head')
    staff_detail = UserSerializer(many=False, read_only=True, source='staff')
    
    class Meta: 
        model = Point
        fields = '__all__'
        
        