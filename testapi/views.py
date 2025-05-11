from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .serializer import ShipmentSerializer,SignInSerializer,PostShipmentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from .models import RoleModel,ShipmentModel,UserModel
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

#User = get_user_model()

class SignIn(APIView):
    @extend_schema(request=SignInSerializer,responses=SignInSerializer)
    def post(self,request,format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        query = UserModel.objects.filter(email=email).first()
        if query:
            user = UserModel.objects.get(email=email)
            if user.password == password:
                token = RefreshToken.for_user(user)
                print(token.access_token,type(token.access_token))
                return Response({'username':query.userName,'token':str(token.access_token)},status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'Incorrect Password'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':'User doesnot exist'},status=status.HTTP_400_BAD_REQUEST)
    

    
class PrivateShipment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(request=ShipmentSerializer,responses=ShipmentSerializer)
    def get(self,request,format=None):
        number = request.query_params.get('transaction')
        print(request.user)
        query = ShipmentModel.objects.filter(transanctionNumber=number).first()
        if query:
            serializer = ShipmentSerializer(query)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Transaction doesnot exist'},status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(request=PostShipmentSerializer,responses=ShipmentSerializer)
    def post(self,request,format=None):
        username = request.user.userName
        user = UserModel.objects.get(userName=username)
        serializer = PostShipmentSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
        print(request.user)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.validated_data['role'] = user.user_role
            serializer.validated_data['subject_id'] = user
            serializer.save()
            shipmnent = ShipmentModel.objects.last()
            shipmentserializer = ShipmentSerializer(shipmnent)
            return Response(shipmentserializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    




class PrivateCRUDShipment(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=ShipmentSerializer)
    def getall(self,request,format=None):
        query = ShipmentModel.objects.all()
        if query:
            serializer = ShipmentSerializer(query,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Transaction doesnot exist'},status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(request=PostShipmentSerializer,responses=ShipmentSerializer)
    def updateshipment(self,request,id,format=None):
        serializer = ShipmentSerializer(request.data,partial=True)
        if serializer.is_valid():
            username = request.user.userName
            user = UserModel.objects.get(userName=username)
            shipment = ShipmentModel.objects.filter(shipment_id=id).first()
            if shipment:
                if shipment.subject_id.id == user.id:
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response({'msg':f'Shipment does not belong to user {username}'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg':'Shipment does not exist'},status=status.HTTP_400_BAD_REQUEST)
        return  serializer.error_messages
    
    @extend_schema(request=PostShipmentSerializer,responses=PostShipmentSerializer)
    def deleteshipment(self,request,id,format=None):
        query = UserModel.objects.all()
        serializer = PostShipmentSerializer(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)