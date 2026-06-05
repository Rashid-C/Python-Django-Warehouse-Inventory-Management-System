

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from .models import InventoryTask, Sale, PurchaseItem, Stock,SaleItem


@receiver(post_save, sender=InventoryTask)
def update_stock_on_task_completion(sender, instance, created, **kwargs):
    if instance.status == 'COMPLETED':
       
        if instance.task_type == 'INBOUND' and instance.to_warehouse:
            stock, _ = Stock.objects.get_or_create(
                warehouse=instance.to_warehouse, product=instance.product
            )
            stock.quantity = F('quantity') + instance.quantity
            stock.save()

     
        elif instance.task_type == 'OUTBOUND' and instance.from_warehouse:
            Stock.objects.filter(warehouse=instance.from_warehouse, product=instance.product).update(
                quantity=F('quantity') - instance.quantity
            )

        elif instance.task_type == 'TRANSFER':
            Stock.objects.filter(warehouse=instance.from_warehouse, product=instance.product).update(
                quantity=F('quantity') - instance.quantity
            )
            dest_stock, _ = Stock.objects.get_or_create(
                warehouse=instance.to_warehouse, product=instance.product
            )
            dest_stock.quantity = F('quantity') + instance.quantity
            dest_stock.save()


@receiver(post_save, sender=PurchaseItem)
def update_stock_on_purchase(sender, instance, created, **kwargs):
    if created:
        stock, _ = Stock.objects.get_or_create(
            warehouse=instance.purchase.warehouse, 
            product=instance.product
        )
        stock.quantity = F('quantity') + instance.quantity
        stock.save()


@receiver(post_save, sender=SaleItem)
def update_stock_on_sale_item_creation(sender, instance, created, **kwargs):

    if created and instance.sale.status == 'COMPLETED':
        Stock.objects.filter(
            warehouse=instance.warehouse, 
            product=instance.product
        ).update(
            quantity=F('quantity') - instance.quantity
        )