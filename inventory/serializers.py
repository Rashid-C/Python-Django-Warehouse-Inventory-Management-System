from rest_framework import serializers
from .models import (
Company,Warehouse,
Product,Stock,
InventoryTask,
Sale,SaleItem,
Customer,Payment,
Currency,Supplier,
Purchase,PurchaseItem
)


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


class SaleItemNestedSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'warehouse', 'quantity', 'price_at_sale']

    def validate(self, data):
        product = data.get('product')
        warehouse = data.get('warehouse')
        requested_quantity = data.get('quantity')

        #
        stock = Stock.objects.filter(warehouse=warehouse, product=product).first()

      
        if not stock:
            raise serializers.ValidationError(
                f"No stock record found for this product in this warehouse."
            )

        if stock.quantity < requested_quantity:
            raise serializers.ValidationError(
                f"Insufficient stock! Available: {stock.quantity}, Requested: {requested_quantity}."
            )
        
        return data


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemNestedSerializer(many=True)

    class Meta:  
        model = Sale  
        fields = ['id', 'invoice_number', 'company', 'status', 'created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        
        for item_data in items_data:
            SaleItem.objects.create(sale=sale, **item_data)
            
        return sale
    

class SaleItemSerializer(serializers.ModelSerializer):
    sale = serializers.PrimaryKeyRelatedField(queryset=Sale.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())

    class Meta:
        model = SaleItem
        fields = ['id', 'sale', 'product', 'warehouse', 'quantity', 'price_at_sale']

    def validate(self, data):
        product = data.get('product')
        warehouse = data.get('warehouse')
        requested_qty = data.get('quantity')

        try:
            
            stock_obj = Stock.objects.select_for_update().get(
                product=product, 
                warehouse=warehouse
            )
        except Stock.DoesNotExist:
            raise serializers.ValidationError(
                "Stock record for this product in this warehouse does not exist."
            )
        
        if requested_qty > stock_obj.quantity:
            raise serializers.ValidationError(
                f"Insufficient stock! Available: {stock_obj.quantity}, Requested: {requested_qty}"
            )
            
        return data



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model=Currency
        fields=['id','code','name','symbol']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'unit_price']

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ['invoice_number', 'total_amount', 'supplier', 'company', 'items']

    def create(self, validated_data):
       
        items_data = validated_data.pop('items')
        
      
        purchase = Purchase.objects.create(**validated_data)
        
        
        for item_data in items_data:
            PurchaseItem.objects.create(purchase=purchase, **item_data)
            
        return purchase