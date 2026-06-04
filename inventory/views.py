
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import ( Company, Warehouse, Product, Stock, 
InventoryTask,Sale,SaleItem,Customer,Payment )
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CompanySerializer, 
    WarehouseSerializer, 
    ProductSerializer, 
    StockSerializer, 
    InventoryTaskSerializer,SaleSerializer, SaleItemSerializer,CustomerSerializer,
    PaymentSerializer
    
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

    permission_classes=[IsAuthenticated]
    
   
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

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        
        if task.status == 'COMPLETED':
            return Response(
                {'error': 'This task is already completed!'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        task.status = 'COMPLETED'
        task.save()  
        
        return Response(
            {'status': f'Task #{task.id} marked as completed, stock levels updated successfully.'},
            status=status.HTTP_200_OK
        )
    
class SaleViewSet(viewsets.ModelViewSet):
    queryset=Sale.objects.all()
    serializer_class=SaleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'company']
    search_fields = ['invoice_number']


class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset=Payment.objects.all()
    serializer_class=PaymentSerializer