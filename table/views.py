# views.py

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg import openapi
from user.models import UserUserAccount
from user.tokens import get_user_from_token
from .models import Table
from .serializers import TableReadSerializer, TableSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

class TableViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(tags=['Table'], responses={200: TableReadSerializer(many=True)},
                         manual_parameters=[
        openapi.Parameter(
            'area',
            openapi.IN_QUERY,
            description="Filter by table area",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],)
    def list(self, request):
        user = get_user_from_token(request.auth)
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
       
        # get user's account
        user_account_instance = UserUserAccount.objects.get(pk=user.id)
        # check if user's has account tagged
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        area = request.query_params.get('area')

        if area is not None:
            queryset = Table.objects.filter(account = account_instance ,area = area)
        else:
            queryset = Table.objects.filter(account = account_instance )
        serializer = TableReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Table'], request_body=TableSerializer, responses={201: TableSerializer()})
    def create(self, request):
        user_account_instance = UserUserAccount.objects.get(pk=request.user.id)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_user = request.user,account=account_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Table'], responses={200: TableSerializer()})
    def retrieve(self, request, pk=None):
        queryset = Table.objects.all()
        table = get_object_or_404(queryset, pk=pk)
        serializer = TableSerializer(table)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Table'], request_body=TableSerializer, responses={200: TableSerializer()})
    def update(self, request, pk=None):
        table = Table.objects.get(pk=pk)
        serializer = TableSerializer(table, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Table'], responses={204: "No Content"})
    def destroy(self, request, pk=None):
        table = Table.objects.get(pk=pk)
        table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
