from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TableViewSet

router = DefaultRouter()
router.register(r'tables', TableViewSet, basename="tables")

urlpatterns = [
    path('', include(router.urls)),
]