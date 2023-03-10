from rest_framework import status, viewsets, filters
from api.permisions import IsHead
from api.serializers import PointSerializer, UpdatePointSerializer
from api.paginations import StandardResultsSetPagination
from core.models import Point
from api.mixins import PaginationBreaker, SerializersByAction, PermissionByAction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


class PointViewSet(PaginationBreaker, PermissionByAction, SerializersByAction, viewsets.ModelViewSet):
    
    queryset = Point.objects.all().order_by('-year', '-month')
    serializer_classes = {
        'list': PointSerializer,
        'retrieve': PointSerializer,
        'create': PointSerializer,
        'update': UpdatePointSerializer,
        'destroy': PointSerializer,
    }
    filter_backends = [DjangoFilterBackend, 
                       filters.OrderingFilter, 
                       filters.SearchFilter]
    filterset_fields = ['staff', 'head', 'month', 'year', 'value']
    search_fields = ['value',]
    permission_classes = {
        'create': [IsAuthenticated, IsHead],
        'list': [IsAuthenticated],
        'update': [IsAuthenticated, IsHead],
        'retrieve': [IsAuthenticated],
        'destroy': [IsAuthenticated, IsHead],
    }
    pagination_class = StandardResultsSetPagination