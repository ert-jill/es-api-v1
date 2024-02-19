from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated

from account.models import UserAccount
from user.models import UserUserType
from .tokens import get_tokens_for_user, get_user_from_token
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    AccountSerializer,
    AccountUserSerializer,
    ForceChangePassSerializer,
    LoginSerializer,
    UserSerializer,
    UserUserTypeSerializer,
)
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from django.contrib.auth.hashers import make_password

# Create your views here.


class UserViewSet(ViewSet):

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={status.HTTP_200_OK: "Logined Successful"},
        operation_description="Login end-point",
        tags=["User"],
    )
    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({"access_token": tokens}, status=status.HTTP_200_OK)

        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    @swagger_auto_schema(
        request_body=AccountUserSerializer,
        responses={status.HTTP_201_CREATED: "User successfully created"},
        operation_description="Create account user end-point",
        tags=["User"],
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["post"])
    def signup(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)

        if user is None or not user.is_superuser:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        account_user_serializer = AccountUserSerializer(data=request.data)

        if account_user_serializer.is_valid():
            try:
                validated_data = account_user_serializer.validated_data
                validated_data["password"] = make_password(validated_data["password"])
                account_user_serializer.save()
                response_data = {"message": "User successfully created"}
                return Response(data=response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    data=account_user_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data=account_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        request_body=ForceChangePassSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "Password changed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
            status.HTTP_400_BAD_REQUEST: "Invalid data or error in changing password",
            status.HTTP_401_UNAUTHORIZED: "Not authorized",
        },
        operation_description="Force change user's password (admin only)",
        tags=["User"],
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["put"])
    def force_change_password(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)
        if user is None or not user.is_superuser:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        force_change_pass_serializer = ForceChangePassSerializer(data=request.data)
        if force_change_pass_serializer.is_valid():
            try:
                validated_data = force_change_pass_serializer.validated_data
                user = User.objects.get(username=validated_data["username"])
                if user is None:
                    return Response(
                        {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
                    )
                user.set_password(validated_data["password"])
                user.save()
                response_data = {"message": "Password changed"}
                return Response(data=response_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    data=force_change_pass_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data=force_change_pass_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(responses={200: AccountSerializer(many=True)}, tags=["User"])
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["get"])
    def get_user_accounts(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)
        user_accounts = UserAccount.objects.filter(user=user)
        account_tags = []
        for user_account in user_accounts:
            account_tags.append(user_account.account)
        if not account_tags:
            return Response(
                {"detail": "No account tag."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AccountSerializer(account_tags, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: AccountUserSerializer()},
        operation_summary="Retrieve a user",
        tags=["User"],
    )
    @permission_classes([IsAuthenticated])
    def retrieve(self, request, pk=None):
        model = get_object_or_404(User, pk=pk)
        serializer = AccountUserSerializer(model)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: AccountUserSerializer()},
        operation_summary="Retrieve a user details",
        tags=["User"],
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["get"])
    def get_user_details(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)
        # user_details = UserUserType.objects.get(user=user)
        serializer = AccountUserSerializer(user)
        # serializer.user_account=serializer.get_user_type(user)
        # serializer.account=serializer.get_account(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)},
        operation_summary="List all users",
        tags=["User"],
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["get"])
    def get_user_list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = User.objects.all()
        else:
            queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserUserTypeSerializer,
        responses={status.HTTP_201_CREATED: "User successfully tag a type"},
        operation_description="Tag a user type",
        tags=["User"],
    )
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["post"])
    def tag_user_type(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)

        if user is None or not user.is_superuser:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = UserUserTypeSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                response_data = {"message": "User successfully tag a type"}
                return Response(data=response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @swagger_auto_schema(
    #     request_body=UserSerializer,
    #     responses={200: UserSerializer()},
    #     operation_summary="Update a user",
    #     tags=["User"],
    # )
    # @permission_classes([IsAuthenticated])
    # def update(self, request, pk=None):
    #     model = User.objects.get(pk=pk)
    #     serializer = UserSerializer(model, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def userAuth(request):
#     username = request.data.get("username")
#     password = request.data.get("password")
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         tokens = get_tokens_for_user(user)
#         return Response({"access_token": tokens}, status=status.HTTP_200_OK)

#     return Response(
#         {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
#     )

# @api_view(["POST"])
# def userCreate(request, *args, **kwargs):
#     user = get_user_from_token(request.auth)

#     if user is None or not user.is_superuser:
#         return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

#     account_user_serializer = AccountUserSerializer(data=request.data)

#     if account_user_serializer.is_valid():
#         account_user = account_user_serializer.save()
#         response_data = {"message": "User successfully created"}
#         return Response(data=response_data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(data=account_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# use to get user data using token
#


# # @api_view(["POST"])
# # @permission_classes([IsAuthenticated])
# # @swagger_auto_schema(
# #     request_body=AccountUserSerializer,
# #     responses={
# #         201: {
# #             "description": "User created successfully",
# #             "content": {"application/json": {"example": {"message": "User successfully created"}}},
# #         },
# #         400: {"description": "Bad request", "content": {"application/json": {"example": {"error": "Validation error"}}}},
# #         401: {"description": "Unauthorized", "content": {"application/json": {"example": {"error": "Not authorized"}}}},
# #     },
# #     operation_description="Endpoint for user login and obtaining JWT token.",
# # )
# # @method_decorator(name='get', decorator=swagger_auto_schema(
# #         manual_parameters=[
# #             openapi.Parameter(

# #             )
# #         ]
# # ))

# class UserViewSet(ModelViewSet):

#     def create_account_user(self, request, *args, **kwargs):
#         user = get_user_from_token(request.auth)

#         if user is None or not user.is_superuser:
#             return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

#         account_user_serializer = AccountUserSerializer(data=request.data)

#         if account_user_serializer.is_valid():
#             account_user = account_user_serializer.save()
#             response_data = {"message": "User successfully created", "user": account_user_serializer.data}
#             return Response(data=response_data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(data=account_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def auth(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             tokens = get_tokens_for_user(user)
#             return Response({"access_token": tokens}, status=status.HTTP_200_OK)

#         return Response(
#             {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
#         )
# # @api_view(["POST"])
# # def login(request):
# #     username = request.data.get("username")
# #     password = request.data.get("password")
# #     user = authenticate(username=username, password=password)
# #     if user is not None:
# #         tokens = get_tokens_for_user(user)
# #         response = {"message": "Login Successfull", "user": user, "tokens": tokens}
# #         return Response(data=response, status=status.HTTP_200_OK)
# #     else:
# #         return Response(data={"message": "Invalid user or password"})


# # @api_view(["POST"])
# # @authentication_classes([])
# # @permission_classes([])
# # def custom_login_view(request):
# #     """
# #     Obtain JWT token with username and password.
# #     """

# #     # Your login logic here
# #     return TokenObtainPairView.as_view()(request)


# # from rest_framework.views import APIView


# # @api_view(["GET"])
# # @permission_classes([IsAuthenticated])
# # @swagger_auto_schema(
# #     responses={
# #         200: "OK - Authenticated endpoint accessed successfully",
# #         401: "Unauthorized - Invalid or expired token",
# #     },
# #     operation_description="Endpoint that requires authentication using JWT token.",
# # )
# # def authenticated_endpoint(request):
# #     print(request.auth)
# #     user = get_user_from_token(request.auth)
# #     print(user.is_superuser)
# #     if user is not None and user.is_superuser:
# #     # Your authenticated endpoint logic here
# #         return Response({"message": "Authenticated endpoint accessed successfully"})


# # @swagger_auto_schema(
# #     request_body=LoginSerializer,
# #     responses={
# #         200: "OK - Login successful",
# #         401: "Unauthorized - Invalid credentials",
# #     },
# #     operation_description="Endpoint for user login and obtaining JWT token.",
# # )
