import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import ConfirmCode
from .serializers import RegisterValidateSerializer, ConfirmUserSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.create_user(username=username, password=password, is_active=False)

        code = str(random.randint(100000, 999999))
        ConfirmCode.objects.create(user=user, code=code)

        return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id, 'code': code})

class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data.get('code')
        
        try:
            confirm = ConfirmCode.objects.get(code=code)
        except ConfirmCode.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Кода не существует'})
            
        user = confirm.user
        user.is_active = True
        user.save()
        confirm.delete()
        
        return Response(status=status.HTTP_200_OK, data={'сообщение': 'Пользователь успешно подтвержден!'})


class AuthAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            if not user.is_active:
                return Response(
                    status=status.HTTP_403_FORBIDDEN, 
                    data={'error': 'Ваш аккаунт еще не активирован. Пожалуйста, подтвердите код.'}
                )

            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist: 
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Неверный логин или пароль'})