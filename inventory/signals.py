# inventory/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InventoryTask, Stock

@receiver(post_save, sender=InventoryTask)
def update_stock_on_task_completion(sender, instance, created, **kwargs):
    if instance.status == 'COMPLETED':
        
        # 1. Handle Inbound Tasks
        if instance.task_type == 'INBOUND' and instance.to_warehouse:
            stock, _ = Stock.objects.get_or_create(
                warehouse=instance.to_warehouse,
                product=instance.product
            )
            stock.quantity += instance.quantity
            stock.save()

        # 2. Handle Outbound Tasks
        elif instance.task_type == 'OUTBOUND' and instance.from_warehouse:
            try:
                stock = Stock.objects.get(
                    warehouse=instance.from_warehouse,
                    product=instance.product
                )
                stock.quantity = max(0, stock.quantity - instance.quantity)
                stock.save()
            except Stock.DoesNotExist:
                pass

        # 3. Handle Transfer Tasks
        elif instance.task_type == 'TRANSFER' and instance.from_warehouse and instance.to_warehouse:
            try:
                source_stock = Stock.objects.get(warehouse=instance.from_warehouse, product=instance.product)
                source_stock.quantity = max(0, source_stock.quantity - instance.quantity)
                source_stock.save()
            except Stock.DoesNotExist:
                pass
            
            dest_stock, _ = Stock.objects.get_or_create(warehouse=instance.to_warehouse, product=instance.product)
            dest_stock.quantity += instance.quantity
            dest_stock.save()