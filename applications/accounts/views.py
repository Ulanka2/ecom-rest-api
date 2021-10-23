from django.shortcuts import render
from rest_framework.views  import  APIView
from applications.accounts.serializers import RegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegistrationAPIView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username =serializer.validated_data.get('username')
        password =serializer.validated_data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Пользователь с таким именем уже существует'}, 
                             status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,}, status=status.HTTP_201_CREATED)



