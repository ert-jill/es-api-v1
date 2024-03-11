from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from user.models import UserUserAccount

from user.tokens import get_user_from_token
from .serializers import TransactionSerializer1
from .models import Transaction

class TransactionViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Retrieve list of transactions",
        responses={200: TransactionSerializer1(many=True)},
        tags=['Transaction']
    )
    def list(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer1(transactions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new transaction",
        request_body=TransactionSerializer1,
        responses={201: TransactionSerializer1()},
        tags=['Transaction']
    )
    def create(self, request):
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_account_instance = UserUserAccount.objects.get(user=user)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        
        serializer = TransactionSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save(account = account_instance,created_by_user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Retrieve a specific transaction",
        responses={200: TransactionSerializer1()},
        tags=['Transaction']
    )
    def retrieve(self, request, pk=None):
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer1(transaction)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update an existing transaction",
        request_body=TransactionSerializer1,
        responses={200: TransactionSerializer1()},
        tags=['Transaction']
    )
    def update(self, request, pk=None):
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer1(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Delete an existing transaction",
        responses={204: "No Content"},
        tags=['Transaction']
    )
    def destroy(self, request, pk=None):
        transaction = Transaction.objects.get(pk=pk)
        transaction.delete()
        return Response(status=204)
