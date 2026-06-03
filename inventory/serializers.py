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
    # Allows entering raw company ID integers on POST requests
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    class Meta:
        model = Warehouse
        fields = ['id', 'company', 'company_id', 'name', 'location_address', 'created_at']
        read_only_fields = ['id', 'created_at']
        depth = 1

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'company', 'title', 'sku', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']


class StockSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source='warehouse', write_only=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = Stock
        fields = ['id', 'warehouse', 'product', 'warehouse_id', 'product_id', 'quantity', 'updated_at']
        read_only_fields = ['id', 'updated_at']
        depth = 1