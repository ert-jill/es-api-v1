from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrinterViewSet

router = DefaultRouter()
router.register(r'printers', PrinterViewSet,basename='printers')

urlpatterns = [
    path('', include(router.urls)),
]