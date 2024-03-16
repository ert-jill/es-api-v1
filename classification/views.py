from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from classification.models import Classification
from classification.serializers import ClassificationSerializer
from user.models import UserUserAccount
from user.tokens import get_user_from_token
from drf_yasg import openapi

# Create your views here.


class ClassificationViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ClassificationSerializer,
        responses={201: ClassificationSerializer()},
        operation_summary="Create a classification",
        tags=["Classification"],
    )
    def create(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ClassificationSerializer(data=request.data)
        # get user's account
        user_account_instance = UserUserAccount.objects.get(user=request.user)
        # check if user's has account tagged
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})

        serializer.is_valid(raise_exception=True)
        serializer.save(
            created_by_user_id=user.id, account=account_instance
        )  # Assuming you have user authentication
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={200: ClassificationSerializer(many=True)},
        operation_summary="List all classifications",
        tags=["Classification"],
         manual_parameters=[
        openapi.Parameter(
            'parent',
            openapi.IN_QUERY,
            description="Filter by classification parent id",
            type=openapi.TYPE_NUMBER,
            required=False
        ), openapi.Parameter(
            'depth',
            openapi.IN_QUERY,
            description="Filter classification by depth value",
            type=openapi.TYPE_NUMBER,
            required=False
        )
    ]
    )
    def list(self, request):
        user = get_user_from_token(request.auth)
        # get user's account
        user_account_instance = UserUserAccount.objects.get(user=user)
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        
        parent_id = request.query_params.get('parent')
        depth = request.query_params.get('depth')
        # Start with an initial queryset containing classifications for the specific account
        queryset = Classification.objects.filter(account=account_instance)
        # Apply filtering based on parent_id if it is provided
        if parent_id:
            queryset = queryset.filter(parent=parent_id)
        # Apply filtering based on depth if it is provided
        if depth:
            # Depending on how depth is used, you might need to adjust this condition
            queryset = queryset.filter(depth=depth)

        serializer = ClassificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: ClassificationSerializer()},
        operation_summary="Retrieve a classification",
        tags=["Classification"],
    )
    def retrieve(self, request, pk=None):
        classification = get_object_or_404(Classification, pk=pk)
        serializer = ClassificationSerializer(classification)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ClassificationSerializer,
        responses={200: ClassificationSerializer()},
        operation_summary="Update a classification",
        tags=["Classification"],
    )
    def update(self, request, pk=None):
        try:
            classification = Classification.objects.get(pk=pk)
        except Classification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data["updated_by_user"] = request.user.id
        serializer = ClassificationSerializer(
            classification, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(created_by_user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: None},
        operation_summary="Delete a classification",
        tags=["Classification"],
    )
    def destroy(self, request, pk=None):
        try:
            classification = Classification.objects.get(pk=pk)
        except Classification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        classification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
