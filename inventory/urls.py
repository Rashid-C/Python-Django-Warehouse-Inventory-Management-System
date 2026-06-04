# inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, WarehouseViewSet, ProductViewSet, StockViewSet, InventoryTaskViewSet


router = DefaultRouter()

router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'warehouse', WarehouseViewSet, basename='warehouse')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'tasks', InventoryTaskViewSet, basename='task')


urlpatterns = [
    path('', include(router.urls))
]