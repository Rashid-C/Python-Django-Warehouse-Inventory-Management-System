from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Company(models.Model):
    name=models.CharField(max_length=255,unique=True)
    address=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Warehouse(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='warehouses') #related_name pointing reverse relationship shortcut to parent(company)
    name=models.CharField(max_length=255)
    location_address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class Product(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE, related_name='products')
    title=models.CharField(max_length=255)
    sku=models.CharField(max_length=100,unique=True)           # Unique barcode/identifier
    price=models.DecimalField(max_digits=10, decimal_places=2) # 399999999.99
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.title} ({self.sku})"
    


class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["warehouse", "product"], name='unique_warehouse_product_stock')
        ]

    def __str__(self):
        return f"{self.product.title} - Qty: {self.quantity} at {self.warehouse.name}"
    
class InventoryTask(models.Model):
    TASK_TYPES = [
        ('INBOUND', 'Receiving New Stock'),
        ('OUTBOUND', 'Shipping to Customer'),
        ('TRANSFER', 'Moving between Warehouses'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Not Started'),
        ('IN_PROGRESS', 'Worker is doing it'),
        ('COMPLETED', 'Finished'),
    ]

    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    from_warehouse = models.ForeignKey(Warehouse, null=True, blank=True, related_name='outgoing_tasks', on_delete=models.SET_NULL)
    to_warehouse = models.ForeignKey(Warehouse, null=True, blank=True, related_name='incoming_tasks', on_delete=models.SET_NULL)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    # Clean look for the admin panel
    def __str__(self):
        return f"{self.task_type} - {self.product.title} ({self.quantity})"
    
class Sale(models.Model):
    STATUS_CHOICE=[
        ('PENDING','Pending Payment'),
        ('COMPLETED','Completed/Dispached'),
        ('CANCELLED','Cancelled'),
    ]

    invoice_number=models.CharField(max_length=50,unique=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    status=models.CharField(max_length=20, choices=STATUS_CHOICE, default='PENDING')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_number} ({self.status})"
    
class SaleItem(models.Model):
    sale=models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse=models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price_at_sale=models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.quantity}x {self.product.title} from {self.warehouse.name}"