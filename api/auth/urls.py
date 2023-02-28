from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)


urlpatterns = [
    path('login/', views.LoginApi.as_view()),
    path('register', views.RegisterApi.as_view()),
    path('profile/', views.ProfileApiView.as_view()),
    path('', include(router.urls)),
    path('', include('rest_registration.api.urls')),
]
