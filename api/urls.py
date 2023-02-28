from rest_framework import routers
from django.urls import path, include
from .yasg import urlpatterns as url_doc
from . import views

router = routers.DefaultRouter()
router.register('points', views.PointViewSet)

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls)),
]

urlpatterns += url_doc