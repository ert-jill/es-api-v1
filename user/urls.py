from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Create a router and register the UserViewSet with it
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
# URL Configuration for account appfrom rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'users', UserViewSet)
# router.register(r'accounts', AccountViewSet)
# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
]
