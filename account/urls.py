from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet

# URL Configuration for account app
router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')

urlpatterns = [
    # path("find/<int:pk>/", views.get_account_by_id, name="find"),
    # path("all/", views.get_accounts, name="all"),
    # path("post/", views.insert, name="add"),
    # # path("put/", views.insert, name="update"),
    # path('update/<int:pk>/', views.update, name='update'),
     path('', include(router.urls)),
]
