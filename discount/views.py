from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Discount
from .serializers import DiscountSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
class DiscountViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: DiscountSerializer(many=True)}, tags=["Discounts"])
    def list(self, request):
        queryset = Discount.objects.all()
        serializer = DiscountSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=DiscountSerializer, responses={201: DiscountSerializer()}, tags=["Discounts"])
    def create(self, request):
        
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(responses={200: DiscountSerializer()}, tags=["Discounts"])
    def retrieve(self, request, pk=None):
        queryset = Discount.objects.all()
        discount = get_object_or_404(queryset, pk=pk)
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=DiscountSerializer, responses={200: DiscountSerializer(partial_update=True)}, tags=["Discounts"])
    def update(self, request, pk=None):
        discount = Discount.objects.get(pk=pk)
        serializer = DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(request_body=DiscountSerializer, responses={200: DiscountSerializer()}, tags=["Discounts"])
    def partial_update(self, request, pk=None):
        discount = Discount.objects.get(pk=pk)
        serializer = DiscountSerializer(discount, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(responses={204: 'No Content'}, tags=["Discounts"])
    def destroy(self, request, pk=None):
        discount = Discount.objects.get(pk=pk)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
