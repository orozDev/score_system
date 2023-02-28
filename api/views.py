from rest_framework import status, viewsets, filters
from api.serializers import PointSerializer
from api.paginations import StandardResultsSetPagination
from core.models import Point
from api.mixins import PaginationBreaker
from django_filters.rest_framework import DjangoFilterBackend


class PointViewSet(PaginationBreaker, viewsets.ModelViewSet):
    
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    filter_backends = [DjangoFilterBackend, 
                       filters.OrderingFilter, 
                       filters.SearchFilter]
    filterset_fields = ['staff', 'head', 'month', 'year', 'value']
    search_fields = ['value',]
    pagination_class = StandardResultsSetPagination
    
    
    def post(self, request, *args, **kwargs):
        pass
    
    def put(self, request, *args, **kwargs):
        pass
    
    def patch(self, request, *args, **kwargs):
        pass