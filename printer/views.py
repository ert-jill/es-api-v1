from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from printer.models import Printer
from printer.serializers import PrinterSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from user.models import UserUserAccount
# Create your views here.

class PrinterViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Printer'], operation_description="List all printers",responses={200: PrinterSerializer(many=True)})
    def list(self, request):
        queryset = Printer.objects.all()
        serializer = PrinterSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Printer'],
        operation_description="Create a new printer",
        request_body=PrinterSerializer
    )
    def create(self, request):
        user_account_instance = UserUserAccount.objects.get(pk=request.user.id)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        serializer = PrinterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_user=request.user, account=account_instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        tags=['Printer'],
        operation_description="Retrieve a printer by ID",
        responses={200: PrinterSerializer}
    )
    def retrieve(self, request, pk=None):
        queryset = Printer.objects.all()
        printer = get_object_or_404(queryset, pk=pk)
        serializer = PrinterSerializer(printer)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Printer'],
        operation_description="Update a printer by ID",
        request_body=PrinterSerializer,
        responses={200: PrinterSerializer}
    )
    def update(self, request, pk=None):
        printer = Printer.objects.get(pk=pk)
        serializer = PrinterSerializer(printer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(tags=['Printer'], operation_description="Delete a printer by ID")
    def destroy(self, request, pk=None):
        printer = Printer.objects.get(pk=pk)
        printer.delete()
        return Response(status=204)