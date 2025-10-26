from partstock.models import Part, MovementItem
from django.db import transaction
from decimal import Decimal

class PartService:
    @staticmethod
    def get_all_parts():
        return Part.objects.all()
        
    @staticmethod
    def get_part_by_id(part_id: int) -> Part:
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
        part = PartService.get_part_by_id(part_id)
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
        part = PartService.get_part_by_id(part_id)
        if MovementItem.objects.filter(part=part_id).count() > 0:
            raise ValueError('Unable to delete the item. There is a movement history')
        part.delete()
