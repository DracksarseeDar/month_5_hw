from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterValidateSerializer, ConfirmUserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode
import random


@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password, is_active=False)

    code = str(random.randint(100000, 999999))
    ConfirmCode.objects.create(user=user, code=code)

    return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id, 'code': code})


@api_view(['POST'])
def confirm_api_view(request):
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


@api_view(['POST'])
def authorization_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    
    if user is not None:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)


