# views.py

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from user.models import UserUserAccount
from .models import Area
from .serializers import AreaSerializer
from drf_yasg.utils import swagger_auto_schema

class AreaViewSet(viewsets.ViewSet):
    @swagger_auto_schema(tags=["Area"], responses={200: AreaSerializer(many=True)})
    def list(self, request):
        queryset = Area.objects.all()
        serializer = AreaSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=["Area"], request_body=AreaSerializer, responses={201: AreaSerializer()})
    def create(self, request):
        user_account_instance = UserUserAccount.objects.get(pk=request.user.id)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        serializer = AreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_user = request.user,account=account_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Area"], responses={200: AreaSerializer()})
    def retrieve(self, request, pk=None):
        queryset = Area.objects.all()
        area = get_object_or_404(queryset, pk=pk)
        serializer = AreaSerializer(area)
        return Response(serializer.data)

    @swagger_auto_schema(tags=["Area"], request_body=AreaSerializer, responses={200: AreaSerializer()})
    def update(self, request, pk=None):
        area = Area.objects.get(pk=pk)
        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Area"], responses={204: "No Content"})
    def destroy(self, request, pk=None):
        area = Area.objects.get(pk=pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
