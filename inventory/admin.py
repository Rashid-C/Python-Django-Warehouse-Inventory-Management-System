# inventory/admin.py
from django.contrib import admin
from .models import Company, Warehouse, Product, Stock, InventoryTask

# Standard registration for simple tables
admin.site.register(Company)
admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(Stock)

# Advanced registration with a custom dashboard for tasks
@admin.register(InventoryTask)
class InventoryTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_type', 'product', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'task_type')
    search_fields = ('product__title',)