from django.db import models

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
    warehouse=models.ForeignKey(Warehouse,on_delete=models.CASCADE, related_name='stocks')
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name="stocks")
    quantity=models.PositiveIntegerField(default=0)
    updated_at=models.DateTimeField(auto_now=True)

class Meta:

    constraints=[

        models.UniqueConstraint(fields=["warehouse","product"], name='unique_warehouse_product_stock')

    ]

    
    def __str__(self):
        return f"{self.product.title} -Qty: {self.quantity} at {self.warehouse.name}"