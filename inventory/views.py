from rest_framework import viewsets
from .models import Company, Warehouse, Product, Stock
from .serializers import CompanySerializer, WarehouseSerializer, ProductSerializer, StockSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset=Warehouse.objects.all()
    serializer_class=WarehouseSerializer


class ProductViewaSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset=Stock.objects.all()
    serializer_class=StockSerializer