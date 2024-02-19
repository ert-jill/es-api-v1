from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserTypeViewSet

router = DefaultRouter()
router.register(r'user_types', UserTypeViewSet,basename='User Type')

urlpatterns = [
    path('', include(router.urls)),
]