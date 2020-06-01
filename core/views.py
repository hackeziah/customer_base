from django.shortcuts import render
from .models import Customer, Profession ,Document, DataSheet #importing tthe models
from .serializer import(
     CustomerSerializer,ProfessionSerializer,
     DataSheetSerializer,DocumentSerializer
     ) # import serialiser
from rest_framework import viewsets #for model sets

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all() #dataset objects
    serializer_class =  CustomerSerializer #setting up the serializer

class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class =  ProfessionSerializer

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class =  DataSheetSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class =  DocumentSerializer
