
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InventoryTask, Stock, Sale,SaleItem

@receiver(post_save, sender=InventoryTask)
def update_stock_on_task_completion(sender, instance, created, **kwargs):
    if instance.status == 'COMPLETED':
        
        
        if instance.task_type == 'INBOUND' and instance.to_warehouse:
            stock, _ = Stock.objects.get_or_create(
                warehouse=instance.to_warehouse,
                product=instance.product
            )
            stock.quantity += instance.quantity
            stock.save()

    
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


@receiver(post_save, sender=Sale)
def handle_sale_completion(sender, instance, created, **kwargs):
    if instance.status=='COMPLETED':
        for item in instance.items.all():
            stock = Stock.objects.filter(warehouse=item.warehouse, product=item.product).first()
            
            if stock:
                stock.quantity -= item.quantity
                stock.save()
            else:
                Stock.objects.create(
                    warehouse=item.warehouse,
                    product=item.product,
                    quantity=-item.quantity
                )



@receiver(post_save, sender=Sale)
def update_stock_on_sale(sender, instance, created, **kwargs):
    if instance.status == "COMPLETED":
        for item in instance.items.all():
            try:
                stock_record = Stock.objects.get(
                    warehouse_id=item.warehouse_id, 
                    product_id=item.product_id
                )
                stock_record.quantity -= item.quantity
                stock_record.save()
            except Stock.DoesNotExist:
                pass


@receiver(post_save, sender=SaleItem)
def update_stock_on_item_save(sender, instance, created, **kwargs):
   
    if instance.sale and instance.sale.status and instance.sale.status.upper() == "COMPLETED":
        try:
            stock_record = Stock.objects.get(
                warehouse_id=instance.warehouse_id,
                product_id=instance.product_id
            )
            
            stock_record.quantity -= instance.quantity
            stock_record.save()
            
        except Stock.DoesNotExist:
            pass