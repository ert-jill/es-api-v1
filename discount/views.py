from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from user.models import UserUserAccount
from .models import Discount
from .serializers import DiscountSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
class DiscountViewSet(viewsets.ViewSet):


    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={200: DiscountSerializer(many=True)}, tags=["Discount"])
    def list(self, request):
        queryset = Discount.objects.all()
        serializer = DiscountSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=DiscountSerializer, responses={201: DiscountSerializer()}, tags=["Discount"])
    def create(self, request):
        user_account_instance = UserUserAccount.objects.get(pk=request.user.id)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_user=request.user, account=account_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(responses={200: DiscountSerializer()}, tags=["Discount"])
    def retrieve(self, request, pk=None):
        queryset = Discount.objects.all()
        discount = get_object_or_404(queryset, pk=pk)
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=DiscountSerializer, responses={200: DiscountSerializer()}, tags=["Discount"])
    def update(self, request, pk=None):
        discount = Discount.objects.get(pk=pk)
        serializer = DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(request_body=DiscountSerializer, responses={200: DiscountSerializer()}, tags=["Discount"])
    def partial_update(self, request, pk=None):
        discount = Discount.objects.get(pk=pk)
        serializer = DiscountSerializer(discount, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(responses={204: 'No Content'}, tags=["Discount"])
    def destroy(self, request, pk=None):
        discount = Discount.objects.get(pk=pk)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
