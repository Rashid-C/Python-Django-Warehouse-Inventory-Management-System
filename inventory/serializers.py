from rest_framework import serializers
from .models import Company
from .models import Warehouse
from .models import Product
from .models import Stock

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields=['id','name','address','created_at']
        read_only_fields=['id','created_at']


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Warehouse
        fields=['id','company','name','location_address','created_at']
        read_only_fields = ['id', 'created_at']
        depth=1

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'company', 'title', 'sku', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model=Stock
        fields=['id','warehouse','product','quantity','created_at']
        read_only_fields = ['id', 'created_at']