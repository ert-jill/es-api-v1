# from django.http import HttpResponse, JsonResponse
# import json
# from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from account.models import Account
from account.serializers import AccountSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet

from user.tokens import get_user_from_token

# Create your views here.

class AccountViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AccountSerializer,
        responses={201: AccountSerializer()},
        operation_summary="Create an account",
        tags=["Account"],
    )
    def create(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)

        if user is None or not user.is_superuser:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        account_serializer = AccountSerializer(data=request.data)

        if account_serializer.is_valid():
            try:
                account_serializer.save(created_by_user=user)
                response_data = {"message": "Account successfully created"}
                return Response(data=response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    data=account_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data=account_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
    @swagger_auto_schema(
        responses={200: AccountSerializer(many=True)},
        operation_summary="List all accounts",
        tags=["Account"],
    )
    def list(self, request):
        queryset = Account.objects.all()
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        responses={200: AccountSerializer()},
        operation_summary="Retrieve an account",
        tags=["Account"],
    )
    def retrieve(self, request, pk=None):
        model = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(model)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=AccountSerializer,
        responses={200: AccountSerializer()},
        operation_summary="Update an account",
        tags=["Account"],
    )
    def update(self, request, pk=None):
        model = Account.objects.get(pk=pk)
        serializer = AccountSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses={204: None},
        operation_summary="Delete an account",
        tags=["Account"],
    )
    def destroy(self, request, pk=None):
        model = Account.objects.get(pk=pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
