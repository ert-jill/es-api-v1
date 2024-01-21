# from django.http import HttpResponse, JsonResponse
# import json
# from django.forms.models import model_to_dict
from rest_framework.decorators import  permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from account.serializers import AccountSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet

from user.tokens import get_user_from_token

# Create your views here.

class AccountViewSet(ViewSet):

    @swagger_auto_schema(
        request_body=AccountSerializer,
        responses={status.HTTP_201_CREATED: AccountSerializer},
        operation_description="Create account end-point",
        tags=["Account"],
    )
    @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        user = get_user_from_token(request.auth)

        if user is None or not user.is_superuser:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        account_serializer = AccountSerializer(data=request.data)

        if account_serializer.is_valid():
            try:
                account_serializer.save()
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

# drf api view
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# def get_account_by_id(request,pk):
#     instance = Account.objects.get(pk=pk)
#     if instance:
#     # Serialize the data
#         serializer = AccountSerializer(instance)

#         # Return the serialized data as JSON response
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         # Handle the case where no data was fetched
#         return Response({"message": "No data found"}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET'])
# def get_accounts(request, *args, **kwargs):
#     all_objects = Account.objects.all()
   
#     if all_objects.exists():
#         # Serialize the data
#         serializer = AccountSerializer(all_objects, many=True)

#         # Return the serialized data as JSON response
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         # Handle the case where no data was fetched
#         return Response({"message": "No data found"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['POST'])
# def insert(request, *args, **kwargs):
#     serializer = AccountSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         print(serializer.data)
#         data = serializer.data
#         return Response(data)
    
    

# # @api_view(['PUT'])
# # def update(request, pk):
# #     try:
# #         # Retrieve the object by ID
# #         obj = Account.objects.get(pk=pk)
# #     except Account.DoesNotExist:
# #         return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

# #     # Serialize the existing object with the updated data
# #     serializer = AccountSerializer(obj, data = request.data)

# #     if serializer.is_valid():
# #         # Save the updated object
# #         serializer.save()
# #         return Response(serializer.data, status=status.HTTP_200_OK)
# #     else:
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PATCH'])
# def update(request, pk):
#     try:
#         # Retrieve the object by ID
#         obj = Account.objects.get(pk=pk)
#     except Account.DoesNotExist:
#         return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

#     # Serialize the existing object with the partially updated data
#     serializer = AccountSerializer(obj, data=request.data, partial=True)

#     if serializer.is_valid():
#         # Save the partially updated object
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def create_account(request,*args,**kwargs):
#     data = {}

#     print(data)
#     body = request.body
#     try:
#         data = json.loads(body)
#     except:
#         pass
#     # param = request.param
#     print(request.GET)
#     data['params'] = dict(request.GET)
#     # data['headers'] = dict(request.headers)
#     print(data)
#     return JsonResponse(data);
