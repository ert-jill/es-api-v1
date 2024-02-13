from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from classification.models import Classification
from classification.serializers import ClassificationSerializer
from user.tokens import get_user_from_token
# Create your views here.

class ClassificationViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        request_body=ClassificationSerializer,
        responses={status.HTTP_201_CREATED: 'Classification created successfully'},
        operation_description='Create a new classification',
        tags=["Classification"]
    )

    @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ClassificationSerializer(data=request.data)
        # get user's account
        user_account_instance = user.useraccount_set.order_by("-dateAdded").first()
        # check if user's has account tagged
        if user_account_instance:
            # get assigned account
            account_instance = user_account_instance.account
        else:
            # Handle the case where no UserAccount is found for the user
            raise serializer.ValidationError({"account": "Account not found"})
        
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by_user_id=user.id, account = account_instance)  # Assuming you have user authentication
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: 'Classification List found'},
        operation_description='Get all classification',
        tags=["Classification"]
    )
    
    @permission_classes([IsAuthenticated])
    def list(self, request):
        user = get_user_from_token(request.auth)
        # get user's account
        user_account_instance = user.useraccount_set.order_by("-dateAdded").first()
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
        queryset = Classification.objects.filter( account = account_instance) # just get the classification for the specific account
        serializer = ClassificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
        