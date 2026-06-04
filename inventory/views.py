
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Company, Warehouse, Product, Stock, InventoryTask

from .serializers import (
    CompanySerializer, 
    WarehouseSerializer, 
    ProductSerializer, 
    StockSerializer, 
    InventoryTaskSerializer
)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    
   
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['warehouse', 'product']
    search_fields = ['product__title', 'warehouse__name']
    ordering_fields = ['quantity', 'updated_at']



class InventoryTaskViewSet(viewsets.ModelViewSet):
    queryset = InventoryTask.objects.all()
    serializer_class = InventoryTaskSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'task_type', 'product']
    search_fields = ['product__title']
    ordering_fields = ['created_at', 'quantity']