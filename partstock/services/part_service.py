from partstock.models import Part, MovementItem
from .stock_movement_service import StockMovementService
from .movement_item_service import MovementItemService
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from decimal import Decimal

MIN_STOCK_LEVEL = 10

class PartService:
    @staticmethod
    def get_all_parts():
        return Part.objects.all()

    @staticmethod
    def get_by_id(part_id: int) -> Part:
        try:
            return Part.objects.get(pk=part_id)
        except Part.DoesNotExist:
            raise Part.DoesNotExist(f'part with id {part_id} not found')

    @staticmethod
    @transaction.atomic
    def create_new_part(validated_data: dict) -> Part:
        cost = validated_data.get('cost', Decimal('0.00'))
        current_price = validated_data.get('current_price', Decimal('0.00'))

        if current_price < cost:
            raise ValueError('The selling price cannot be less than the cost')

        new_part = Part.objects.create(**validated_data) 
        return new_part

    @staticmethod
    @transaction.atomic
    def update_part(part_id: int, validated_data: dict) -> Part:
        part = PartService.get_by_id(part_id)
        is_active = validated_data.get('is_active')
        if is_active is not None and not is_active:
            if part.current_stock > 0:
                raise ValueError(
                    'Cannot deactivate a Part that still has stock (stock > 0)'
                    )
        part.name = validated_data.get('name', part.name)
        part.description = validated_data.get('description', part.description)
        part.cost = validated_data.get('cost', part.cost)
        part.current_price = validated_data.get('current_price', part.current_price)
        part.is_active = validated_data.get('is_active', part.is_active)
        part.save()
        return part

    @staticmethod
    @transaction.atomic
    def delete_part(part_id: int) -> None:
        part = PartService.get_by_id(part_id)
        if MovementItem.objects.filter(part=part_id).count() > 0:
            raise ValidationError(
                'Unable to delete the item. There is a movement history'
                )
        part.delete()

    @staticmethod
    @transaction.atomic
    def replenish_stock():
        replenishment_data = []
        parts_to_replenish = Part.objects.select_for_update().filter(
            current_stock__lt=MIN_STOCK_LEVEL
        )

        for part in parts_to_replenish:
            delta = MIN_STOCK_LEVEL - part.current_stock

            if delta > 0:
                replenishment_data.append({
                    'part': part,
                    'quantity': delta,
                })

        updated_count = len(replenishment_data)

        if updated_count == 0:
            return 0

        movement_data = {
            'movement_type': 'IN',
            'notes': f"Automatic Minimum Stock Replenishment (CRON) - "
                     f"{updated_count} items",
            'date_recorded': timezone.now()
        }
        movement = StockMovementService.create_new_movement(movement_data)

        for item_data in replenishment_data:
            item_creation_data = {
                'movement': movement,
                'part': item_data['part'],
                'quantity': item_data['quantity'],
            }

            MovementItemService.create_new_movement(item_creation_data)

        return updated_count