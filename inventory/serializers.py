from rest_framework import serializers
from .models import Company
from .models import Warehouse

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

