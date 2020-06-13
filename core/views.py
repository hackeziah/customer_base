from django.shortcuts import render
from .models import Customer, Profession ,Document, DataSheet #importing tthe models
from .serializer import(
     CustomerSerializer,ProfessionSerializer,
     DataSheetSerializer,DocumentSerializer
     ) # import serialiser
from rest_framework import viewsets #for model sets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication  #token-auth import to get the classes
from rest_framework.permissions import(
    AllowAny,
    IsAdminUser, # use for permission if it is a ADMIN User Auth
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions, #this is use for auth permission reading direct to Model
    DjangoModelPermissionsOrAnonReadOnly
    )
from django.http.response import HttpResponseNotAllowed # from the reponse Class
from rest_framework.filters import SearchFilter,OrderingFilter #my search,orderFilter import
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class =  CustomerSerializer #setting up the serializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filter_fields = ('name',) #for filtering the data
    search_fields = ('name','address','data_sheet__description') #search Filter use "___" for obeject contains
    ordering_fields = ('id','name')
    ordering = ('id',)
    lookup_field = 'cu_number'
    authentication_classes = [TokenAuthentication,] #setting for token must be import first the auth
    permission_classes = [IsAdminUser,] #permission setup if it is adnin auth
    # queryset = Customer.objects.all() #dataset objects
        #this is for overriding method from ModelViewSet -> Mixin
    # import pdb; pdb.set_trace() for trace error in Database

    def get_queryset(self):
        address = self.request.query_params.get('address',None)

        if self.request.query_params.get('active') == 'False':
            status = False
        else:
            status = True

        if address:
            customers = Customer.objects.filter(address__icontains = address,active = status )
        else:
            customers =  customers = Customer.objects.filter(active = status)
        return customers


    # def get_queryset(self):
    #     customers = Customer.objects.all()
    #     return customers

    # def list(self,request,*args, **kwargs): # Overriding of list data though out ModelsMixin
    #     customers = self.get_queryset()
    #     serializer = CustomerSerializer(customers,many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CustomerSerializer(obj) #instance of a this objects
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     customer = Customer.objects.create(
    #         name = data['name'],
    #         address=data['address'],
    #         data_sheet_id=data['data_sheet']
    #     )
    #     profession = Profession.objects.get(id = data['profession']) # For aobject get id of Foreign Key
    #     customer.profession.add(profession)
    #     customer.save()

    #     serializer = CustomerSerializer
    #     return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = self.get_object() #get the object

        data = request.data #requesting data input
        customer.name = data['name'] #a signing datas
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']

        profession = Profession.objects.get(id = data['profession']) # For aobject get id of Foreign Key

        for p in customer.professions.all():
            customer.profession.remove()

        customer.profession.add(profession)
        customer.save()

        serializer = CustomerSerializer
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object() #get the object
        customer.name = request.data.get('name',customer.name)
        customer.address = request.data.get('address',customer.address)
        customer.data_sheet_id = request.data.get('data_sheet',customer.data_sheet)
        customer.save()
        serializer = CustomerSerializer
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()
        return Response("obeject was remove")

    @action(detail=True)
    def deactive(self,request,*args,**kwargs):
        customer = self.get_object()
        customer.active = False
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


    @action(detail=True)
    def active(self,request,*args,**kwargs):
        customer = self.get_object()
        customer.active = True
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=False)
    def deactive_all(self,request,*args,**kwargs):
        customer = Customer.objects.all()
        customer.update(active=False)
        serializer = CustomerSerializer(customer,many = True)
        return Response(serializer.data)

    @action(detail=False)
    def active_all(self,request,*args,**kwargs):
        customer = Customer.objects.all()
        customer.update(active=True)
        serializer = CustomerSerializer(customer,many = True)
        return Response(serializer.data)

    # @action(detail=False, method = ["POST"])
    # def change_status(self,request,*args,**kwargs):
    #     status = True if request.data['active'] == True else False
    #     customers = Customer.objects.all()
    #     customers.update(active=status)
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class =  ProfessionSerializer
    authentication_classes = [TokenAuthentication,]
class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class =  DataSheetSerializer
    permession_classes = [AllowAny,]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class =  DocumentSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly,]