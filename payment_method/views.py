from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import PaymentMethod
from .serializers import PaymentMethodSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

class PaymentMethodViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: PaymentMethodSerializer(many=True)},
        operation_summary="List all payment methods",
        tags=["Payment Methods"],
    )
    def list(self, request):
        queryset = PaymentMethod.objects.all()
        serializer = PaymentMethodSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PaymentMethodSerializer,
        responses={201: PaymentMethodSerializer()},
        operation_summary="Create a payment method",
        tags=["Payment Methods"],
    )
    def create(self, request):
        request.data['created_by_user'] = request.user.id
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: PaymentMethodSerializer()},
        operation_summary="Retrieve a payment method",
        tags=["Payment Methods"],
    )
    def retrieve(self, request, pk=None):
        queryset = PaymentMethod.objects.all()
        payment_method = get_object_or_404(queryset, pk=pk)
        serializer = PaymentMethodSerializer(payment_method)
        return Response(serializer.data)    

    @swagger_auto_schema(
        request_body=PaymentMethodSerializer,
        responses={200: PaymentMethodSerializer()},
        operation_summary="Update a payment method",
        tags=["Payment Methods"],
    )
    def update(self, request, pk=None):
        try:
            payment_method = PaymentMethod.objects.get(pk=pk)
        except PaymentMethod.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentMethodSerializer(payment_method, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: None},
        operation_summary="Delete a payment method",
        tags=["Payment Methods"],
    )
    def destroy(self, request, pk=None):
        try:
            payment_method = PaymentMethod.objects.get(pk=pk)
        except PaymentMethod.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        payment_method.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
