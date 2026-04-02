from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MovementItem


@receiver(post_save, sender=MovementItem)
def update_stock_on_save(sender, instance, created, **kwargs):
    part = instance.part
    quantity = instance.quantity
    movement_type = instance.movement.movement_type

    if created:
        if movement_type == 'IN':
            part.current_stock += quantity
        else:
            part.current_stock -= quantity
        part.save(update_fields=['current_stock'])


@receiver(post_delete, sender=MovementItem)
def update_stock_on_delete(sender, instance, **kwargs):
    part = instance.part
    quantity = instance.quantity
    movement_type = instance.movement.movement_type

    if movement_type == 'IN':
        part.current_stock -= quantity
    else:
        part.current_stock += quantity
    part.save(update_fields=['current_stock'])
