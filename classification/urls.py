from django.urls import path, include
from rest_framework.routers import DefaultRouter
from classification.views import ClassificationViewSet

router = DefaultRouter()
router.register(r'classifications', ClassificationViewSet, basename='classification')

urlpatterns = [
     path('', include(router.urls)),
]