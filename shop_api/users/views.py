from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView, GenericAPIView
import random
import string
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer,
    CustomTokenObtainPairSerializer,
)
from .models import ConfirmationCode
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

CustomUser = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        phone_number = serializer.validated_data.get('phone_number', '')
        birthdate = serializer.validated_data.get('birthdate')
        first_name = serializer.validated_data.get('first_name', '')
        last_name = serializer.validated_data.get('last_name', '')


        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                phone_number=phone_number,
                birthdate=birthdate, 
                is_active=False ,
                first_name =first_name,
                last_name =last_name,
                registration_source='local'
            )

            code = ''.join(random.choices(string.digits, k=6))
            ConfirmationCode.objects.create(user=user, code=code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={'user_id': user.id, 'confirmation_code': code}
        )

class ConfirmUserAPIView(GenericAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        with transaction.atomic():
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'User not found'})
            
            user.is_active = True
            user.save()

            refresh = RefreshToken.for_user(user)
            
            ConfirmationCode.objects.filter(user=user).delete()

        return Response(
            status=status.HTTP_200_OK,
            data={
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        )



# class AuthorizationAPIView(GenericAPIView):
#     serializer_class = AuthValidateSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = authenticate(**serializer.validated_data)

#         if user:
#             if not user.is_active:
#                 return Response(
#                     status=status.HTTP_401_UNAUTHORIZED,
#                     data={'error': 'CustomUser account is not activated yet!'}
#                 )

#             token, _ = Token.objects.get_or_create(user=user)
#             return Response(data={'key': token.key})

#         return Response(
#             status=status.HTTP_401_UNAUTHORIZED,
#             data={'error': 'CustomUser credentials are wrong!'}
#         )
