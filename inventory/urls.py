# inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CompanyViewSet, WarehouseViewSet, 
    ProductViewSet, StockViewSet, InventoryTaskViewSet,
    SaleViewSet, SaleItemViewSet, CustomerViewSet, 
    PaymentViewSet, SalesReportView,CurrencyViewSet)


router = DefaultRouter()

router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'warehouse', WarehouseViewSet, basename='warehouse')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'tasks', InventoryTaskViewSet, basename='task')
router.register(r'sales',SaleViewSet,basename='sale')
router.register(r'sale-items',SaleItemViewSet,basename='saleitem')
router.register(r'customers',CustomerViewSet)
router.register(r'payments',PaymentViewSet)
router.register(r'currencies',CurrencyViewSet, basename='currency')



urlpatterns = [
    path('', include(router.urls)),
    path('reports/sales/', SalesReportView.as_view(), name='sales-report'),

]