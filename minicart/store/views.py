from django.shortcuts import render
from .serializers import ProductModelSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet


# Create your views here.

class ProductView(APIView):
     def get(self,request):
        prod=Product.objects.all()
        dser=ProductModelSerializer(prod,many=True)
        return Response(data=dser.data)
    
     def post(self,request):
        ser=ProductModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"Ok"})
        return Response(data=ser.errors)

class SpecificProductView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        prod=Product.objects.get(id=id)
        dser=ProductModelSerializer(prod)
        return Response(data=dser.data)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        prod=Product.objects.get(id=id)
        prod.delete()
        return Response({"msg":"Deleted"})
    
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        prod=Product.objects.get(id=id)
        ser=ProductModelSerializer(data=request.data,instance=prod)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"Updated"})
        return Response(data=ser.errors)    
    
class ProductVSet(ViewSet):
    def retrieve(self,request,*args,**kwargs):
        pid=kwargs.get("pk")
        prod=Product.objects.get(id=pid)
        dser=ProductModelSerializer(prod)
        return Response(data=dser.data)
    def list(self,request):
        prodlist=Product.objects.all()
        dser=ProductModelSerializer(prodlist,many=True)
        return Response(data=dser.data)
    def create(self,request):
        ser=ProductModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        return Response(data=ser.errors)
    def update(self,request,*args,**kwargs):
        pid=kwargs.get("pk")
        prod=Product.objects.get(id=pid)
        ser=ProductModelSerializer(data=request.data,instance=prod)
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        return Response(data=ser.errors)
    def destroy(self,request,*args,**kwargs):
        pid=kwargs.get("pk")
        prod=Product.objects.get(id=pid)
        prod.delete()
        return Response({"msg":"DELETED"})
    
    @action(methods=["GET"],detail=False)
    def category(self,request,*args,**kwargs):
        cat=Product.objects.values_list("category",flat=True).distinct()
        return Response(data=cat) 

from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
             
class ProductMVSet(ModelViewSet):
    serializer_class=ProductModelSerializer
    queryset=Product.objects.all()
    # authentication_classes=[BasicAuthentication]
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    

class UserVset(ViewSet):
    def create(self,request):
        ser=UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"Created"})
        return Response({"msg":"Failed"})