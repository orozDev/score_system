from rest_framework.settings import api_settings
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework import status

from utils.constants import USE_PAGINATION
from utils.utils import make_bool

import django


class SerializersByAction(object):
    
    serializer_classes: dict
    
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return self.serializer_classes.get('update', None)
        return self.serializer_classes.get(self.action, None)  
        
        
class PermissionByAction(object):
    
    permission_classes_by_action : dict = {
        'create': api_settings.DEFAULT_PERMISSION_CLASSES,
        'list': api_settings.DEFAULT_PERMISSION_CLASSES,
        'update': api_settings.DEFAULT_PERMISSION_CLASSES,
        'retrieve': api_settings.DEFAULT_PERMISSION_CLASSES,
        'destroy': api_settings.DEFAULT_PERMISSION_CLASSES,
    }
    
    def get_permissions(self):
       
        default_permission = api_settings.DEFAULT_PERMISSION_CLASSES
        permission_classes = self.permission_classes_by_action.get(self.action, None)  
        if self.action == "update_partial":
            permission_classes = self.permission_classes_by_action['update']
        if permission_classes is None:
            permission_classes = default_permission

        return [permission() for permission in permission_classes]
    

class PermissionByMethod(object):
    
    permission_classes_by_method : dict = {
        'get': api_settings.DEFAULT_PERMISSION_CLASSES,
        'post': api_settings.DEFAULT_PERMISSION_CLASSES,
        'delete': api_settings.DEFAULT_PERMISSION_CLASSES,
        'put': api_settings.DEFAULT_PERMISSION_CLASSES,
        'patch': api_settings.DEFAULT_PERMISSION_CLASSES,
        'options': api_settings.DEFAULT_PERMISSION_CLASSES,
    }
    
    def get_permissions(self):
        
        method = self.request.method.lower()
        default_permission = api_settings.DEFAULT_PERMISSION_CLASSES
        permission_classes = self.permission_classes_by_method.get(method, None)
        if permission_classes is None:
            permission_classes = default_permission
        return [permission() for permission in permission_classes]
    

class PaginationBreaker(object):
    
    def _break_pagination(self, request):
        use_pagination = make_bool(request.GET.get(USE_PAGINATION, True))
        if not use_pagination:
            self.pagination_class = None
    
    def get(self, request, *args, **kwargs):
        self._break_pagination(request)
        return super().get(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        self._break_pagination(request)
        return super().list(request, *args, **kwargs)
        
    

class DetailResopnse(object):
    
    """ Works only with UpdateMixin """
    
    detail_serializer: Serializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
            
        detail_serializer = self.detail_serializer(instance, many=False)

        return Response(detail_serializer.data)



class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except django.db.models.deletion.ProtectedError as e:
            return Response(status=status.HTTP_423_LOCKED, data={'detail': str(e)})
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
