from rest_framework import status, viewsets, filters
from api.serializers import PointSerializer, UpdatePointSerializer
from api.paginations import StandardResultsSetPagination
from core.models import Point
from api.mixins import PaginationBreaker, SerializersByAction
from django_filters.rest_framework import DjangoFilterBackend


class PointViewSet(PaginationBreaker, SerializersByAction, viewsets.ModelViewSet):
    
    queryset = Point.objects.all()
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
    pagination_class = StandardResultsSetPagination