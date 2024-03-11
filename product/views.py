from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from classification.models import Classification
from product.models import Product
from user.models import UserUserAccount
from drf_yasg import openapi
from user.tokens import get_user_from_token
from .serializers import ProductClassificationSerializer, ProductSerializer, ProductSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
# Create your views here.

class ProductViewSet(viewsets.ViewSet):
    
    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={status.HTTP_201_CREATED: 'Product created successfully'},
        operation_description='Create a new product',
        tags=["Product"]
    )

    @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)
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
        
        serializer = ProductSerializer(data=request.data, context = {'user': user })
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Assuming you have user authentication
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={status.HTTP_201_CREATED: ProductSerializer},
        operation_description='Create a new group product',
        tags=["Product"]
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["post"])
    def add_group_product(self, request, *args, **kwargs):

        #get loggined user
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Extract order data from the request data
        data = request.data.copy()
        # initialized serializer
        serializer = ProductSerializer(data=data, context = {'user': user })
        # check if order data is valid
        if serializer.is_valid():
            # save order
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)},
        operation_summary="List all products",
        tags=["Product"],
        manual_parameters=[
        openapi.Parameter(
            'product_name',
            openapi.IN_QUERY,
            description="Filter by product name",
            type=openapi.TYPE_STRING,
            required=False
        )
        ,openapi.Parameter(
            'page',
            openapi.IN_QUERY,
            description="Page number",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'classification',
            openapi.IN_QUERY,
            description="Filter by product classification",
            type=openapi.TYPE_STRING,
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
        filter_conditions = Q(account=account_instance)
        product_name = request.query_params.get('product_name')
        classification_value = request.query_params.get('classification')


        if(product_name is not None):
            filter_conditions &= Q(name__icontains=product_name)
        if classification_value is not None:
            mainClass = Classification.objects.get(pk=classification_value)
            if mainClass.depth == 0:
                filter_conditions &= Q(productclassification__classification__parent=classification_value)
            else:
                filter_conditions &= Q(productclassification__classification__id=classification_value)
        queryset = Product.objects.filter(filter_conditions).distinct()
        page_number = request.query_params.get('page')
        paginator = PageNumberPagination()
        #paginator.page_size = 10  # Optional, you can set it here if you want to override the default page size
        result_page = paginator.paginate_queryset(queryset, request, page_number)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(
        request_body=ProductClassificationSerializer(many=True),
        responses={status.HTTP_201_CREATED: ProductSerializer},
        operation_description='Add clasification to product',
        tags=["Product"],
        manual_parameters=[
        openapi.Parameter(
            'product',
            openapi.IN_QUERY,
            description="product id",
            type=openapi.TYPE_STRING,
            required=False
        ),
       
    ]
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["put"])
    def add_product_classification(self, request, *args, **kwargs):

        #get loggined user
        user = get_user_from_token(request.auth)
        #check if there is a user
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        product = request.query_params.get('product')
        # Extract order data from the request data
        data = request.data.copy()
        # initialized serializer
        serializer = ProductClassificationSerializer(data=data, many=True)
        # check if order data is valid
        if serializer.is_valid():
            # save order
            serializer.save(product_id = product,created_by_user=user)
            product_instance =  Product.objects.get(pk=product)
            product_serializer = ProductSerializer(data = product_instance)  
            if product_serializer.is_valid():
                return Response(product_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)