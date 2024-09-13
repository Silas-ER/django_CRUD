from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer

import json

@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_by_nick(request, nick):
    try:
        user = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user) #se estiver encontrado vai ser transformado num json
        return Response(serializer.data)
    
@api_view(['GET','POST','PUT','DELETE'])
def user_manager(request):

    # OBTER DADOS
    if request.method == 'GET':
        try:
            if request.GET['user']:

                user_nickname = request.GET['user'] #parametro passado na url

                try:
                    user = User.objects.get(pk=user_nickname)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND) #usuario não encontrado
                
                serializer = UserSerializer(user)
                return Response(serializer.data)
            
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST) #requisição veio com parametro errado
        
    # CRIAR DADOS
    if request.method == 'POST':
        new_user = request.data

        serializer = UserSerializer(data=new_user) #serializando dados 

        if serializer.is_valid(): #verificação se os dados são validos
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # MODIFICAR DADOS
    if request.method == 'PUT':

        nickname = request.data['user_nickname'] #parametro passado na url

        try:
            updated_user = User.objects.get(pk=nickname)    #verifica se o nickname existe na base de dados 
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        print(request.data)

        serializer = UserSerializer(updated_user, data=request.data) #indica qual objeto vai ser editado

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # DELETAR DADOS
    if request.method == 'DELETE':
    
        try:
            user_to_delete = User.objects.get(pk=request.data['user_nickname'])    #verifica se o nickname existe na base de dados 
            user_to_delete.delete() # deletamos diretamente o objeto
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
# Create your views here.
