from drf_yasg.utils import swagger_auto_schema
from user.tokens import get_user_from_token
from user_type.models import UserType
from user_type.serializers import UserTypeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

# Create your views here.
class UserTypeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of user types",
        responses={200: UserTypeSerializer(many=True)},
        tags=["User Type"]
    )
    def list(self, request):
        queryset = UserType.objects.all().order_by('name')
        serializer = UserTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Retrieve a user type by ID",
        responses={200: UserTypeSerializer()},
        tags=["User Type"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user type",
        request_body=UserTypeSerializer,
        responses={201: UserTypeSerializer()},
        tags=["User Type"]
    )
    def create(self, request):
        user = get_user_from_token(request.auth)
        if user is None:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing user type",
        request_body=UserTypeSerializer,
        responses={200: UserTypeSerializer()},
        tags=["User Type"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partial update of an existing user type",
        request_body=UserTypeSerializer,
        responses={200: UserTypeSerializer()},
        tags=["User Type"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a user type",tags=["User Type"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
