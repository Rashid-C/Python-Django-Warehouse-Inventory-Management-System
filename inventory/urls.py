from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, WarehouseViewSet, ProductViewSet, StockViewSet

# Create a router
router=DefaultRouter()

# Create register
router.register(r'companies',CompanyViewSet,basename='company')
router.register(r'warehouse',WarehouseViewSet,basename='warehouse')
router.register(r'products',ProductViewSet,basename='product')
router.register(r'stocks',StockViewSet,basename='stock')



# The API URLs are now determined automatically by the router
urlpatterns = [
    path('',include(router.urls))
]



