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