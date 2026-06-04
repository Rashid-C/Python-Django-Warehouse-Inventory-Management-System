from rest_framework import serializers
from .models import Company,Warehouse,Product,Stock,InventoryTask


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']


class WarehouseSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    class Meta:
        model = Warehouse
        fields = ['id', 'company', 'company_id', 'name', 'location_address', 'created_at']
        read_only_fields = ['id', 'created_at']
        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'company', 'company_id', 'title', 'sku', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']
        depth = 1


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

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Qty can't be negative.")
        return value  


class InventoryTaskSerializer(serializers.ModelSerializer):
   
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    from_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source='from_warehouse', write_only=True, required=False, allow_null=True
    )
    to_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source='to_warehouse', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = InventoryTask
        fields = [
            'id', 'task_type', 'product', 'product_id', 'quantity', 
            'from_warehouse', 'from_warehouse_id', 'to_warehouse', 
            'to_warehouse_id', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        depth = 1