from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Warehouse, Product, Stock
from .serializers import CompanySerializer, WarehouseSerializer, ProductSerializer, StockSerializer

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
    
    # 1. Enable filtering and search engines
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # 2. Exact match filters (e.g., /api/stocks/?warehouse=1)
    filterset_fields = ['warehouse', 'product']

    
    # 3. Text search filters (e.g., /api/stocks/?search=Laptop)
    # The double underscore __ allows searching inside related model fields!
    search_fields = ['product__title', 'warehouse__name']


    
    # 4. Allow sorting (e.g., /api/stocks/?ordering=-quantity)
    ordering_fields = ['quantity', 'updated_at']